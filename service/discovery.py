#!/usr/bin/env python
import logging
import socket
import uuid
import time
import json # TODO maybe remove me

from kazoo.protocol import paths as ZkPaths
from kazoo.protocol.states import KazooState
from kazoo.exceptions import NoNodeError, NodeExistsError

from service.instance import ServiceType
from service.serialization import ServiceInstanceSerializer

class ServiceDiscovery(object):
    def __init__(self, client, basePath, thisInstance=None, serializer=None):
        if not client:
            raise ValueError("client cannot be None")
        if not basePath:
            raise ValueError("basePath cannot be None")

        self.log = logging.getLogger()
        self.client = client
        self.basePath = basePath
        self.services = {}
        self.serializer = serializer if serializer else ServiceInstanceSerializer()

        if thisInstance:
            self.__setService(thisInstance)

    def __stateChanged(self, newState):
        if newState == KazooState.CONNECTED:
            try:
                self.log.debug("Re-registering due to reconnection")
                self.__reRegisterServices()
            except:
                self.log.exception("Could not re-register instances after reconnection")

    def start(self):
        try:
            self.__reRegisterServices()
        except:
            self.log.exception("Could not register instances - will try again later")
        self.client.add_listener(self.__stateChanged)
            
    def close(self):
        if self.services:
            for service in self.services.values():
                path = self.pathForInstance(service.getName(), service.getId())

                try:
                    self.client.delete(path)
                except NoNodeError:
                    pass
                except:
                    self.log.exception("Could not unregister instance: %s" % service.getName())
            self.services = None
        self.client.remove_listener(self.__stateChanged)

    def __del__(self):
        self.close()

    def registerService(self, service):
        self.__setService(service)
        self.__registerService(service)

    def __reRegisterServices(self):
        for service in self.services.values():
            self.__registerService(service)

    def updateService(self, service):
        data = self.serializer.serialize(service)
        path = self.pathForInstance(service.getName(), service.getId())
        self.client.set(path, data)
        self.services[service.getId()] = service

    def __registerService(self, service):
        data = self.serializer.serialize(service)
        path = self.pathForInstance(service.getName(), service.getId())

        def register():
            ephemeral = service.getServiceType() == ServiceType.DYNAMIC
            self.client.create(path, data, ephemeral=ephemeral, makepath=True)

        try:
            register()
        except NodeExistsError:
            client.delete(path)
            register()

    def unregisterService(self, service):
        path = self.pathForInstance(service.getName(), service.getId())
        try:
            self.client.delete(path)
        except NoNodeError:
            pass
        del self.services[service.getId()] 

    def __setService(self, service):
        self.services[service.getId()] = service

    def queryForNames(self):
        return self.client.get_children(self.basePath)

    def queryForInstances(self, name, watcher=None):
        path = self.pathForName(name)

        if watcher:
            raise Exception("NOT IMPLEMENTED")
        else:
            try:
                instanceIds = self.client.get_children(path)
            except NoNodeError:
                instanceIds = []

            instances = []

        for id in instanceIds:
            instance = self.queryForInstance(name, id)
            if instance:
                instances.append(instance)
        return instances

    def queryForInstance(self, name, id):
        path = self.pathForInstance(name, id)
        try:
            data, stat = self.client.get(path)
            return self.serializer.deserialize(data)
        except NoNodeError:
            return None

    def pathForInstance(self, name, id):
        return ZkPaths.join(self.pathForName(name), id)

    def pathForName(self, name):
        return ZkPaths.join(self.basePath, name)

    def getClient(self):
        return client

    

