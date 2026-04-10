const cron = require('node-cron');
const { execSync } = require('child_process');
const path = require('path');

const scripts = [
    'amfi_searcher.js',
    'fetch_index_data.js',
    'normalize_all_dates.js',
    'load_fact_data.js',
    'calculate_kpis.js'
];

function runPipeline() {
    console.log(`[${new Date().toISOString()}] Starting daily pipeline...`);
    
    for (const script of scripts) {
        try {
            const scriptPath = path.join(__dirname, script);
            console.log(`Executing ${script}...`);
            const output = execSync(`node "${scriptPath}"`, { stdio: 'inherit' });
            console.log(`${script} completed successfully.`);
        } catch (err) {
            console.error(`Error executing ${script}:`, err.message);
            // Break loop if a critical step fails
            if (script === 'amfi_searcher.js' || script === 'load_fact_data.js') break;
        }
    }
    
    console.log(`[${new Date().toISOString()}] Pipeline execution finished.`);
}

// Schedule for 07:00 AM IST (Indian Standard Time)
// Since the server usually runs on UTC, 07:00 IST is 01:30 UTC
// Cron format: 'minute hour day-of-month month day-of-week'
cron.schedule('30 1 * * *', () => {
    runPipeline();
}, {
    scheduled: true,
    timezone: "Asia/Kolkata"
});

console.log('Automated Scheduler (M4) is running. Monitoring for 07:00 IST sync...');

// Export for manual trigger if needed
module.exports = { runPipeline };
