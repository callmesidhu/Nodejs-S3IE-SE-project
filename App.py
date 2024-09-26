from flask import Flask, render_template, request

app = Flask(__name__)

# Route for rendering the form
@app.route('/')
def home():
    return render_template('index.html')  # Ensure you have form.html in the templates folder

# Route for handling form submission
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    return f"Thank you, {name}. We have received your email: {email}"

if __name__ == '__main__':
    app.run(debug=True)
