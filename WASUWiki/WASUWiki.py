import jwt
import datetime
from flask import Flask, redirect, session, render_template, request

# Initialize the Flask application
app                 = Flask(__name__)

# Secret key for session management
app.secret_key      = '0a86d121-f01f-4524-a922-c86138e4f88a'

# Secret key for JWT encoding/decoding
JWT_SECRET          = 'your_jwt_secret'


@app.route('/')
def home():
    # Retrieve the token from the session
    token           = session.get('token')
    if token:
        try:
            # Decode the JWT token
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            # Render the home page with the user's information
            return render_template('WASUWiki-home.html', user=payload['user'])
        except jwt.ExpiredSignatureError:
            # Redirect to login if the token has expired
            return redirect('http://127.0.0.1:5000/login?next=' + request.url)
        except jwt.InvalidTokenError:
            # Redirect to login if the token is invalid
            return redirect('http://127.0.0.1:5000/login?next=' + request.url)

    # Redirect to login if no token is found
    return redirect('http://127.0.0.1:5000/login?next=' + request.url)


if __name__ == '__main__':
    # Run the Flask application on port 5001
    app.run(port=5001)
