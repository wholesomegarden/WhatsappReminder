#ServiceLoader.py
from API import *

from EchoService import *
from DanilatorService import *
from ReminderService import *
from MusicService import *
from MasterService import *
from ExperimentalService import *

from threading import Thread


class ServiceLoader(object):
    def LoadServices(send, backup, genLink, list = ["Master","Echo", "Danilator", "Reminders", "Music", "Experimental"], master = None):
        services = {}
        for service in list:
            if service is "Master" or service is "Experimental":
                services[service] = ServiceLoader.LoadService(service, send, backup, genLink, master = master)
            else:
                services[service] = ServiceLoader.LoadService(service, send, backup, genLink)
        return services

    def LoadService(service, send, backup, genLink, master = None):
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
        if service is "Master":
            foundServiceClass = MasterService
        if service is "Experimental":
            foundServiceClass = ExperimentalService

        if foundServiceClass is not None:
            api = API(service, send, backup, genLink)
            ServiceLoader.startService(foundServiceClass, db={}, api=api, master = master)
            return {"obj": foundServiceClass.share, "api":api}


        return None

    def startService(service_class, db = None, api = None, master = None):
        serviceThread = Thread(target = ServiceLoader.startServiceAsync, args = [[service_class, db, api, master]])
        serviceThread.start()

    def startServiceAsync(data):
        service_class, db, api, master = data
        if master is None:
            service_class(db, api).go()
        else:
            service_class(db,api,master).go()
