from flask import Flask, redirect, url_for, session
from requests_oauthlib import OAuth2Session

app = Flask(__name__)
app.secret_key = 'YOUR_SECRET_KEY'  # Replace with your actual secret key

# Dummy organization credentials
ORG_KEY = "dummy_org_key"
ORG_PASSWORD = "dummy_password"

# OAuth2 configuration
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
authorization_base_url = 'https://example.com/oauth/authorize'
token_url = 'https://example.com/oauth/token'
redirect_uri = 'http://localhost:5000/callback'

@app.route('/')
def home():
    return 'Welcome to the OAuth2 SSO Example'

@app.route('/login')
def login():
    # Create an OAuth2 session
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)
    authorization_url, state = oauth.authorization_url(authorization_base_url)

    # Save the state in the session for later use
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    # Retrieve the authorization response
    oauth = OAuth2Session(client_id, state=session['oauth_state'], redirect_uri=redirect_uri)
    token = oauth.fetch_token(token_url, authorization_response=request.url, client_secret=client_secret)

    # Store the token in the session
    session['oauth_token'] = token
    return 'Login successful!'

@app.route('/profile')
def profile():
    oauth = OAuth2Session(client_id, token=session['oauth_token'])
    user_info = oauth.get('https://example.com/api/userinfo').json()
    return f"User info: {user_info}"

if __name__ == '__main__':
    app.run(debug=True)
