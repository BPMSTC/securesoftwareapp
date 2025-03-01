from flask import Flask, request
import sqlite3

app = Flask(__name__)
app.config["DEBUG"] = True  # Debug mode enabled (vulnerable for production)

def init_db():
    """Initialize the SQLite database with a vulnerable user table."""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Create users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')
    # Insert a hardcoded user (hardcoded credentials are a vulnerability)
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
    conn.commit()
    conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    """A login endpoint that is vulnerable to SQL injection."""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Vulnerable raw SQL query (no parameterization)
        query = "SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(username, password)
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        if user:
            return "Logged in as: " + user[1]
        else:
            return "Invalid credentials", 401
    # Simple HTML login form
    return '''
        <form method="post">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

if __name__ == '__main__':
    init_db()
    app.run()
