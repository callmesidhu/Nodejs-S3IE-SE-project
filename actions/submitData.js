const { google } = require('googleapis');
const path = require('path');

// Google Sheets configuration
const SPREADSHEET_ID = '1lsquKezsrlneVMZe_KQW9ExlBr8hO_LhkSkMSlicv_U';
const SERVICE_ACCOUNT_FILE = path.join(__dirname, 'configs', 'service-account.json');

// Load the service account credentials
const auth = new google.auth.GoogleAuth({
    keyFile: SERVICE_ACCOUNT_FILE,
    scopes: ['https://www.googleapis.com/auth/spreadsheets']
});

// Function to append data to Google Sheets
async function appendToSheet(data) {
    const sheets = google.sheets({ version: 'v4', auth: await auth.getClient() });
    
    // Prepare the request body with the form data
    const request = {
        spreadsheetId: SPREADSHEET_ID,
        range: 'Sheet1',  // Adjust range to match your sheet
        valueInputOption: 'RAW',
        insertDataOption: 'INSERT_ROWS',
        resource: {
            values: [
                [data.name, data.email]  // Adjust columns according to your form fields
            ]
        }
    };

    try {
        await sheets.spreadsheets.values.append(request);
        console.log('Data added to Google Sheets');
    } catch (err) {
        console.error('Error appending data:', err);
        throw err;
    }
}

// Export the function to be used in index.js
module.exports = {
    appendToSheet
};
