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

async function startNormalization() {
    console.log('Fetching all fund records for date normalization...');
    
    db.all('SELECT id, date FROM stg_fund_data', (err, rows) => {
        if (err) return console.error(err);

        console.log(`Normalizing ${rows.length} records...`);
        
        db.serialize(() => {
            db.run('BEGIN TRANSACTION');
            const stmt = db.prepare('UPDATE stg_fund_data SET date = ? WHERE id = ?');

            for (const row of rows) {
                const normDate = normalizeAMFIDate(row.date);
                if (normDate !== row.date) {
                    stmt.run(normDate, row.id);
                }
            }

            stmt.finalize();
            db.run('COMMIT', (err) => {
                if (err) {
                    console.error('Error committing normalization:', err);
                } else {
                    console.log('Staging table dates normalized successfully.');
                    db.close();
                }
            });
        });
    });
}

startNormalization();
