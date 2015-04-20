import json
from service.instance import ServiceInstance

class ServiceInstanceEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ServiceInstance):
            d = {}
            for k, v in obj.__dict__.items():
                #if v == None:
                    #continue

                if k == "payload":
                    if isinstance(v, (list, dict, str, unicode, int, float, bool, type(None))):
                        d[unicode(k)] = v
                    else:
                        o = {}
                        o.update(v.__dict__)
                        t = type(v)
                        o["@class"] = str("%s.%s" % (t.__module__,t.__name__))
                        d[unicode(k)] = o
                else:
                    d[unicode(k)] = v
            return d

        return super(ServiceInstanceEncoder, self).default(obj)

class ServiceInstanceSerializer(object):
    def __init__(self, encoderCls=ServiceInstanceEncoder, decoderCls=None, payloadCls=None):
        self.encoderCls = encoderCls
        self.decoderCls = decoderCls
        self.payloadCls = payloadCls

    def serialize(self, service):
        return json.dumps(service, cls=self.encoderCls).encode("utf-8")

    def deserialize(self, data):
        o = json.loads(data, "utf-8", cls=self.decoderCls)
        b = ServiceInstance.builder()
        for k, v in o.items():
            if k.startswith("_"):
                continue
            elif k == "payload" and v != None:
                p = self.getClass(v["@class"])()
                for pk, pv in v.items():
                    if pk == "@class":
                        continue
                    setattr(p, pk, pv)
                if self.payloadCls and not isinstance(p, self.payloadCls):
                    raise ValueError("Object is not of class '%s'" % self.payloadCls)
                v = p
            getattr(b, k)(v)
        return b.build()

    def getClass(self, className):
        p = className.rsplit(".",1)
        m = __import__(p[0], globals(), locals(), p[1])
        c = getattr(m, p[1])
        return c


