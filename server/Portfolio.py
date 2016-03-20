class Portfolio(object):
    def __init__(self, portfolioId, userId):
        self.userId = userId
        self.portfolioId = portfolioId
        # first step
        self.pseudo = ""
        self.place = ""
        self.fieldOfActivity = None
        self.profilePicture = None
        self.availability = {}

        # second step
        self.contact = {}
        self.galery = []
        self.tags = []
        self.networking = []
        self.artistLogo = None
        self.coverPicture = {
            'id':'',
            'path':'',
            'mimetype':''
        }