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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'google_token' in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@config.g_app.route('/')
def index():
    if 'google_token' in session:
        user = config.google.get('userinfo').data
        return render_template("index.html", user=user)
    return render_template("index.html")


if __name__ == '__main__':
    config.g_app.run(host="0.0.0.0",port=config.clientPort,debug=True)