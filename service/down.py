import time
import itertools

class InstanceFilter(object):
    def apply(self, instance):
        return True

def currentTimeMs():
    return long(round(time.time()*1000))

class DownInstanceManager(InstanceFilter):

    def __init__(self, downInstancePolicy):
        self.statuses = {}
        self.downInstancePolicy = downInstancePolicy
        self.lastPurge = currentTimeMs()

    def add(self, instance):
        newStatus = Status()
        oldStatus = self.statuses.setdefault(instance,newStatus)
        useStatus = oldStatus if oldStatus else newStatus;
        useStatus.errorCount.next() # essentially incrementAndGet()

    def apply(self, instance):
        purge()

        status = self.statuses.get(instance)

    class Status(object):
        def __init__(self):
            self.startMs = currentTimeMs()
            self.errrorCount = itertools.count()

    
