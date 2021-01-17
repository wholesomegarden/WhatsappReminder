#ServiceLoader.py
from API import *

from EchoService import *
from DanilatorService import *
from ReminderService import *
from MusicService import *

from threading import Thread


class ServiceLoader(object):
    def LoadServices(send, backup, genLink, list = ["Echo", "Danilator", "Reminders", "Music"]):
        services = {}
        for service in list:
            services[service] = ServiceLoader.LoadService(service, send, backup, genLink)
        return services

    def LoadService(service, send, backup, genLink):
        # Load Dynamicly
        # api = API(service, send, backup, genLink)
        foundServiceClass = None
        if service is "Echo":
            foundServiceClass = EchoService
        if service is "Reminders":
            foundServiceClass = ReminderService
        if service is "Danilator":
            foundServiceClass = DanilatorService
        if service is "Music":
            foundServiceClass = MusicService

        if foundServiceClass is not None:
            api = API(service, send, backup, genLink)
            ServiceLoader.startService(foundServiceClass, db={}, api=api)
            return {"obj": foundServiceClass.share, "api":api}


        return None

    def startService(service_class, db = None, api = None):
        serviceThread = Thread(target = ServiceLoader.startServiceAsync, args = [[service_class, db, api]])
        serviceThread.start()

    def startServiceAsync(data):
        service_class, db, api = data
        service_class(db, api).go()
