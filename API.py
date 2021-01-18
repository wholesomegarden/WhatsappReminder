#api.py
class API(object):
    def __init__(self, service, send, backup, newLink):
        self.service = service
        self.sendFunc = send
        self.backupFunc = backup
        self.newLink = newLink

    def send(self, target, content, thumnail = None):
        return self.sendFunc(self, self.service, target, content, thumnail = thumnail)

    def backup(self, db):
        return self.backupFunc(api = self, db = db, service = self.service)

    def genLink(self, chatID, answer, newLink = None):
        if newLink is None:
            return self.newLink(api = self,service = self.service, chatID = chatID, answer = answer)
        return self.newLink(api = self,service = self.service, chatID = chatID, answer = answer, newLink = newLink)
