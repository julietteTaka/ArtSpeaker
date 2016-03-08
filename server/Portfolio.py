class Portfolio(object):
    def __init__(self, portfolioId, userId):
        self.userId = userId
        self.portfolioId = portfolioId
        # first step
        self.pseudo = ""
        self.place = ""
        self.fieldOfActivity = None
        self.networking = []
        self.profilePicture = None
        self.availability = {}
        self.coverPicture = {
            'id':'',
            'path':'',
            'mimetype':''
        }

        # second step
        self.contact = {}
        self.galery = []
        self.tags = []
