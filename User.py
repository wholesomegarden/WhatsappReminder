# User.py
from Conv import Conv

class User():
    id = -1
    isNumber = False
    prefs = {}
    reminders = {}
    remCount = 0
    conv = None
    lastRem = None

    def checkNum(id):
        return str.isnumeric(id)

    def __init__(self,id):
        id = str(id)
        number = User.checkNum(id)
        if number is not None:
            self.isNumber = True
        self.id = id
        self.prefs = {}
        self.reminders = {"sent":{},"unsent":{}}
        self.remCount = 0
        self.conv = Conv(id)
        self.lastRem = None


    def markSent(self, remID):
        if remID in self.reminders["unsent"]:
            self.reminders["sent"][remID] = self.reminders["unsent"].pop(remID)
            self.reminders["sent"][remID].sent = True
            ## check for repeat
            print("# REMINDER", remID," MARKED SENT!!!", self.reminders["sent"][remID])
            return True
        return False
