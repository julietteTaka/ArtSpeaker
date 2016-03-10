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
    session,
    send_file,
    Response
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
    offers = requests.get(config.serverRootUri+"/offers/number/10/page/0")

    session.pop('google_token', None)
    redirectTarget = request.values.get('next') or request.referrer
    return render_template("index.html", offers=offers.json())

@config.google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

# --------- INDEX  ---------

@config.g_app.route('/')
def index():
    offers = requests.get(config.serverRootUri+"/offers/number/10/page/0")
    if 'google_token' in session:
        user = config.google.get('userinfo').data

        return render_template("index.html", user=user, offers=offers.json())
    return render_template("index.html", offers=offers.json())

# --------- OFFER  ---------

@config.g_app.route("/offers/number/<number>", methods=["GET"])
@config.g_app.route("/offers/number/<number>/page/<page>", methods=["GET"])
def allOffers(number,page=0):
    offers = requests.get(config.serverRootUri+"/offers/number/"+number+"/page/"+page)
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
    result = requests.post(config.serverRootUri + '/offer', data=request.data, headers=header)
    if result.status_code != 200:
        abort(result.status_code,  {'message': 'il y a eu une erreur lors de la soumission de votre formulaire.'})
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
    result = requests.post(config.serverRootUri + '/offer/'+offerId+'/step/'+step, data=request.data, headers=header)
    if result.status_code != 200:
        abort(result.status_code,  {'message': 'il y a eu une erreur lors de la soumission de votre formulaire.'})
    return jsonify(**result.json())

@config.g_app.route('/offer', methods=['GET'])
def offerCreationForm():
    if 'google_token' in session:
        user = config.google.get('userinfo').data
        return render_template("offerCreation.html", user=user, step="1") # toDo page erreur
    return render_template("index.html")  # toDo page erreur

@config.g_app.route('/offer/<offerId>/step/<step>', methods=['GET'])
def offerCreationFormStep2(offerId, step):
    if 'google_token' in session:
        user = config.google.get('userinfo').data
        result = requests.get(config.serverRootUri + '/offer/'+offerId)

        if result.status_code != 200:
            abort(result.status_code,  {'message': 'On dirait l\'offre '+offerId+' n\'existe plus...'})

        return render_template("offerCreation.html", user=user, offer=result.json(), step=step, edit=True)
    return render_template("index.html") # toDo page erreur


# --------- PORTFOLIO  ---------
@config.g_app.route('/user/<userId>/portfolio', methods=['GET'])
def editPortfolio(userId):
    if 'google_token' in session:
        user = config.google.get('userinfo').data
        portfolio = requests.get(config.serverRootUri+"/user/"+user['id']+"/portfolio")
        if portfolio.json() is not None:
            return render_template("myPortfolio.html", user=user, portfolio=portfolio.json())
        else:
            return render_template("portfolioCreation.html", user=user)
    return render_template("index.html")  # toDo page erreur

@config.g_app.route('/portfolio/<portfolioId>', methods=['GET'])
def displayPortfolioFrom(portfolioId):
    portfolio = requests.get(config.serverRootUri + '/portfolio/'+portfolioId)
    if 'google_token' in session:
        user = config.google.get('userinfo').data
        return render_template("myPortfolio.html", user=user, portoflio=portfolio.json())
    return render_template("myPortfolio.html", portoflio=portfolio.json())

@config.g_app.route('/portfolio', methods=['POST'])
def newPortfolio():
    header = {'content-type' : 'application/json'}
    result = requests.post(config.serverRootUri + '/portfolio', data=request.data, headers=header)
    if result.status_code != 200:
        abort(result.status_code,  {'message': 'il y a eu une erreur lors de la soumission de votre formulaire.'})
    return jsonify(**result.json())

@config.g_app.route('/portfolio/<portfolioId>', methods=['DELETE'])
def deletePortfolio(portfolioId):
    result = requests.delete(config.serverRootUri + '/portfolio/' + portfolioId)
    if result.status_code != 200:
        abort(result.status_code,  {'message': 'il y a eu une erreur lors la suppression du portfolio.'})
    return jsonify(**result.json())

@config.g_app.route("/user/<userId>/portfolio/<portfolioId>/cover", methods=['POST'])
def addCoverPicture(userId, portfolioId):
    filename = request.files['file'].filename
    file = request.files['file']
    file.save("/tmp/" + filename)
    mimetype = request.files['file'].content_type
    multiple_files = [('file', (filename, open("/tmp/" + filename, 'rb'), mimetype))]
    req = requests.post(config.serverRootUri + "/portfolio/"+portfolioId+"/cover", files=multiple_files)

    return jsonify(**req.json())

@config.g_app.route("/user/<userId>/portfolio/<portfolioId>/galleryImage", methods=['POST'])
def addImageToGallery(userId, portfolioId):
    filename = request.files['file'].filename
    file = request.files['file']
    file.save("/tmp/" + filename)
    mimetype = request.files['file'].content_type
    multiple_files = [('file', (filename, open("/tmp/" + filename, 'rb'), mimetype))]
    req = requests.post(config.serverRootUri + "/portfolio/"+portfolioId+"/galleryImage", files=multiple_files)
    return jsonify(**req.json())

@config.g_app.route("/portfolio/<portfolioId>/resource/<resourceId>", methods=['get'])
def getResource(portfolioId, resourceId):
    req = requests.get(config.serverRootUri + "/portfolio/"+portfolioId+"/resource/" + str(resourceId) + "/data")
    return Response(req.content, mimetype=req.headers["content-type"])

@config.g_app.route('/user')
def userAccount():
    if 'google_token' in session:
        user = config.google.get('userinfo').data
        return render_template("userAccount.html", user=user)
    return render_template("index.html")

if __name__ == '__main__':
    config.g_app.run(host="0.0.0.0",port=config.clientPort,debug=True)