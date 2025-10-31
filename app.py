from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime
import sqlite3, os

DB_PATH = os.environ.get('DB_PATH', 'clicks.db')
app = Flask(__name__)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS clicks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    referrer TEXT,
                    user_agent TEXT,
                    timestamp TEXT NOT NULL
                );''')
    conn.commit(); conn.close()

init_db()

@app.route('/')
def index():
    urls = [
        {'id': 'google', 'label': 'Google', 'target': 'https://www.google.com'},
        {'id': 'github', 'label': 'GitHub', 'target': 'https://github.com'}
    ]
    return render_template('index.html', urls=urls)

@app.route('/t/<link_id>')
def track(link_id):
    mapping = {'google': 'https://www.google.com', 'github': 'https://github.com'}
    target = mapping.get(link_id, 'https://google.com')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO clicks (url, referrer, user_agent, timestamp) VALUES (?, ?, ?, ?)', (
        link_id, request.referrer, request.headers.get('User-Agent'), datetime.utcnow().isoformat()
    ))
    conn.commit(); conn.close()
    return redirect(target)

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT url, COUNT(*) as cnt FROM clicks GROUP BY url')
    rows = c.fetchall()
    conn.close()
    stats = {r[0]: r[1] for r in rows}
    return render_template('dashboard.html', stats=stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
