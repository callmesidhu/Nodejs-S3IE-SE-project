from flask import Flask, render_template, request

app = Flask(__name__)

# Route for rendering the form
@app.route('/')
def home():
    return render_template('index.html')  # Render the form from index.html

# Route for handling form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    email = request.form['floating_email']
    password = request.form['floating_password']
    confirm_password = request.form['repeat_password']
    first_name = request.form['floating_first_name']
    last_name = request.form['floating_last_name']
    phone = request.form['floating_phone']
    company = request.form['floating_company']
    
    # Here you can add logic to handle the data (e.g., save to database)
    
    # Check if passwords match
    if password != confirm_password:
        return "Passwords do not match!", 400
    
    # Return a thank you message
    return f"Thank you, {first_name} {last_name}. We have received your submission with email: {email} and phone: {phone}."

if __name__ == '__main__':
    app.run(debug=True)
