import unittest
import logging

from service.instance import ServiceInstance
from service.serialization import ServiceInstanceSerializer 

class TestSerialization(unittest.TestCase):

    def setUp(self):
        self.log = logging.getLogger()

    def test_serialization(self):
        serializer = ServiceInstanceSerializer(payloadCls=Foo)

        service1 = ServiceInstance.builder().id("instance1").name("service1").build()

        v = serializer.serialize(service1)
        self.log.debug(v)

        # Test custom payload classes
        service2 = ServiceInstance.builder().id("instance2").name("service2").payload(Foo()).build()
        self.log.debug(service2)

        v = serializer.serialize(service2)
        self.log.debug(v)

        o = serializer.deserialize(v)
        self.log.debug(o)
        self.assertEquals(service2, o)

        v2 = serializer.serialize(o)
        self.log.debug(v2)
        self.assertEquals(v, v2)

        service3 = ServiceInstance.builder().id("instance2").name("service3").payload({"bar":25}).build()
        v = serializer.serialize(service3)
        self.log.debug(v)

        # can't deserialize a class we don't know about
        service4 = ServiceInstance.builder().id("instance2").name("service4").payload(Bar()).build()
        v = serializer.serialize(service4)
        self.log.debug(v)
        with self.assertRaises(ValueError) as x:
            serializer.deserialize(v)

class Bar(object):
    pass

class Foo(object):
    def __init__(self):
        self.foo = 23
    def __repr__(self):
        return "Foo(%s)" % self.foo
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
    def __ne__(self, other):
        return not self.__eq__(other)

if __name__ == "__main__":
    unittest.main()
