const { google } = require('googleapis');

const SERVICE_ACCOUNT_FILE = 'configs/credentials.json';
const SCOPES = ['https://www.googleapis.com/auth/spreadsheets'];

const auth = new google.auth.GoogleAuth({
    keyFile: SERVICE_ACCOUNT_FILE,
    scopes: SCOPES,
});


const sheets = google.sheets({ version: 'v4', auth });

async function fetchSpreadsheetData(spreadsheetId, range) {
    try {
        const response = await sheets.spreadsheets.values.get({
            spreadsheetId,
            range,
        });
        const rows = response.data.values;
        return rows; 
    } catch (error) {
        console.error('Error reading data from spreadsheet:', error);
        throw error; 
    }
}


function fetchData(app) {
    app.get('/data', async (req, res) => {
        const SPREADSHEET_ID = '1lsquKezsrlneVMZe_KQW9ExlBr8hO_LhkSkMSlicv_U'; 
        const RANGE = 'Sheet1'; // This will read the entire sheet

        try {
            const rows = await fetchSpreadsheetData(SPREADSHEET_ID, RANGE);

            if (rows.length) {
                // Send the rows as a JSON response
                res.json(rows);
            } else {
                res.status(404).send('No data found.');
            }
        } catch (error) {
            res.status(500).send('Error retrieving data from spreadsheet.');
        }
    });
}

module.exports = { fetchSpreadsheetData, fetchData }; 
