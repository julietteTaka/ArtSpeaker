import logging
import config
import requests
import json
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


@config.g_app.route('/login/google')
def login():
    log = config.google.authorize(callback=url_for('authorized', _external=True))
    return log

@config.g_app.route('/login')
def loginPage():
    return render_template("login.html")

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
    return render_template("index.html")

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

# --------- OFFERS  ---------

@config.g_app.route('/offers', methods=['GET'])
def allOffers():
    offers = requests.get(config.serverRootUri+"/offer")

    if 'google_token' in session:
        user = config.google.get('userinfo').data
        return render_template("offers.html", user=user, offers=offers.json())
    return render_template("offers.html", offers=offers.json())

@config.g_app.route('/user/<userId>/offers', methods=['GET'])
def userOffers(userId):
    offers = requests.get(config.serverRootUri+"/user/"+userId+"/offer")

    if 'google_token' in session:
        user = config.google.get('userinfo').data
        return render_template("myOffers.html", user=user, offers=offers.json())
    return render_template("index.html")

@config.g_app.route('/offer', methods=['POST'])
def newOffer():
    header = {'content-type' : 'application/json'}
    logging.error(request.data)
    result = requests.post(config.serverRootUri + '/offer', data=request.data, headers=header)
    if result.status_code != 200:
        abort(result.status_code,  {'message': 'il y a eu une erreur lors de la soumission de votre formulaire.'})
    logging.error(result.json())
    return jsonify(**result.json())

@config.g_app.route('/offer/<offerID>', methods=['DELETE'])
def deleteOffer(offerID):
    result = requests.delete(config.serverRootUri + '/offer/' + offerID)
    if result.status_code != 200:
        abort(result.status_code,  {'message': 'il y a eu une erreur lors la suppression de l\'offre.'})
    return jsonify(**result.json())

@config.g_app.route('/offer/<offerID>', methods=['GET'])
def getOfferById(offerID):
    result = requests.get(config.serverRootUri + '/offer/' + offerID)
    if result.status_code != 200:
        abort(result.status_code,  {'message': 'can\'t retrieve offer '+offerID})
    if result is None:
        return render_template("index.html") # toDo page erreur
    return jsonify(**result.json())

@config.g_app.route('/offer/<offerId>/step/<step>', methods=['POST'])
def completeOffer(offerId, step):
    header = {'content-type' : 'application/json'}
    logging.error(request.data)
    result = requests.post(config.serverRootUri + '/offer/'+offerId+'/step/'+step, data=request.data, headers=header)
    if result.status_code != 200:
        abort(result.status_code,  {'message': 'il y a eu une erreur lors de la soumission de votre formulaire.'})
    return jsonify(**result.json())

@config.g_app.route('/offer', methods=['GET'])
def offerCreationForm():
    if 'google_token' in session:
        user = config.google.get('userinfo').data
        return render_template("offerCreation.html", user=user) # toDo page erreur
    return render_template("index.html")  # toDo page erreur

@config.g_app.route('/offer/<offerId>/step/<step>', methods=['GET'])
def offerCreationFormStep2(offerId, step):
    if 'google_token' in session:
        user = config.google.get('userinfo').data
        result = requests.get(config.serverRootUri + '/offer/'+offerId)

        if result.status_code != 200:
            abort(result.status_code,  {'message': 'On dirait l\'offre '+offerId+' n\'existe plus...'})

        return render_template("offerCreation.html", user=user, offer=result.json(), step=step)
    return render_template("index.html") # toDo page erreur


@config.g_app.route('/user')
def userAccount():
    if 'google_token' in session:
        user = config.google.get('userinfo').data
        return render_template("userAccount.html", user=user)
    return render_template("index.html")

if __name__ == '__main__':
    config.g_app.run(host="0.0.0.0",port=config.clientPort,debug=True)