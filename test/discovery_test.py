import unittest
import logging
import time

from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError, NodeExistsError

from service.discovery import ServiceDiscovery
from service.instance import ServiceInstance
    
class TestServiceDiscovery(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        logging.basicConfig(format="%(asctime)s %(levelname)s %(module)s[%(lineno)d] %(threadName)s %(message)s", level=logging.WARN)
        self.log = logging.getLogger()
        self.basePath = "/discovery_test_%x" % int(time.time())
        self.log.info("Using base path: %s" % self.basePath)
        self.client = KazooClient(hosts="127.0.0.1:2181") 
        self.client.start()
        self._clean()

        self.discovery = ServiceDiscovery(self.client, self.basePath)

    def _clean(self):
        try:
            self.client.delete(self.basePath,recursive=True)
        except NoNodeError:
            pass

    def tearDown(self):
        self.discovery.close()
        self._clean()
        self.client.stop()
        self.client.close()

    def test_paths(self):
        svc1 = ServiceInstance.builder().id("instance1").name("service1").build()
        svc2 = ServiceInstance.builder().id("instance2").name("service1").build()
        svc3 = ServiceInstance.builder().id("foo1").name("foo").build()

        self.assertEquals(self.basePath + "/service1/instance1", self.discovery.pathForInstance(svc1.getName(),svc1.getId()))
        self.assertEquals(self.basePath + "/service1/instance2", self.discovery.pathForInstance(svc2.getName(),svc2.getId()))
        self.assertEquals(self.basePath + "/foo/foo1", self.discovery.pathForInstance(svc3.getName(),svc3.getId()))

    def test_reg_and_dereg(self):
        svc1 = ServiceInstance.builder().id("instance1").name("service1").build()
        svc2 = ServiceInstance.builder().id("instance2").name("service1").build()
        svc3 = ServiceInstance.builder().id("foo1").name("foo").build()

        self.discovery.registerService(svc1)
        self.discovery.registerService(svc2)
        self.discovery.registerService(svc3)

        self.assertTrue(self.client.exists(self.discovery.pathForInstance(svc1.getName(),svc1.getId())))
        self.assertTrue(self.client.exists(self.discovery.pathForInstance(svc2.getName(),svc2.getId())))
        self.assertTrue(self.client.exists(self.discovery.pathForInstance(svc3.getName(),svc3.getId())))

        self.discovery.unregisterService(svc1)
        self.discovery.unregisterService(svc2)
        self.discovery.unregisterService(svc3)

        self.assertFalse(self.client.exists(self.discovery.pathForInstance(svc1.getName(),svc1.getId())))
        self.assertFalse(self.client.exists(self.discovery.pathForInstance(svc2.getName(),svc2.getId())))
        self.assertFalse(self.client.exists(self.discovery.pathForInstance(svc3.getName(),svc3.getId())))

    def test_query(self):
        svc1 = ServiceInstance.builder().id("instance1").name("service1").build()
        svc2 = ServiceInstance.builder().id("instance2").name("service1").build()
        svc3 = ServiceInstance.builder().id("foo1").name("foo").build()

        self.discovery.registerService(svc1)
        self.discovery.registerService(svc2)
        self.discovery.registerService(svc3)

        self.assertEquals(sorted(["foo", "service1"]), sorted(self.discovery.queryForNames()))
        instances = self.discovery.queryForInstances("service1")
        self.assertEquals(2, len(instances))
        self.assertEquals(sorted([svc1, svc2]), sorted(instances))

        # make sure unregister works
        self.discovery.unregisterService(svc2)
        instances = self.discovery.queryForInstances("service1")
        self.assertEquals(1, len(instances))
        self.assertEquals(sorted([svc1]), sorted(instances))

        instance = self.discovery.queryForInstance("service1","instance1")
        self.assertTrue(instance)
        self.assertEquals(svc1, instance)

