# Reminder.py
## check language
## commands
## repeats

class Reminder():

    id = -1
    userID = -1
    message = "__"
    sendTime = None
    sent = False
    repeat = False
    hasTime = False

    def __init__(self, remID, userID, msg, t):
        self.id          = remID
        self.userID      = userID
        self.message     = msg
        self.sendTime    = t
        self.repeat      = False
        self.hasTime     = t is not None

        print("NEW REMINDER CREATED!",self,self.id         ,
self.userID     ,
self.message    ,
self.sendTime   ,
self.repeat     ,
self.hasTime    ,'\n')
