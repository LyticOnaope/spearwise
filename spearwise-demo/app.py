# app.py
from flask import Flask, request, render_template, redirect, url_for
import sqlite3, datetime, os

app = Flask(__name__)
DB = 'spearwise.db'

def init_db():
    if not os.path.exists(DB):
        conn = sqlite3.connect(DB)
        conn.execute('CREATE TABLE clicks (id INTEGER PRIMARY KEY, user TEXT, email TEXT, role TEXT, time TEXT, user_agent TEXT)')
        conn.commit()
        conn.close()

@app.route('/')
def index():
    return "Spearwise demo running. Use /send-demo to see sample email text."

@app.route('/send-demo')
def send_demo():
    # Example link - replace domain with your host when deployed
    link = url_for('track', _external=True) + '?u=onaope&e=onaope@example.com&role=engineer'
    body = f"Subject: Payroll Update\n\nHi Onaope,\nPlease review: {link}"
    return f"<pre>{body}</pre>"

@app.route('/track')
def track():
    user = request.args.get('u','unknown')
    email = request.args.get('e','unknown@example.com')
    role = request.args.get('role','staff')
    ua = request.headers.get('User-Agent','')
    conn = sqlite3.connect(DB)
    conn.execute('INSERT INTO clicks (user,email,role,time,user_agent) VALUES (?,?,?,?,?)',
                 (user,email,role,datetime.datetime.utcnow().isoformat(),ua))
    conn.commit()
    conn.close()
    return render_template('lesson.html', user=user, role=role)

@app.route('/admin')
def admin():
    conn = sqlite3.connect(DB)
    rows = conn.execute('SELECT user,email,role,time FROM clicks ORDER BY time DESC').fetchall()
    conn.close()
    return render_template('admin.html', rows=rows)

@app.route('/complete-quiz', methods=['POST'])
def complete_quiz():
    # simple placeholder — you can expand this later
    return "<p>Thanks for completing the quick quiz — more tips sent to your inbox (demo).</p>"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
