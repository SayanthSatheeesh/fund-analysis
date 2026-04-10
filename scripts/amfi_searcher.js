const axios = require('axios');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const AMFI_URL = 'https://portal.amfiindia.com/spages/NAVAll.txt';
const dbPath = path.resolve(__dirname, '../data/fund_index.db');

async function fetchAMFIData() {
    try {
        console.log('Fetching NAV data from AMFI...');
        const response = await axios.get(AMFI_URL);
        const rawData = response.data;
        
        const lines = rawData.split('\n');
        const db = new sqlite3.Database(dbPath);
        
        let count = 0;
        
        db.serialize(() => {
            const stmt = db.prepare(`
                INSERT OR REPLACE INTO stg_fund_data (scheme_code, scheme_name, fund_category, nav, date)
                VALUES (?, ?, ?, ?, ?)
            `);

            let currentCategory = '';
            let currentAMC = '';

            for (const line of lines) {
                const trimmedLine = line.trim();
                
                // Skip empty lines or header legend
                if (!trimmedLine || trimmedLine.toLowerCase().includes('scheme code')) continue;

                // Category headers usually contain "Schemes("
                if (trimmedLine.includes('Schemes(')) {
                    currentCategory = trimmedLine;
                    continue;
                }

                // AMC headers are usually lines without semicolons that aren't categories
                if (!trimmedLine.includes(';')) {
                    currentAMC = trimmedLine;
                    continue;
                }

                const parts = line.split(';');
                if (parts.length >= 6) {
                    const schemeCode = parts[0].trim();
                    const schemeName = parts[3].trim();
                    const nav = parseFloat(parts[4]);
                    const date = parts[5].trim();

                    if (!isNaN(nav) && schemeCode && date) {
                        // We store the specific category (e.g., Equity Scheme - Large Cap Fund)
                        stmt.run(schemeCode, schemeName, currentCategory, nav, date);
                        count++;
                    }
                }
            }
            stmt.finalize();
        });

        db.close((err) => {
            if (err) console.error('Error closing DB:', err);
            console.log(`Successfully ingested ${count} fund records.`);
        });

    } catch (error) {
        console.error('Error fetching AMFI data:', error.message);
    }
}

fetchAMFIData();
