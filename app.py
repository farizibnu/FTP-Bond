from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Dummy user data
users = {'username': 'password'}

@app.route('/')
def result():
    if 'username' in session:
        return render_template('result.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            # Successful login, set session and redirect to result page
            session['username'] = username
            return redirect(url_for('result'))
        else:
            # Failed login, redirect back to login page
            return redirect(url_for('login'))
    # Render the login page template
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
