import logging
import config
import json
import math

from bson import json_util, ObjectId
from flask import jsonify, Response, request, abort, make_response

from Offer import Offer
from Portfolio import Portfolio

@config.g_app.route("/")
def index():
    return "Artspeaker job offer and portfolio services."

# --------- OFFER  ---------

@config.g_app.route("/offer", methods=["POST"])
def createOffer():
    '''
    Create the offer
    '''

    offerId = str(ObjectId())
    userId = request.get_json().get("userId", None)

    if  offerId == None or userId == None:
        logging.error("The offer ID, the user ID or the project title is undefined")
        abort(make_response("The offer ID, the user ID is undefined", 500))

    offer = Offer(offerId, userId)

    # minimal requierements

    projectTitle = request.get_json().get("projectTitle", None)
    fieldActivity = request.get_json().get('fieldActivity', None)
    place = request.get_json().get('place', None)
    enterpriseLogo = request.get_json().get('entrepriseLogo', None)
    networking = request.get_json().get('networking', None)
    projectDate = request.get_json().get('projectDate', None)
    contact = request.get_json().get('contact', None)

    # Data

    if projectTitle is not None :
        offer.projectTitle = projectTitle
    if fieldActivity is not None :
        offer.fieldActivity = fieldActivity
    if place is not None :
        offer.place = place
    if enterpriseLogo is not None :
        offer.enterpriseLogo = enterpriseLogo
    if networking is not None :
        offer.networking = networking
    if projectDate is not None :
        offer.projectDate['begin'] = projectDate['begin']
        offer.projectDate['end'] = projectDate['end']
    if contact is not None :
        offer.contact['name'] = contact['name']
        offer.contact['phone'] = contact['phone']
        offer.contact['mail'] = contact['mail']

    config.offerTable.insert(offer.__dict__)
    requestResult = config.offerTable.find_one({"offerId": offerId})
    return mongodoc_jsonify(requestResult)

@config.g_app.route("/offer/<offerId>/step/<step>", methods=["POST"])
def offerStepTwo(offerId, step):
    offerTitle = request.get_json().get('offerTitle', None)
    offerDate = request.get_json().get('offerDate', None)
    wantedProfile = request.get_json().get('wantedProfile', None)
    text = request.get_json().get('text', None)

    if step == 2:
        config.offerTable.update_one(
            {"offerId": offerId},
            {"$set":{   "offerTitle":offerTitle,
                        "offerDate" : offerDate,
                        "wantedProfile" : wantedProfile,
                        "text": text, 
                        "offerDate['begin']" : offerDate['begin'],
                        "offerDate['end']" : offerDate['end'],
                        }}
        )

    if step == 1:
        projectTitle = request.get_json().get("projectTitle", None)
        fieldActivity = request.get_json().get('fieldActivity', None)
        place = request.get_json().get('place', None)
        enterpriseLogo = request.get_json().get('entrepriseLogo', None)
        networking = request.get_json().get('networking', None)
        projectDate = request.get_json().get('projectDate', None)
        contact = request.get_json().get('contact', None)

        config.offerTable.update_one(
            {"offerId": offerId},
            {"$set":{   "projectTitle":projectTitle,
                        "fieldActivity" : fieldActivity,
                        "place" : place,
                        "enterpriseLogo": enterpriseLogo, 
                        "projectDate['begin']" : projectDate['begin'],
                        "projectDate['end']" : projectDate['end'],
                        "contact[name]" : contact['name'],
                        "contact[phone]" : contact['phone'],
                        "contact[mail]" : contact['mail'],
                        }}
        )

    updateResult = config.offerTable.find_one({"offerId": offerId})
    return mongodoc_jsonify(updateResult)

@config.g_app.route("/offers", methods=["GET"])
def getOffers():
    offers = config.offerTable.find()
    return mongodoc_jsonify({"offers":[ result for result in offers ]})

@config.g_app.route("/offers/number/<number>/page/<page>", methods=["GET"])
def getOfferGroup(number, page):
    if number:
        number = int(number)
    if page:
        page = int(page)

    totalOffers = config.offerTable.count()
    totalPages = int(math.ceil(totalOffers / number)+1)
    offers = config.offerTable.find().limit(number).skip(page)

    return mongodoc_jsonify({"offers":[ result for result in offers ], "totalOffers":totalOffers, "page":page, "totalPages":totalPages})

@config.g_app.route("/user/<userId>/offer", methods=["GET"])
def getOffersFromUser(userId):
    offers = config.offerTable.find({"userId": userId})
    return mongodoc_jsonify({"offers":[ result for result in offers ]})

@config.g_app.route("/offer/<offerId>", methods=["DELETE"])
def deleteOffers(offerId):
    deletedOffer = config.offerTable.remove({"offerId": offerId})
    return mongodoc_jsonify(deletedOffer)

@config.g_app.route("/offer/<offerId>", methods=["GET"])
def getOfferById(offerId):
    offer = config.offerTable.find_one({"offerId": offerId})
    return mongodoc_jsonify(offer)


# --------- PORTFOLIO  ---------

@config.g_app.route("/portfolio", methods=["POST"])
def createPortfolio():
    '''
    Create the portfolio
    '''

    portfolioId = str(ObjectId())
    userId = request.get_json().get("userId", None)

    if  portfolioId == None or userId == None:
        logging.error("The portfolio ID or the user ID is undefined")
        abort(make_response("The portfolio ID, the user ID is undefined", 500))

    portfolio = Portfolio(portfolioId, userId)
    logging.error(portfolio)
    # minimal requierements

    pseudo = request.get_json().get("projectTitle", None)
    fieldActivity = request.get_json().get('fieldActivity', None)
    place = request.get_json().get('place', None)
    networking = request.get_json().get('networking', None)
    availability = request.get_json().get('availability', None)
    contact = request.get_json().get('contact', None)

    # Data

    if pseudo is not None :
        portfolio.pseudo = pseudo
    if fieldActivity is not None :
        portfolio.fieldActivity = fieldActivity
    if place is not None :
        portfolio.place = place
    if networking is not None :
        portfolio.networking = networking
    if availability is not None :
        portfolio.availability['begin'] = availability['begin']
        portfolio.availability['end'] = availability['end']
    if contact is not None :
        portfolio.contact['name'] = contact['name']
        portfolio.contact['phone'] = contact['phone']
        portfolio.contact['mail'] = contact['mail']

    config.portfolioTable.insert(portfolio.__dict__)
    requestResult = config.portfolioTable.find_one({"portfolioId": portfolioId})
    logging.error(requestResult)
    return mongodoc_jsonify(requestResult)

@config.g_app.route("/portfolio/<portfolioId>", methods=["GET"])
def getPortfolioById(portfolioId):
    portfolio = config.portfolioTable.find_one({"portfolioId": portfolioId})
    return mongodoc_jsonify(portfolio)

@config.g_app.route("/user/<userId>/portfolio", methods=["GET"])
def getPortfolioByUserId(userId):
    portfolio = config.portfolioTable.find_one({"userId": userId})
    return mongodoc_jsonify(portfolio)

@config.g_app.route("/portfolio/<oportfolioId>", methods=["DELETE"])
def deletePortfolio(portfolioId):
    deletedPortfolio = config.portfolioTable.remove({"portfolioId": portfolioId})
    return mongodoc_jsonify(deletedPortfolio)

def mongodoc_jsonify(*args, **kwargs):
    return Response(json.dumps(args[0], default=json_util.default), mimetype='application/json')

if __name__ == '__main__':
    config.g_app.run(host="0.0.0.0",port=config.serverPort,debug=True)