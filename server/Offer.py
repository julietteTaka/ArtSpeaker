class Offer(object):
    def __init__(self, offerId, userId, projectTitle):

        # first step data
        self.userId = userId
        self.offerId = offerId

        self.title = projectTitle
        self.fieldActivity = None
        self.place = ""
        self.enterpriseLogo = None
        self.networking = []
        self.projectDate = {}

        self.isOpen = False
        self.isComplete = False


        # second step data
        self.offerDate = {}
        self.wantedProfiles = []
        self.text = ""
        self.tags = []
        self.sector = []
        self.contact = {}

        # not sure
        self.remuneration = None
        self.workType = ""
        self.artists = []
