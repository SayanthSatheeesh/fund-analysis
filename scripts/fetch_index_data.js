const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const dbPath = path.resolve(__dirname, '../data/fund_index.db');

async function insertDummyIndexData() {
    const db = new sqlite3.Database(dbPath);
    
    // For Milestone 1, we populate NIFTY 50 dummy data to test the pipeline
    // In a real scenario, this would use an NSE historical data scraper or API
    const today = new Date();
    const data = [];
    
    for (let i = 0; i < 30; i++) {
        const date = new Date(today);
        date.setDate(today.getDate() - i);
        const dateStr = date.toISOString().split('T')[0];
        
        data.push({
            index_name: 'NIFTY 50',
            date: dateStr,
            open: 22000 + Math.random() * 100,
            high: 22100 + Math.random() * 100,
            low: 21900 + Math.random() * 100,
            close: 22050 + Math.random() * 100,
            volume: Math.floor(Math.random() * 1000000)
        });
    }

    db.serialize(() => {
        const stmt = db.prepare(`
            INSERT OR REPLACE INTO stg_index_data (index_name, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        `);

        for (const row of data) {
            stmt.run(row.index_name, row.date, row.open, row.high, row.low, row.close, row.volume);
        }
        stmt.finalize();
    });

    db.close((err) => {
        if (err) console.error('Error closing DB:', err);
        console.log('Successfully inserted 30 days of NIFTY 50 index data.');
    });
}

insertDummyIndexData();
