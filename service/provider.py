

def ServiceProviderBuilder(object):
    def __init__(self, discovery):
        self._discovery = discovery
        self._serviceName = None
        self._providerStrategy = None
        #ThreadFactory threadFactory
        self._filters = []
        self._downInstancePolicy = DownInstancePolicy()

    def build(self):
        return ServiceProvider(self._discovery, self._serviceName, self._providerStrategy, self._filters, self._downInstancePolicy)

    def discovery(self, discovery):
        self._discovery = discovery
        return self

    def serviceName(self, serviceName):
        self._serviceName = serviceName
        return self

    def providerStrategy(self, providerStrategy):
        self._providerStrategy = providerStrategy
        return self

    def additionalFilter(self, filter):
        self._filters.append(filter)
        return self

    def downInstancePolicy(self, downInstancePolicy):
        self._downInstancePolicy = downInstancePolicy
        return self

def DownInstancePolicy(object):
    def __init__(self, timeoutMs=30000, errorThreshold=2):
        self.timeoutMs = timeoutMs
        self.errorThreshold = errorThreshold

    def getErrorThreshold(self):
        return self.errorThreshold

    def getTimeoutMs(self):
        return self.timeoutMs
