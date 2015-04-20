import socket
import uuid
import time
from datetime import datetime

class ServiceType(object):
    DYNAMIC = u"DYNAMIC" 
    STATIC = u"STATIC" 
    PERMANENT = u"PERMANENT" 

class ServiceInstanceBuilder(object):
    def __init__(self):
        self._serviceType = ServiceType.DYNAMIC
        self._uriSpec = None
        self._name = None
        self._id = None
        self._address = None
        self._port = None
        self._sslPort = None
        self._payload = None
        self._registrationTimeUTC = None

    def build(self):
        return ServiceInstance(self._name, self._id, self._address, self._port, self._sslPort, self._payload, self._registrationTimeUTC, self._serviceType, self._uriSpec)

    def _encode(self, value):
        if value == None or not isinstance(value, str):
            return value
        else:
            return unicode(value)

    def serviceType(self, serviceType):
        self._serviceType = self._encode(serviceType)
        return self

    def uriSpec(self, uriSpec):
        self._uriSpec = self._encode(uriSpec)
        return self

    def name(self, name):
        self._name = self._encode(name)
        return self

    def id(self, id):
        self._id = self._encode(id)
        return self

    def address(self, address):
        self._address = self._encode(address)
        return self

    def port(self, port):
        self._port = int(port) if port else None
        return self

    def sslPort(self, sslPort):
        self._sslPort = int(sslPort) if sslPort else None
        return self

    def payload(self, payload):
        self._payload = payload
        return self

    def registrationTimeUTC(self, registrationTimeUTC):
        self._registrationTimeUTC = long(registrationTimeUTC) if registrationTimeUTC else registrationTimeUTC
        return self

class ServiceInstance(object):
    def __init__(self, name, id, address=None, port=None, sslPort=None, payload=None, registrationTimeUTC=None, serviceType=None, uriSpec=None):
        if not name:
            raise ValueError("name cannot be None")
        if not id:
            raise ValueError("id cannot be None")

        self.serviceType = serviceType;
        self.uriSpec = uriSpec;
        self.name = name;
        self.id = id;
        self.address = address;
        self.port = port;
        self.sslPort = sslPort;
        self.payload = payload;
        self.registrationTimeUTC = registrationTimeUTC;
        self.__sortKey = "%s:%s" % (self.name, self.id)

    @staticmethod
    def builder():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
        address = s.getsockname()[0]
        id = str(uuid.uuid4())

        # Make sure we get UTC time (for pre-python2.7)
        epoch = datetime(1970, 1, 1)
        now = (datetime.utcnow() - epoch).total_seconds()

        return ServiceInstanceBuilder().address(address).id(id).registrationTimeUTC(int(round(now * 1000)))

    def __repr__(self):
        return "<ServiceInstance %s>" % str(dict([(unicode(x[0]),x[1]) for x in self.__dict__.items()]))[1:-1]

    def getName(self):
        return self.name

    def getServiceType(self):
        return self.serviceType

    def getServiceType(self):
        return self.serviceType;

    def getUriSpec(self):
        return self.uriSpec;

    def getName(self):
        return self.name;

    def getId(self):
        return self.id;

    def getAddress(self):
        return self.address;

    def getPort(self):
        return self.port;

    def getSslPort(self):
        return self.sslPort;

    def getPayload(self):
        return self.payload;

    def getRegistrationTimeUTC(self):
        return self.registrationTimeUTC;

    def __hash__(self):
        return hash([x for x in self.__dict__.items() if not x[0].startswith("_"))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        self.__sortKey < other.__sortKey

    def __le__(self, other):
        self.__sortKey <= other.__sortKey

    def __gt__(self, other):
        self.__sortKey > other.__sortKey

    def __ge__(self, other):
        self.__sortKey >= other.__sortKey

