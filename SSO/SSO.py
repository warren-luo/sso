import jwt
import datetime
from flask import Flask, request, redirect, url_for, session, render_template

# Initialize the Flask application
app                          = Flask(__name__)

# Secret key for session management
app.secret_key               = '0a86d121-f01f-4524-a922-c86138e4f88a'

# Secret key for JWT encoding/decoding
JWT_SECRET                   = 'your_jwt_secret'

# Dummy user data for authentication
users                        = {'user1': 'password1'}


@app.route('/')
def home():
    # Retrieve the token from the session
    token                    = session.get('token')
    if token:
        try:
            # Decode the JWT token
            payload          = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            # Render the home page with the user's information
            return render_template('SSO-home.html', user=payload['user'])
        except jwt.ExpiredSignatureError:
            # Redirect to login if the token has expired
            return redirect(url_for('login'))
        except jwt.InvalidTokenError:
            # Redirect to login if the token is invalid
            return redirect(url_for('login'))

    # Render the home page without user information if no token is found
    return render_template('SSO-home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # Get username and password from the form
        username             = request.form['username']
        password             = request.form['password']
        # Check if the username and password match
        if username in users and users[username] == password:
            # Create a JWT token with user information and expiration time
            token            = jwt.encode({
                'user': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, JWT_SECRET, algorithm="HS256")
            # Store the token in the session
            session['token'] = token
            # Redirect to the next page or home page
            next_url = request.args.get('next') or url_for('home')
            return redirect(f"{next_url}?token={token}")

    # Render the login page
    return render_template('login.html')


@app.route('/logout')
def logout():
    # Remove the token from the session
    session.pop('token', None)
    # Redirect to the home page
    return redirect(url_for('home'))


if __name__ == '__main__':
    # Run the Flask application on port 5000
    app.run(port=5000)
