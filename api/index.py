from flask import Flask, render_template, request
import psycopg2
import os
from dotenv import load_dotenv

# Initialize the Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()

# Function to create a database connection
def get_db_connection():
    # Use the POSTGRES_URL environment variable for the connection string
    conn = psycopg2.connect(os.environ.get('POSTGRES_URL'))
    conn.autocommit = True  # Enable autocommit
    return conn

# Function to initialize the database
def initialize_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Create the 'request' table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS request (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                request TEXT NOT NULL
            );
        ''')
        cursor.close()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"An error occurred while initializing the database: {e}")

# Call initialize_db() when the app starts
initialize_db()

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

    try:
        # Insert the form data into the 'request' table
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO request (name, email, request) VALUES (%s, %s, %s)',
            (name, email, prayer_request)
        )
        cursor.close()
        conn.close()
        return render_template('confirmation.html', name=name)
    except Exception as e:
        print(f"An error occurred while submitting the request: {e}")
        return "An error occurred. Please try again later.", 500

if __name__ == '__main__':
    app.run(debug=True)
