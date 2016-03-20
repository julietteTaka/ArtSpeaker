import os
import ConfigParser
import logging
from flask import Flask
from flask_oauthlib.client import OAuth

APP_ROOT = os.path.dirname(os.path.abspath(__file__)) 

config =  ConfigParser.ConfigParser()
config.read(os.path.join(APP_ROOT, 'client.cfg'))

g_app = Flask(__name__)
g_app.config['GOOGLE_ID'] = config.get('OAUTH_CONFIG', 'googleId')
g_app.config['GOOGLE_SECRET'] = config.get('OAUTH_CONFIG', 'googleSecret')
clientPort = config.getint('APP_CLIENT', 'port')
g_app.debug = True
g_app.secret_key = config.get('APP_CLIENT', 'secretKey')

oauth = OAuth(g_app)

google = oauth.remote_app(
    'google',
    consumer_key=g_app.config.get('GOOGLE_ID'),
    consumer_secret=g_app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/userinfo.profile'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

def get_resource_as_string(name, charset='utf-8'):
    with g_app.open_resource(name) as f:
        return f.read().decode(charset)
        
g_app.jinja_env.globals['get_resource_as_string'] = get_resource_as_string

serverRootUri = config.get("APP_CLIENT", "serverRootUri")


