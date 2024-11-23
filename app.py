from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Route to display the form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/submit_request', methods=['POST'])
def submit_request():
    name = request.form['name']
    email = request.form['email']
    prayer_request = request.form['request']

    # Connect to the SQLite database
    conn = sqlite3.connect('db.sqlite3')  # Replace with your database file
    cursor = conn.cursor()

    # Insert the form data into the 'request' table
    cursor.execute('INSERT INTO request (name, email, request) VALUES (?, ?, ?)',
                   (name, email, prayer_request))
    conn.commit()
    conn.close()

    return render_template('confirmation.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
