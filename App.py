from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()  # Load environment variables from .env file

# Configure database connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
  # Update this with your credentials
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a model for your form data
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(100))

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
    


    # Create a new User instance
    new_user = User(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        company=company
    )
    
    # Add the user to the session and commit to the database
    db.session.add(new_user)
    db.session.commit()
    
    # Return a thank you message
    return "Thank you for your response"

if __name__ == '__main__':
    # Create the database and tables if they don't exist
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
