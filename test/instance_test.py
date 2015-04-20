import unittest
from service.instance import ServiceInstance 

class TestServiceInstance(unittest.TestCase):

    def test_instance(self):
        with self.assertRaises(ValueError) as x:
            ServiceInstance.builder().build()

        with self.assertRaises(ValueError) as x:
            ServiceInstance.builder().id(1231).build()

        service1 = ServiceInstance.builder().id("1231").name("a1").build()
        service2 = ServiceInstance.builder().id("1111").name("a1").payload({"a" : 1}).build()

        self.assertEquals(service1, service1)
        self.assertNotEquals(service1, service2)


if __name__ == "__main__":
    unittest.main()
