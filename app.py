from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session
import os
import sqlite3
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)



if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

DATABASE = 'database.db'




def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    return conn

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with get_db_connection() as conn:
            try:
                query = "SELECT * FROM users WHERE username = ? AND password = ?"
                user = conn.execute(query, (username, password)).fetchone()
            except Exception as e: 
                print(f"Error occurred: {e}")
                user = None
            
            if user:
                session['admin_logged_in'] = True
                return redirect(url_for('admin'))
            else:
                flash('Invalid credentials, please try again.')
                return redirect(url_for('login'))


    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename:
                filename = file.filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                if os.path.exists(file_path):
                    base, extension = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(file_path):
                        filename = f"{base}_{counter}{extension}"
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        counter += 1

                file.save(file_path)
                flash(f'File successfully uploaded as {filename}')

    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('admin.html', files=files)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
        flash(f'File "{filename}" successfully deleted')
    else:
        flash(f'File "{filename}" not found')

    return redirect(url_for('admin'))

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
