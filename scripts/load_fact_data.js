const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const dbPath = path.resolve(__dirname, '../data/fund_index.db');
const db = new sqlite3.Database(dbPath);

async function loadFactData() {
    db.serialize(() => {
        // Create the unified fact table
        db.run(`
            CREATE TABLE IF NOT EXISTS fact_fund_index (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scheme_code TEXT NOT NULL,
                date TEXT NOT NULL,
                nav REAL,
                index_close REAL,
                avg_val_deviation REAL,
                load_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(scheme_code, date)
            )
        `);

        console.log('Fact table initialized. migrating data...');

        // Join staging fund data with staging index data
        // For Milestone 2, we assume all funds map to 'NIFTY 50'
        db.run(`
            INSERT OR REPLACE INTO fact_fund_index (scheme_code, date, nav, index_close)
            SELECT 
                f.scheme_code,
                f.date,
                f.nav,
                i.close as index_close
            FROM stg_fund_data f
            LEFT JOIN stg_index_data i ON f.date = i.date AND i.index_name = 'NIFTY 50'
        `, (err) => {
            if (err) {
                console.error('Error during fact migration:', err.message);
            } else {
                console.log('Fact table data migration complete.');
                db.all('SELECT COUNT(*) as count FROM fact_fund_index', (err, rows) => {
                    if (!err) console.log(`Total fact records: ${rows[0].count}`);
                    db.close();
                });
            }
        });
    });
}

loadFactData();
