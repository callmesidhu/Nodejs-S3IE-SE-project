const express = require('express');
const path = require('path');
const { google } = require('googleapis');

// Load your service account credentials from the JSON file
const SERVICE_ACCOUNT_FILE = 'configs/credentials.json';
const SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly'];

// Create a JWT client
const auth = new google.auth.GoogleAuth({
    keyFile: SERVICE_ACCOUNT_FILE,
    scopes: SCOPES,
});

// Create a Google Sheets API client
const sheets = google.sheets({ version: 'v4', auth });

const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Define a route to render the HTML page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Define the /data route to fetch data from Google Sheets
app.get('/data', async (req, res) => {
    const SPREADSHEET_ID = '1lsquKezsrlneVMZe_KQW9ExlBr8hO_LhkSkMSlicv_U'; // Your Spreadsheet ID
    const RANGE = 'Sheet1'; // This will read the entire sheet

    try {
        const response = await sheets.spreadsheets.values.get({
            spreadsheetId: SPREADSHEET_ID,
            range: RANGE,
        });

        const rows = response.data.values;

        if (rows.length) {
            // Send the rows as a JSON response
            res.json(rows);
        } else {
            res.status(404).send('No data found.');
        }
    } catch (error) {
        console.error('Error reading data from spreadsheet:', error);
        res.status(500).send('Error retrieving data from spreadsheet.');
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
