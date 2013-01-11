#**************************************************************
#  
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#  
#    http://www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.
#  
#**************************************************************

import uno
import unohelper

from com.sun.star.awt import Rectangle
from com.sun.star.awt.MessageBoxButtons import BUTTONS_OK
from com.sun.star.awt.MessageBoxType import INFOBOX
from com.sun.star.frame import XDispatch, XDispatchProvider
from com.sun.star.lang import XServiceInfo

class Provider(unohelper.Base, XServiceInfo, XDispatchProvider):
    implementationName = "com.sun.star.comp.test.deployment.passive_python"

    serviceNames = ("com.sun.star.test.deployment.passive_python",)

    def __init__(self, context):
        self.context = context

    def getImplementationName(self):
        return self.implementationName

    def supportsService(self, ServiceName):
        return ServiceName in self.serviceNames

    def getSupportedServiceNames(self):
        return self.serviceNames

    def queryDispatch(self, URL, TargetFrame, SearchFlags):
        return self.context.getValueByName( \
            "/singletons/com.sun.star.test.deployment.passive_python_singleton")

    def queryDispatches(self, Requests):
        tuple( \
            self.queryDispatch(i.FeatureURL, i.FrameName, i.SearchFlags) \
                for i in Requests)

class Dispatch(unohelper.Base, XServiceInfo, XDispatch):
    implementationName = \
        "com.sun.star.comp.test.deployment.passive_python_singleton"

    serviceNames = ()

    def __init__(self, context):
        self.context = context

    def getImplementationName(self):
        return self.implementationName

    def supportsService(self, ServiceName):
        return ServiceName in self.serviceNames

    def getSupportedServiceNames(self):
        return self.serviceNames

    def dispatch(self, URL, Arguments):
        smgr = self.context.getServiceManager()
        box = smgr.createInstanceWithContext( \
            "com.sun.star.awt.Toolkit", self.context).createMessageBox( \
                smgr.createInstanceWithContext( \
                    "com.sun.star.frame.Desktop", self.context). \
                    getCurrentFrame().getComponentWindow(), \
                INFOBOX, BUTTONS_OK, "passive", "python")
        box.execute();
        box.dispose();

    def addStatusListener(self, Control, URL):
        pass

    def removeStatusListener(self, Control, URL):
        pass

g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation( \
    Provider, Provider.implementationName, Provider.serviceNames)
g_ImplementationHelper.addImplementation( \
    Dispatch, Dispatch.implementationName, Dispatch.serviceNames)
