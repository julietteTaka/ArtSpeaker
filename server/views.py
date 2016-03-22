import logging
import config
import json
import math
import shutil, os

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

@config.g_app.route("/offer/<offerId>/step/<int:step>", methods=["POST"])
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
                        "offerDate" : {"begin" : offerDate['begin'], "end" : offerDate['end']},
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
                        "projectDate" : {"begin" : projectDate['begin'], "end" : projectDate['end']},
                        "contact" : {"name" : contact['name'], "phone" : contact['phone'], "mail" : contact['mail']},
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

@config.g_app.route('/offer/<offerId>/liked', methods=['POST'])
def likeOffer(offerId):
    userId = request.get_json().get('userId', None)
    config.offerTable.update_one(
            {"offerId": offerId},
            {"$set":{ "likedBy" : {"userId" : userId } }})
    updateResult = config.offerTable.find_one({"offerId": offerId})
    return mongodoc_jsonify(updateResult)

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

    portfolioPath = os.path.join(config.portfoliosDir, str(portfolioId))
    imagesPath = os.path.join(portfolioPath, str("images"))
    try:
        if not os.path.exists(portfolioPath):
            os.makedirs(portfolioPath)
            os.makedirs(imagesPath)
    except OSError:
        logging.error("can't create "+portfolioPath+" or "+imagesPath)
        pass

    portfolio = Portfolio(portfolioId, userId)
    # minimal requierements

    pseudo = request.get_json().get("pseudo", None)
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
    return mongodoc_jsonify(requestResult)

@config.g_app.route("/portfolio/<portfolioId>", methods=["GET"])
def getPortfolioById(portfolioId):
    offersLiked = config.offerTable.find()
    portfolio = config.portfolioTable.find_one({"portfolioId": portfolioId})
    return mongodoc_jsonify({"portfolio":portfolio, "offerLiked": [ result for result in offersLiked ]})

@config.g_app.route("/user/<userId>/portfolio", methods=["GET"])
def getPortfolioByUserId(userId):
    portfolio = config.portfolioTable.find_one({"userId": userId})
    offersLiked = config.offerTable.find()
    logging.error(offersLiked)
    return mongodoc_jsonify({"portfolio":portfolio, "offerLiked": [ result for result in offersLiked ]})

@config.g_app.route("/portfolios/number/<number>/page/<page>", methods=["GET"])
def getPortfolioGroup(number, page):
    if number:
        number = int(number)
    if page:
        page = int(page)

    totalPortfolios = config.portfolioTable.count()
    totalPages = int(math.ceil(totalPortfolios / number)+1)
    portfolios = config.portfolioTable.find().limit(number).skip(page)

    return mongodoc_jsonify({"portfolios":[ result for result in portfolios ], "totalPortfolios":totalPortfolios, "page":page, "totalPages":totalPages})

@config.g_app.route("/portfolio/<portfolioId>", methods=["DELETE"])
def deletePortfolio(portfolioId):
    portfolioPath = os.path.join(config.portfoliosDir, str(portfolioId))

    try:
        shutil.rmtree(portfolioPath)
    except OSError:
        logging.error("Can't remove file "+portfolioPath)
        pass
    
    deletedPortfolio = config.portfolioTable.remove({"portfolioId": portfolioId})
    return mongodoc_jsonify(deletedPortfolio)

@config.g_app.route('/portfolio/<portfolioId>/cover', methods=['POST'])
def addCoverPicture(portfolioId):
    '''
    Upload a cover picture in the database and delete the old one
    '''

    portfolioPath = os.path.join(config.portfoliosDir, str(portfolioId))
    
    coverToBeReplaced = config.portfolioTable.find_one({ "portfolioId" : portfolioId}, {"coverPicture":1})
    
    if(coverToBeReplaced['coverPicture']['path']):
        os.remove(coverToBeReplaced['coverPicture']['path'])

    imgId = str(ObjectId())

    file = request.files['file']
    mimetype = request.files['file'].content_type
    imgPath = os.path.join(portfolioPath+"/images", str(imgId)+"."+mimetype.split('/')[1])

    fileName = str(imgId)+"."+mimetype.split('/')[1]
    file.save(imgPath)

    img = request.data
    config.portfolioTable.update_one(
            {"portfolioId": portfolioId},
            {"$set":{   "coverPicture.id" : str(imgId),
                        "coverPicture.mimetype" : mimetype,
                        "coverPicture.path" : imgPath,
                        }}
        )

    coverPicture = config.portfolioTable.find_one({ "coverPicture.id" : str(imgId)})
    return mongodoc_jsonify(coverPicture)

@config.g_app.route('/portfolio/<portfolioId>/galleryImage', methods=['POST'])
def addImageToGallery(portfolioId):
    '''
    Upload an image into the gallery
    '''

    portfolioPath = os.path.join(config.portfoliosDir, str(portfolioId))
    imgId = str(ObjectId())

    file = request.files['file']
    mimetype = request.files['file'].content_type
    imgPath = os.path.join(portfolioPath+"/images", str(imgId)+"."+mimetype.split('/')[1])

    fileName = str(imgId)+"."+mimetype.split('/')[1]
    file.save(imgPath)

    logging.error("name "+fileName)
    dbImg = {'image' :[{
                'id' : str(imgId),
                'mimetype' : mimetype,
                'path' : imgPath,
                }]
    }

    
    config.portfolioTable.update_one(
            {"portfolioId": portfolioId},
            {"$push":{"galery" : dbImg }}
        )

    resourceData = config.portfolioTable.find_one({ "galery.image.id":str(imgId)}, {"_id":0, "galery": {"$elemMatch":{"image.id":str(imgId)}}})

    return mongodoc_jsonify(resourceData)


@config.g_app.route('/portfolio/<portfolioId>/resource/<resourceId>/data/<dataType>', methods=['GET'])
def getResourceData(portfolioId, resourceId, dataType):
    '''
     Returns the resource.
    '''

    resourceData = None
    mimetype = None

    if dataType == "coverPicture":
        resourceData = config.portfolioTable.find_one({ "portfolioId" : portfolioId}, {"coverPicture":1})
        mimetype = resourceData['coverPicture']['mimetype']
    else:
        resourceData = config.portfolioTable.find_one({ "galery.image.id":resourceId}, {"_id":0, "galery": {"$elemMatch":{"image.id":resourceId}}})
        mimetype = resourceData['galery'][0]['image'][0]['mimetype']

    if not resourceData:
        abort(404)


    portfolioPath = os.path.join(config.portfoliosDir, str(portfolioId))
    filePath = os.path.join (portfolioPath+"/images", resourceId+"."+mimetype.split('/')[1])

    if not os.path.isfile(filePath):
        abort(404)

    resource = open(filePath)
    return Response(resource.read(), mimetype=mimetype)

def mongodoc_jsonify(*args, **kwargs):
    return Response(json.dumps(args[0], default=json_util.default), mimetype='application/json')

if __name__ == '__main__':
    config.g_app.run(host="0.0.0.0",port=config.serverPort,debug=True)