class User(object):
    def __init__(self, userId, mdp, userName):
        self.id = userId
        self.mdp = mdp
        self.userName = userName
        self.isActive = False