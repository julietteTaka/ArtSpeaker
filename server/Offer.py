class Offer(object):
    def __init__(self, offerId, userId, projectTitle):
        '''
        define all datas in the offer table

        example for social {
            [{  network : "website",
                url : me.com}],
        }

        example for projectDate{
            "begin" : "01/02/2016",
            "end": "01/08/2016",
        }
        '''
        # first step data
        self.userId = userId
        self.offerId = offerId
        self.title = projectTitle
        self.activity = None
        self.enterpriseLogo = None
        self.place = ""
        self.remuneration = None
        self.workType = ""
        self.artists = []
        self.isOpen = False
        self.website = ""
        self.networking = []
        self.projectDate = {}
        self.offerDate = {}
        self.wantedProfiles = []
        # last step data
        self.text = ""
        self.tags = []
        self.sector = []
