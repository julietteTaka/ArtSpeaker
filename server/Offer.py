class Offer(object):
    def __init__(self, offerId, userId):

        # first step data
        self.userId = userId
        self.offerId = offerId

        self.projectTitle = ""
        self.fieldActivity = None
        self.place = ""
        self.enterpriseLogo = None
        self.networking = []
        self.projectDate = {}
        self.contact = {}
        self.isOpen = False
        self.isComplete = False

        # second step data
        self.offerTitle = ""
        self.offerDate = {}
        self.wantedProfiles = ""
        self.text = ""

        # not sure
        self.remuneration = None
        self.workType = ""
        self.artists = []
