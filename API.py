#api.py
class API(object):
    def __init__(self, service, send, backup):
        self.service = service
        self.sendFunc = send
        self.backupFunc = backup

    def send(self, target, content):
        return self.sendFunc(self, self.service, target, content)

    def backup(self, db):
        return self.backupFunc(api = self, db = db, service = self.service)
