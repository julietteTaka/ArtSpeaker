class Offer(object):
    def __init__(self, userId):
        self.userId = userId
        self.title = ""
        self.text = ""
        self.enterprise = ""
        self.enterpriseLogo = None
        self.coordinate = []
        self.remuneration = None
        self.workType = ""
        self.tags = []
        self.artists = []
        self.isOpen = False