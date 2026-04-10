const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const dbPath = path.resolve(__dirname, '../data/fund_index.db');
const db = new sqlite3.Database(dbPath);

function normalizeAMFIDate(dateStr) {
    if (!dateStr) return null;
    const months = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
        'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    };
    const parts = dateStr.split('-');
    if (parts.length !== 3) return dateStr; 
    const day = parts[0].padStart(2, '0');
    const month = months[parts[1]];
    const year = parts[2];
    if (!month) return dateStr;
    return `${year}-${month}-${day}`;
}

async function loadFactData() {
    console.log('Fetching staging data for normalization...');
    
    db.all('SELECT * FROM stg_fund_data', (err, fundRows) => {
        if (err) return console.error(err);

        console.log(`Normalizing ${fundRows.length} fund dates...`);
        
        db.serialize(() => {
            db.run('BEGIN TRANSACTION');
            // Fact table now includes fund_category
            const stmt = db.prepare(`
                INSERT OR REPLACE INTO fact_fund_index (scheme_code, date, fund_category, nav, index_close)
                VALUES (?, ?, ?, ?, (SELECT close FROM stg_index_data WHERE date = ? AND index_name = 'NIFTY 50'))
            `);

            for (const row of fundRows) {
                const normDate = normalizeAMFIDate(row.date);
                stmt.run(row.scheme_code, normDate, row.fund_category, row.nav, normDate);
            }

            stmt.finalize();
            db.run('COMMIT', (err) => {
                if (err) {
                    console.error('Error committing fact data:', err);
                } else {
                    console.log('Fact migration complete.');
                    db.all('SELECT COUNT(*) as count FROM fact_fund_index WHERE index_close IS NOT NULL', (err, rows) => {
                        console.log(`Matched records (Fund + Index): ${rows[0].count}`);
                        db.close();
                    });
                }
            });
        });
    });
}

loadFactData();
