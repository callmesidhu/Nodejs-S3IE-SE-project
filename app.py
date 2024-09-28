from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()# load environment variable

# Set the secret key for session management
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

# Set up the Google Sheets API
SERVICE_ACCOUNT_FILE = os.environ.get('CONFIG_PATH')  # Path to your service account JSON file
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Create credentials using the service account
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Sheets API service
service = build('sheets', 'v4', credentials=credentials)

# Google Sheets ID and range
SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID') 
RANGE_NAME = 'Sheet1'  # The sheet name or range to access

@app.route('/')
def index():
    # Render the main page
    return render_template('index.html')

# READ (CRUD)
@app.route('/data', methods=['GET'])
def get_data():
    # Call the Sheets API to get data
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        return jsonify({'message': 'No data found.'}), 404

    return jsonify(values)

# CREATE (CRUD) - Write data to Google Sheets
def write_to_google_sheet(data):
    # Define the sheet range where you want to add data
    body = {'values': [data]}  # Data needs to be in a list of lists
    
    # Append the data to the sheet
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
        valueInputOption="RAW", body=body).execute()

    return result

@app.route('/submit', methods=['POST'])
def submit():
    # Extract data from the form
    email = request.form['floating_email']
    password = request.form['floating_password']
    repeat_password = request.form['repeat_password']
    first_name = request.form['floating_first_name']
    last_name = request.form['floating_last_name']
    phone = request.form['floating_phone']
    company = request.form['floating_company']

    # Prepare data to write to Google Sheets
    data = [email, password, repeat_password, first_name, last_name, phone, company]
    
    # Write data to Google Sheets
    result = write_to_google_sheet(data)

    # Flash a success message to the user
    flash('Form submitted successfully!')
    return '<h1>Thank you for your response</h1>'
    

if __name__ == '__main__':
    app.run(debug=True)
