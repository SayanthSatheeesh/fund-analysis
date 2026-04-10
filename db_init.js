const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const dbPath = path.resolve(__dirname, 'data/fund_index.db');
const db = new sqlite3.Database(dbPath);

db.serialize(() => {
  db.run('CREATE TABLE IF NOT EXISTS stg_index_data (id INTEGER PRIMARY KEY AUTOINCREMENT, index_name TEXT NOT NULL, date TEXT NOT NULL, open REAL, high REAL, low REAL, close REAL, volume INTEGER, load_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, UNIQUE(index_name, date))');
  db.run('CREATE TABLE IF NOT EXISTS stg_fund_data (id INTEGER PRIMARY KEY AUTOINCREMENT, scheme_code TEXT NOT NULL, scheme_name TEXT, nav REAL NOT NULL, date TEXT NOT NULL, load_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, UNIQUE(scheme_code, date))');
  console.log('Database initialized at:', dbPath);
});

db.close();
