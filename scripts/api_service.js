const express = require('express');
const cors = require('cors');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const { exec } = require('child_process');
const scheduler = require('./scheduler');

const app = express();
const port = 3000;
const dbPath = path.resolve(__dirname, '../data/fund_index.db');

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../')));

// Endpoint 1: Get all Fund KPIs (Filtered by Category)
app.get('/api/funds', (req, res) => {
    const db = new sqlite3.Database(dbPath);
    const category = req.query.category;
    
    let query = `
        SELECT k.*, s.scheme_name, s.fund_category 
        FROM mart_fund_kpis k
        JOIN stg_fund_data s ON k.scheme_code = s.scheme_code
    `;
    
    let params = [];
    if (category) {
        query += ` WHERE s.fund_category LIKE ? `;
        params.push(`%${category}%`);
    }
    
    query += ` GROUP BY k.scheme_code ORDER BY k.avg_deviation DESC LIMIT 100`;

    db.all(query, params, (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json(rows);
    });
    db.close();
});

// Endpoint 2: Get time-series data for a specific fund vs index
app.get('/api/comparison/:code', (req, res) => {
    const db = new sqlite3.Database(dbPath);
    const query = `
        SELECT date, nav, index_close 
        FROM fact_fund_index 
        WHERE scheme_code = ? 
        ORDER BY date ASC
    `;
    db.all(query, [req.params.code], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json(rows);
    });
    db.close();
});

// Endpoint 3: Trigger Mart Recalculation
app.post('/api/refresh', (req, res) => {
    console.log('Triggering mart refresh...');
    const scriptPath = path.join(__dirname, 'calculate_kpis.js');
    exec(`node "${scriptPath}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).json({ success: false, error: error.message });
        }
        res.json({ success: true, message: 'Data Mart successfully recalculated.' });
    });
});

app.listen(port, () => {
    console.log(`API Service running at http://localhost:${port}`);
});
