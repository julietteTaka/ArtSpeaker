import logging
import config
import json

from bson import json_util, ObjectId
from flask import jsonify, Response, request, abort, make_response

from Offer import Offer

@config.g_app.route("/")
def index():
    return "Artspeaker job offer and portfolio services."


@config.g_app.route("/offer", methods=["POST"])
def createOffer():
    '''
    Create the offer with minimal requierement.
    '''

    offerId = str(ObjectId())
    userId = request.get_json().get('userId', None)
    projectTitle = request.get_json().get('projectTitle', None)
    enterpriseLogo = request.get_json().get('entrepriseLogo', None)
    place = request.get_json().get('place', None)
    worktype = request.get_json().get('worktype', None)
    projectDate = request.get_json().get('projectDate', None)
    offerDate = request.get_json().get('offerDate', None)
    wantedProfiles = request.get_json().get('wantedProfiles', None)
    remuneration = request.get_json().get('remuneration', None)

    if  offerId == None or projectTitle == None or userId == None:
        logging.error("The offer ID, the user ID or the project title is undefined")
        abort(make_response("The offer ID, the user ID or the project title is undefined", 500))

    offer = Offer(offerId, userId, projectTitle)
    if remuneration is not None :
        offer.remuneration = remuneration
    if wantedProfiles is not None :
        offer.wantedProfiles = wantedProfiles
    if wantedProfiles is not None :
        offer.wantedProfiles = wantedProfiles
    if worktype is not None :
        offer.worktype = worktype
    if enterpriseLogo is not None :
        offer.enterpriseLogo = enterpriseLogo
    if projectDate is not None :
        offer.projectDate = projectDate
    if offerDate is not None :
        offer.offerDate = offerDate
    if place is not None :
        offer.place = place
    if social is not None :
        offer.social = social

    config.offerTable.insert(offer.__dict__)
    requestResult = config.offerTable.find_one({"offerId": offerId})

    return mongodoc_jsonify(requestResult)

@config.g_app.route("/offer/<offerId>/content")
def offerContent(offerId):
    
    text = request.get_json().get('text', None)
    title = request.get_json().get('title', None)
    sector = request.get_json().get('sector', None)
    tags = request.get_json().get('tags', None)

    config.offerTable.update_one(
        {"offerId": offerId},
        {"$set":{   "text": text, 
                    "title":title,
                    "sector":sector,
                    "tags":tags}}
    )

    return mongodoc_jsonify(requestResult)

@config.g_app.route("/offer", methods=["GET"])
def getOffers():
    offers = config.offerTable.find()
    return mongodoc_jsonify({"offers":[ result for result in offers ]})

def mongodoc_jsonify(*args, **kwargs):
    return Response(json.dumps(args[0], default=json_util.default), mimetype='application/json')

if __name__ == '__main__':
    config.g_app.run(host="0.0.0.0",port=config.serverPort,debug=True)