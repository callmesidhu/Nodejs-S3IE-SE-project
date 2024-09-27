from flask import Flask, render_template, request, redirect, url_for, jsonify
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

app = Flask(__name__)

# Set up the Google Sheets API
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Update with your JSON file path
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Create credentials using the service account
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Sheets API service
service = build('sheets', 'v4', credentials=credentials)

# Replace with your Google Sheets ID and range
SPREADSHEET_ID = '1lsquKezsrlneVMZe_KQW9ExlBr8hO_LhkSkMSlicv_U'  # Your spreadsheet ID

 # Update with your spreadsheet ID
RANGE_NAME = 'Sheet1'  # Accesses all data in the sheet


@app.route('/data', methods=['GET'])
def get_data():
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        return jsonify({'message': 'No data found.'}), 404

    return jsonify(values)





















@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['floating_email']
    password = request.form['floating_password']
    repeat_password = request.form['repeat_password']
    first_name = request.form['floating_first_name']
    last_name = request.form['floating_last_name']
    phone = request.form['floating_phone']
    company = request.form['floating_company']

    # Here you can handle the form data, e.g., store it in a database, validate input, etc.
    # For now, just printing the values
    print(f"Email: {email}")
    print(f"Password: {password}")
    print(f"Repeat Password: {repeat_password}")
    print(f"First Name: {first_name}")
    print(f"Last Name: {last_name}")
    print(f"Phone: {phone}")
    print(f"Company: {company}")

    # Redirect to a success or confirmation page (optional)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
