class Offer(object):
    def __init__(self, offerId, userId, title):
        '''
        define all datas in the offer table

        example for social [{
            twitter[{   
                icon:"/url.png",
                url:"/url"
            }]
        }]

        example for projectDate[{
            "begin" : "01/02/2016",
            "end": "01/08/2016",
        }
        '''
        # first step data
        self.userId = userId
        self.offerId = offerId
        self.title = title
        self.enterpriseLogo = None
        self.place = ""
        self.remuneration = None
        self.workType = ""
        self.tags = []
        self.artists = []
        self.isOpen = False
        self.website = ""
        self.social = []
        self.projectDate = []
        self.offerDate = []
        self.wantedProfiles = []
        # last step data
        self.text = ""
