const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const dbPath = path.resolve(__dirname, '../data/fund_index.db');
const db = new sqlite3.Database(dbPath);

async function calculateKPIs() {
    db.serialize(() => {
        // Create the KPI mart table
        db.run(`
            CREATE TABLE IF NOT EXISTS mart_fund_kpis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scheme_code TEXT NOT NULL,
                current_nav REAL,
                prev_nav_1m REAL,
                return_1m REAL,
                avg_deviation REAL,
                calculation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(scheme_code)
            )
        `);

        console.log('Calculating KPIs for all funds...');

        // For Milestone 2 (where we have 1 day of real fund data and 30 days of index):
        // We will simulate the "1 Month" lookback by using the current NAV 
        // and a random baseline, while calculating real deviation for the dates we have.
        
        // In a real production loop, we would window over the fact table.
        db.run(`
            INSERT OR REPLACE INTO mart_fund_kpis (scheme_code, current_nav, avg_deviation)
            SELECT 
                scheme_code,
                MAX(nav) as current_nav,
                AVG(nav - index_close) / AVG(index_close) * 100 as avg_deviation
            FROM fact_fund_index
            WHERE index_close IS NOT NULL
            GROUP BY scheme_code
        `, (err) => {
            if (err) {
                console.error('Error calculating metrics:', err.message);
            } else {
                console.log('KPI calculation complete.');
                db.all('SELECT COUNT(*) as count FROM mart_fund_kpis', (err, rows) => {
                    if (!err) console.log(`Total KPI records generated: ${rows[0].count}`);
                    db.close();
                });
            }
        });
    });
}

calculateKPIs();
