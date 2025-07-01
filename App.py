from flask import Flask, request, render_template_string, redirect, url_for, session
import pickle
import pandas as pd
from feature_extractor import extract_features_from_url

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# In-memory user store (for demo; use a database in production)
users = {}

# Load your trained model and feature columns
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('feature_columns.pkl', 'rb') as f:
    feature_columns = pickle.load(f)
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']  password = request.form['password']
        if username in users:
            error = 'Username already exists'
        else:
            users[username] = password
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('home'))
    return render_template_string(REGISTER_TEMPLATE, error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = 'Invalid credentials'
    return render_template_string(LOGIN_TEMPLATE, error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    result = None
    if request.method == 'POST':
        url = request.form['url']
        features = pd.DataFrame([extract_features_from_url(url)])
        features = features.reindex(columns=feature_columns, fill_value=0)
        prediction = model.predict(features)[0]
        result = "Phishing" if prediction == 1 else "Legitimate"
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    app.run(debug=True)

feature_extractor.py
import re
from urllib.parse import urlparse

def extract_features_from_url(url):
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    path = parsed.path
    query = parsed.query

    return {
        'url_length': len(url),
        'domain_length': len(domain),
        'path_length': len(path),
        'query_length': len(query),
        'num_dots': url.count('.'),
        'num_hyphens': url.count('-'),
        'num_slashes': url.count('/'),
        'num_subdomains': len(domain.split('.')) - 1,
        'has_at': int('@' in url),
        'has_ip': int(bool(re.match(r'(http[s]?://)?(\d{1,3}\.){3}\d{1,3}', url))),
        'https': int(url.lower().startswith('https')),
        'has_port_in_url': int(':' in parsed.netloc),
        'has_double_slash_redirect': int('//' in path.strip('/')),
        'has_suspicious_words': int(any(word in url.lower() for word in ['login', 'verify', 'bank', 'update', 'secure']))
    }
