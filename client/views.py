import logging
import config
from functools import wraps
from flask import (
    request,
    jsonify,
    render_template,
    abort,
    redirect,
    url_for,
    session
)


# --------- LOGIN  ---------


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'google_token' in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@config.g_app.route('/login')
def login():
    log = config.google.authorize(callback=url_for('authorized', _external=True))
    return log

@config.g_app.route('/login/authorized')
def authorized():
    resp = config.google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')

    redirectTarget = request.values.get('next') or request.referrer or url_for('index')
    if redirectTarget == None:
        logging.warning('login/authorized redirectTarget is None')

    log = redirect( redirectTarget )
    return log

@config.g_app.route('/logout')
def logout():
    session.pop('google_token', None)
    redirectTarget = request.values.get('next') or request.referrer
    return redirect( redirectTarget )

@config.google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

# --------- INDEX  ---------

@config.g_app.route('/')
def index():
    if 'google_token' in session:
        user = config.google.get('userinfo').data
        return render_template("index.html", user=user)
    return render_template("index.html")


if __name__ == '__main__':
    config.g_app.run(host="0.0.0.0",port=config.clientPort,debug=True)