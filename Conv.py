# Conv.py

class Conv:
    userID = -1
    lastTurn = None
    ongoing = False
    fin = {"msg":None,"year":None,"month":None,"day":None,"hour":None,"minute":None}
    tries = 0
    human = []
    manager = []

    def __init__(self, userID):
        self.userID = userID
        self.lastTurn = None
        self.ongoing = False
        self.fin = {"msg":None,"year":None,"month":None,"day":None,"hour":None,"minute":None}
        self.tries = 0
        self.human_msg = []
        self.manager_msg = []

    def human(self, msg):
        self.human_msg.append(msg)
        self.lastTurn = "human"
        print("@ HUMAN:",msg)
        print()

    def manager(self,msg):
        self.manager_msg.append(msg)
        self.lastTurn = "manager"
        print("@ MANAGER:",msg)
        print()
