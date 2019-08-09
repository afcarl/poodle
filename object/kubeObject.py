import sys

from poodle import *
from object.commonObject import *
from object.addedNumbers10 import *

NULL='null'

class NumberFactory():
    maxNum=0
    numberCollection = {}
    null=Number('null')

    def __init__(self, num=202):
        self.maxNum = num
        for i in range(0, num) :
            self.addNumber(i)
        # for i in range(0, num):
        #     for j in range(0,i):
        #         print("LOWER " , "I ",i," j ", j , " ", self.getNumber(j))
        #         self.numberCollection[i].lower_than.add(self.getNumber(j))
        #     for j in range(i+1, num):
        #         print("GREATER ",j , " ", self.getNumber(j))
        #         self.numberCollection[i].higher_than.add(self.numberCollection[j])


    def addNumber(self, num):
        self.numberCollection[num] = Number(num)

    def getNumber(self,num):
        if num == 'null':
            return self.null
        return self.numberCollection[num]

class Type(Object):
    pass

class Kind(Object):
    pass
    # Identity
    # Properties 
    # Relations
         
class Mode(Object):
    pass
    # Identity
    # Properties 
    # Relations 

class Status(Object):
    sequence = Property(Number)

    # Identity
    # Properties 
    # Relations 
    
class State(Object):
    sequence = Property(Number)

class ContainerConfig(Object):
    service = Property("Service")
    realInitialMemConsumption = Property( Number)
    realInitialCpuConsumption = Property( Number)
    currentRealCpuConsumption = Property( Number)
    currentRealMemConsumption = Property( Number)
    podIsOnetime = StateFact()
    memLimit = Property(Number)
    cpuLimit = Property(Number)
    type = Property(Type)
    _label = ""
    requestedMem = Property(Number)
    requestedCpu = Property(Number)
    # status =..... #Stopped here 2807 Artem
   

class Node(Object):
    # Identity
    # Properties 
    cpuCapacity = Property(Number)
    memCapacity = Property(Number)
    status = Property(Status)
    state = Property(State)
    currentFormalCpuConsumption = Property(Number)
    currentFormalMemConsumption = Property(Number)
    currentRealMemConsumption = Property(Number)
    currentRealCpuConsumption = Property(Number)
    AmountOfPodsOverwhelmingMemLimits = Property(Number)
    podAmount = Property(Number)
Node.prevNode = Property(Node)

class EntityType(Object):
    pass

class GlobalVar(Object):
    numberOfRejectedReq = Property(Number)
         
class Pod(Object):
    #Identity
    # Property
    podId = Property(Number)
    podConfig = Property(ContainerConfig)
    realInitialMemConsumption = Property( Number)
    realInitialCpuConsumption = Property( Number)
    currentRealCpuConsumption = Property( Number)
    currentRealMemConsumption = Property( Number)
    atNode = Property(Node)
    toNode = Property(Node)
    status = Property(Status)
    state = Property(State)
    isPending = StateFact()
    isRunning = StateFact()
    bindedToNode = Property(Node)
    podOverwhelmingLimits = StateFact()
    podNotOverwhelmingLimits = StateFact()
    podIsOnetime = StateFact()
    memLimit = Property(Number)
    cpuLimit = Property(Number)
    type = Property(Type)
    _label = ""
    requestedMem = Property(Number)
    requestedCpu = Property(Number)
    targetService = Property("Service")

    def __str__ (self): return str(self.value)
    

Pod.prevPod = Property(Pod)    
    
# class Event(PlannedAction):
#     #Identity
#     # Property
#     node = Property(Node)
#     extraValue = Property(Number)
#     eventType = Property(EventType)

# class EventType(Object):
#     #Identity
    
class Service(Object):
    lastPod = Property(Pod)
    atNode = Property(Node)
    _label = ""
         # Relations
Service.selectionedPod = Relation(Pod)

class Period(Object):
    pass
         # Relations
Period.prevPeriod = Property(Period)         


class Container(Object):
        # Properties
    hasPod = Property(Pod)
    cpuRequest = Property(Number)
    memRequest = Property(Number)
    cpuLimit = Property(Number)
    memLimit = Property(Number)
    config = Property(ContainerConfig)

class Request(Object):
         # Properties 
    
    launchPeriod = Property(Period)
    status = Property(Status)
    state = Property(State)
    atLb = Property('Loadbalancer')
    isAtLoadbalancer = StateFact()
    atPod = Property(Pod)
    atNode = Property(Node)
    toPod = Property(Pod)
    toNode = Property(Node)
    firstToNode = Property(Node)
    firstToPod = Property(Pod)
    targetService = Property(Service)
    cpuRequest = Property(Number)
    memRequest = Property(Number)
    type = Property(Type)
         # Relations

class Loadbalancer(Object):
    _ipAndName = []
    lastNode = Property(Node)
    atNode = Property(Node)
    switchingPerformed = StateFact()
         # Relations
Loadbalancer.selectionedService = Relation(Service)
        
class Kubeproxy(Object):


    # Properties 
    mode = Property(Mode)
    lastPod = Property(Pod)
    atNode = Property(Node)
    # Relations

         # Relations


ContainerConfig.service = Property(Service)
     