from poodle.poodle import * 
from object.commonObject import *
from object.addedNumbers10 import *

class NumberFactory():
    numberCollection = {}

    def __init__(self, num=202):
        for i in range(0, num) :
            self.addNumber(i)
    def addNumber(self, num):
        self.numberCollection[num] = Number(num)
    def getNumber(self,num):
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
Node.prevNode = Property(Node)

class EntityType(Object):
    pass
         
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
    bindedToNode = Property(Node)
    requestedMem = Property(Number)
    requestedCpu = Property(Number)
    podOverwhelmingLimits = StateFact()
    podNotOverwhelmingLimits = StateFact()
    podIsOnetime = StateFact()
    memLimit = Property(Number)
    cpuLimit = Property(Number)
    type = Property(Type)
    

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
    atPod = Property(Pod)
    atNode = Property(Node)
    toPod = Property(Pod)
    toNode = Property(Node)    
    targetService = Property(Service)
    cpuRequest = Property(Number)
    memRequest = Property(Number)
    type = Property(Type)
         # Relations

class Loadbalancer(Object):
    lastNode = Property(Node)
    atNode = Property(Node)
         # Relations
Loadbalancer.selectionedService = Relation(Service)
        
class Kubeproxy(Object):


    # Properties 
    mode = Property(Mode)
    lastPod = Property(Pod)
    atNode = Property(Node)
    # Relations
Kubeproxy.selectionedPod = Relation(Pod)
Kubeproxy.selectionedService = Relation(Service)

         # Relations


ContainerConfig.service = Property(Service)


class ToLoadbalancer(PlannedAction):
    cost = 1
    request1 = Request()
    serviceTarget = Select(Service == request1.targetService)
    lb = Loadbalancer()
    lbNode = Select(Node == lb.atNode)

    def selector(self):
        return Select( self.serviceTarget in self.lb.selectionedService and \
        self.request1.status == self.problem.statusReqAtStart)
    
    def effect(self):
        self.request1.status.set(self.problem.statusReqAtLoadbalancer)
        self.request1.state.set(self.problem.stateRequestActive)
        self.request1.atNode.set(self.lbNode)

class DirectToNode(PlannedAction):
    cost = 1
    request1 = Request()
    targetService = Select( Service == request1.targetService)
    podWithTargetService = Select( Pod == targetService.selectionedPod)
    nodeWithTargetService = Select( Node == podWithTargetService.atNode)
    
    def selector(self):
        return Select( self.request1.status == self.problem.statusReqAtLoadbalancer)

    def effect(self):
        self.request1.status = self.problem.statusPodDirectedToNode
        self.request1.toNode = self.nodeWithTargetService
        
        # newPod = self.problem.addObject(Pod())
        # newPod.memRequest = self.template1.memRequest

        # self.node.pod.add(self.problem.pod1)
        
        # self.newPod.set()
        # newPod.podConfig = ...
        
#        self.newPod.status = pending
#        self.newPod.memRequest = ...


    
class ToNode(PlannedAction):
    cost = 1 
    request1 = Request()
    node1 = Select( Node == request1.toNode)

    def selector(self):
        return Select( self.node1.status == self.problem.statusNodeActive and self.request1.status == self.problem.statusPodDirectedToNode)

    def effect(self):
        self.request1.status = self.problem.statusReqAtKubeproxy
        self.request1.toNode.unset(self.node1)
        self.request1.atNode = self.node1


class SwitchToNextNode(PlannedAction):
    cost = 1
    request1 = Request()
    node1 = Select( Node == request1.toNode)
    nextNode1 = Select( Node.prevNode == node1)
    def selector(self):
        return Select( self.node1.status == self.problem.statusNodeInactive and self.request1.status == self.problem.statusPodDirectedToNode)

    def effect(self):
        self.request1.toNode = self.nextNode1


class DirectToPod(PlannedAction):
    cost = 1
    request1 = Request()
    targetService = Select( Service == request1.targetService)
    podWithTargetService = Select( Pod == targetService.selectionedPod)
    currectNode = Select( Node == request1.atNode)


    def selector(self):
        return Select(self.request1.status == self.problem.statusReqAtKubeproxy)

    def effect(self):
        self.request1.status = self.problem.statusPodDirectedToNode
        self.request1.toPod = self.podWithTargetService


class ToPod(PlannedAction):
    cost = 1 
    request1 = Request()
    pod1 = Select( Pod == request1.toPod)

    def selector(self):
        return Select( self.pod1.status == self.problem.statusPodActive and \
        self.request1.status == self.problem.statusPodDirectedToNode) 

    def effect(self):
        self.request1.status = self.problem.statusReqAtPodInput
        self.request1.toPod.unset(self.pod1) 
        self.request1.atPod = self.pod1



class SwitchToNextPod(PlannedAction):
    cost = 1
    request1 = Request()
    pod1 = Select( Pod == request1.toPod)
    nextPod1 = Select( Pod.prevPod == request1.toPod)
    nodeForPod = Select( Node == pod1.atNode)
    kubeproxyatNode = Select( Kubeproxy.atNode == nodeForPod)
    def selector(self):
        return Select(self.pod1.status == self.problem.statusPodInactive and \
        self.kubeproxyatNode.mode == self.problem.modeUsermode and \
        Request.status == self.problem.statusReqDirectedToPod) 
    def effect(self):
        self.request1.toPod = self.nextPod1

class ConsumeResourceCpu(PlannedAction):
    cost = 1
    request1 =  Request()
    currentPod = Select( Pod == request1.atPod)
    currentNode = Select( Node == currentPod.atNode)

    addedCpuConsumptionAtCurrentPod1_res = AddedNumber.Select(operator1 = currentPod.currentRealCpuConsumption, operator2 = request1.cpuRequest)
    addedCpuConsumptionAtCurrentPod1_res_num = Select(  Number == addedCpuConsumptionAtCurrentPod1_res.result)
    
    addedCpuConsumptionAtCurrentNode1_res = AddedNumber.Select( operator1 = currentNode.currentRealCpuConsumption, operator2 = request1.cpuRequest) 
    addedCpuConsumptionAtCurrentNode1_res_num = Select(  Number == addedCpuConsumptionAtCurrentNode1_res.result)
    
    #KB: RealCPUConsumption - is consumption calculated per active requests ( each request adds some level of consumption, realy on the CPU/Mem
    #KB: RealCPUConsumption - it is tracked for pod and node . Both. this is used by autoscale and scheduller and kubectl  while starting pods on node
    #KB: FormalCPUConcumption - it is consumption calculated for nodes only. Pods when try to start shoul check limits by this value.  
    
    def selector(self):
        return Select( self.request1.status == self.problem.statusReqAtPodInput )        

    def effect(self):
        self.request1.status.set(self.problem.statusReqCpuResourceConsumed)
        self.currentPod.currentRealCpuConsumption.set(self.addedCpuConsumptionAtCurrentPod1_res_num)
        self.currentNode.currentRealCpuConsumption.set(self.addedCpuConsumptionAtCurrentNode1_res_num)

class ConsumeResourceMem(PlannedAction):
    cost = 1
    request1 =  Request()
    currentPod = Select( Pod == request1.atPod)
    currentNode = Select( Node == currentPod.atNode)

    addedMemConsumptionAtCurrentPod1_res = AddedNumber.Select(operator1 = currentPod.currentRealMemConsumption, operator2 = request1.memRequest) 
    addedMemConsumptionAtCurrentPod1_res_num = Select(  Number == addedMemConsumptionAtCurrentPod1_res.result)
    
    addedMemConsumptionAtCurrentNode1_res = AddedNumber.Select( operator1 = currentNode.currentRealMemConsumption, operator2 = request1.memRequest)
    addedMemConsumptionAtCurrentNode1_res_num = Select(  Number == addedMemConsumptionAtCurrentNode1_res.result)
    
    def selector(self):
        return Select( self.request1.status == self.problem.statusReqCpuResourceConsumed )        

    def effect(self):
        self.request1.status.set(self.problem.statusReqMemResourceConsumed)
        self.currentPod.currentRealMemConsumption.set(self.addedMemConsumptionAtCurrentPod1_res_num)
        self.currentNode.currentRealMemConsumption.set(self.addedMemConsumptionAtCurrentNode1_res_num)

class ConsumeResource(PlannedAction):
    cost = 1
    request1 =  Request()
    currentPod = Select( Pod == request1.atPod)
    currentNode = Select( Node == currentPod.atNode)

    def selector(self):
        return Select( self.request1.status == self.problem.statusReqMemResourceConsumed )        

    def effect(self):
        self.request1.status.set(self.problem.statusReqResourcesConsumed)

class ProcessTempRequest(PlannedAction):
    cost = 1
    request1 = Request()
    
    def selector(self):
        return Select( self.request1.status == self.problem.statusReqResourcesConsumed and self.request1.type == self.problem.typeTemporary)
    
    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestPIDToBeEnded)
        
class ProcessPersistentRequest(PlannedAction):
    cost = 1
    request1 = Request()
    
    def selector(self):
        return Select( self.request1.status == self.problem.statusReqResourcesConsumed and \
        self.request1.type == self.problem.typePersistent)

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)


class ReleaseResourceCpu(PlannedAction):
    cost = 1
    request1 = Request() 
    currentPod = Select( Pod == request1.atPod)
    currentNode = Select( Node == request1.atNode)

    reducedCpuConsumptionAtCurrentPod1 = Select( AddedNumber.result == currentPod.currentRealCpuConsumption)
    reducedCpuConsumptionAtCurrentPod1_op1 = Select (Number == reducedCpuConsumptionAtCurrentPod1.operator1)
    
    reducedCpuConsumptionAtCurrentNode1 = Select( AddedNumber.result == currentNode.currentRealCpuConsumption) 
    reducedCpuConsumptionAtCurrentNode1_op1 = Select (Number == reducedCpuConsumptionAtCurrentNode1.operator1)
    
    def selector(self):
        return Select( self.request1.status == self.problem.statusReqRequestPIDToBeEnded and \
        self.reducedCpuConsumptionAtCurrentPod1.operator2 == self.request1.cpuRequest and \
        self.reducedCpuConsumptionAtCurrentNode1.operator2 == self.request1.cpuRequest)

    def effect(self):
        self.request1.status.set(self.problem.statusReqCpuResourceReleased)
        self.currentPod.currentRealCpuConsumption.set(self.reducedCpuConsumptionAtCurrentPod1_op1)
        self.currentNode.currentRealCpuConsumption.set(self.reducedCpuConsumptionAtCurrentNode1_op1)

class ReleaseResourceMem(PlannedAction):
    cost = 1
    request1 = Request() 
    currentPod = Select( Pod == request1.atPod)
    currentNode = Select( Node == request1.atNode)

    reducedMemConsumptionAtCurrentPod1 = Select( AddedNumber.result == currentPod.currentRealMemConsumption) 
    reducedMemConsumptionAtCurrentPod1_op1 = Select (Number == reducedMemConsumptionAtCurrentPod1.operator1)
    
    reducedMemConsumptionAtCurrentNode1 = Select( AddedNumber.result == currentNode.currentRealMemConsumption)
    reducedMemConsumptionAtCurrentNode1_op1 = Select (Number == reducedMemConsumptionAtCurrentNode1.operator1)
    def selector(self):
        return Select( self.request1.status == self.problem.statusReqCpuResourceReleased and \
        self.reducedMemConsumptionAtCurrentPod1.operator2 == self.request1.memRequest and \
        self.reducedMemConsumptionAtCurrentNode1.operator2 == self.request1.memRequest)


    def effect(self):
        self.request1.status.set(self.problem.statusReqMemResourceReleased)
        self.currentPod.currentRealMemConsumption.set(self.reducedMemConsumptionAtCurrentPod1_op1)
        self.currentNode.currentRealMemConsumption.set(self.reducedMemConsumptionAtCurrentNode1_op1) 

class ReleasedResources(PlannedAction):
    cost = 1
    request1 = Request() 
    currentPod = Select( Pod == request1.atPod)
    currentNode = Select( Node == request1.atNode)

    def selector(self):
        return Select( self.request1.status == self.problem.statusReqMemResourceReleased)

    def effect(self):
        self.request1.status.set(self.problem.statusReqResourcesReleased)

class FinishRequest(PlannedAction):
    cost = 1
    request1 = Request()
    pod1 = Select( Pod == request1.atPod)
    node1 = Select( Node == request1.atNode)
    
    
    def selector(self):
        return Select( self.request1.status == self.problem.statusReqResourcesReleased and \
         self.pod1.type == self.problem.typePersistent)
    
    def effect(self):
        self.request1.status.set( self.problem.statusReqRequestFinished)
        self.request1.atPod.unset(self.pod1)
        self.request1.atNode.unset(self.node1)
        self.request1.state = self.problem.stateRequestInactive

class TerminatePodAfterFinish(PlannedAction):
    cost = 1
    request1 = Request()
    pod1 = Select(Pod == request1.atPod)
    node1 = Select( Node == request1.atNode)

    def selector(self):
        return Select( self.request1.status == self.problem.statusReqResourcesReleased and \
        self.pod1.type == self.problem.typeTemporary)
        
    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)
        self.request1.atPod.unset(self.pod1)
        self.request1.atNode.unset(self.node1)
        self.pod1.status.set(self.problem.statusReqRequestTerminated)
        self.request1.state.set(self.problem.stateRequestInactive)

class TerminatePod(PlannedAction):
    cost = 1
    pod1 = Pod()
    request1 = Request()
    currentNode = Select( Node == pod1.atNode)
    reducedCpuConsumptionAtCurrentNode1 = Select( AddedNumber.result == currentNode.currentRealCpuConsumption)
    reducedCpuConsumptionAtCurrentNode1_op1 = Select( Number == reducedCpuConsumptionAtCurrentNode1.operator1)
    reducedMemConsumptionAtCurrentNode1 = Select( AddedNumber.result == currentNode.currentRealMemConsumption)
    reducedMemConsumptionAtCurrentNode1_op1 = Select( Number == reducedMemConsumptionAtCurrentNode1.operator1)
    
    def selector(self):
        return Select( self.request1.status == self.problem.statusReqRequestPIDToBeEnded and
        self.reducedCpuConsumptionAtCurrentNode1.operator2 == self.pod1.currentRealCpuConsumption and
        self.reducedMemConsumptionAtCurrentNode1.operator2 == self.pod1.currentRealMemConsumption)

    def effect(self):
        self.pod1.status.set(self.problem.statusPodInactive) #TODO: divide status and state  for POds. state is to be active and nonactive. and status  would also include intermediate substates        
        self.currentNode.currentRealCpuConsumption = self.reducedCpuConsumptionAtCurrentNode1_op1
        self.currentNode.currentRealMemConsumption = self.reducedMemConsumptionAtCurrentNode1_op1
        self.request1.state.set(self.problem.statePodInactive)


############
# Scaling
### Replicas

class ReadDeploymentConfig(PlannedAction):
    pod1 = Pod()
    configOfPod = Select(ContainerConfig == pod1.podConfig)
    serviceOfPod = Select(Service == configOfPod.service)
    def selector(self):
        Select(self.pod1.status == self.problem.statusPodAtConfig)
    
    def effect(self):
        self.pod1.status.set(self.problem.statusPodPending) 
        self.serviceOfPod.selectionedPod.add(self.pod1)

class CreatePodManually(PlannedAction):
    pod1 = Pod()
    def selector(self):
        return Select(self.pod1.status == self.problem.statusPodAtManualCreation)

    def effect(self):
        self.pod1.status.set(self.problem.statusPodPending)

class SchedulerNofityUnboundedPod(PlannedAction):
    pod1 = Pod()
    node1 = Node()
    
    #freeMem_op1 = Select( AddedNumber.operator2 == node1.currentFormalMemConsumption)
    NodeWithSomefreeMem_op1 = AddedNumber.Select(operator2 = node1.currentFormalMemConsumption, result = node1.memCapacity)
    NodeWithSomefreeCpu_op1 = AddedNumber.Select(operator2 = node1.currentFormalCpuConsumption, result = node1.cpuCapacity)
    checkThatfreeMemIsEnoughForPodLaunch_op1 =  AddedNumber.Select(operator2 = pod1.requestedMem, result = NodeWithSomefreeMem_op1.operator1)
    checkThatfreeCpuIsEnoughForPodLaunch_op1 = AddedNumber.Select(operator2 = pod1.requestedCpu, result = NodeWithSomefreeCpu_op1.operator1)
    newFormalMemConsumptionAtNode_res = Select( AddedNumber.operator1 == node1.currentFormalMemConsumption) 
    newFormalMemConsumptionAtNode_res_num = Select(Number == newFormalMemConsumptionAtNode_res.result)
    #newFormalCpuConsumptionAtNode_res = AddedNumber.Select(operator1 == node1.currentFormalCpuConsumption, operator2 = pod1.requestedCpu)
    newFormalCpuConsumptionAtNode_res = Select( AddedNumber.operator1 == node1.currentFormalCpuConsumption) 
    newFormalCpuConsumptionAtNode_res_num = Select(Number == newFormalCpuConsumptionAtNode_res.result)
    
    #to-do: Soft conditions are not supported yet ( prioritization of nodes :  for example healthy  nodes are selected  rather then non healthy if pod  requests such behavior 
    def selector(self):
        return Select( self.pod1.status == self.problem.statusPodPending and\
        self.newFormalMemConsumptionAtNode_res.operator2 == self.pod1.requestedMem and\
        self.newFormalCpuConsumptionAtNode_res.operator2 == self.pod1.requestedCpu)
    
    def effect(self):
        self.pod1.status.set(self.problem.statusPodBindedToNode)
        self.pod1.bindedToNode.set(self.node1)
        self.node1.currentFormalMemConsumption.set(self.newFormalMemConsumptionAtNode_res_num)
        self.node1.currentFormalCpuConsumption.set(self.newFormalCpuConsumptionAtNode_res_num)

class KubectlStartsPod(PlannedAction):
    pod1 = Pod()
    
    # consume real resources from node
    node1 = Select( Node == pod1.bindedToNode)
    newMemRealConsumptionAtNode_res = AddedNumber.Select(operator1 = node1.currentRealMemConsumption, operator2 = pod1.realInitialMemConsumption)
    newMemRealConsumptionAtNode_res_num = Select( Number == newMemRealConsumptionAtNode_res.result)
    newCpuRealConsumptionAtNode_res = AddedNumber.Select(operator1 = node1.currentRealCpuConsumption, operator2 = pod1.realInitialCpuConsumption)
    newCpuRealConsumptionAtNode_res_num = Select( Number == newCpuRealConsumptionAtNode_res.result)
    
    def selector(self):
        return Select(self.pod1.status == self.problem.statusPodBindedToNode)
    
    def effect(self):
        self.pod1.status.set(self.problem.statusPodActive)
        self.pod1.state.set(self.problem.statePodActive)
        self.pod1.atNode.set(self.node1)
        self.node1.currentRealMemConsumption.set(self.newMemRealConsumptionAtNode_res_num)
        self.node1.currentRealCpuConsumption.set(self.newCpuRealConsumptionAtNode_res_num)

class MarkPodAsOverwhelmingMemLimits(PlannedAction):
    cost = 1
    pod1 = Pod()
    node1 = Select( Node == pod1.atNode)
    nextAmountOfoverwhelming  = Select( AddedNumber.operator1 == node1.AmountOfPodsOverwhelmingMemLimits)
    nextAmountOfoverwhelming_res = Select( Number == nextAmountOfoverwhelming.result)
    greaterthan = GreaterThan()
    

    def selector(self):
        return Select( 
            self.pod1.podNotOverwhelmingLimits == True and \
            self.greaterthan.lower == self.pod1.memLimit and \
        self.greaterthan.higher == self.pod1.currentRealMemConsumption and \
        self.nextAmountOfoverwhelming.operator2 == self.problem.numberFactory.getNumber(1))

    def effect(self):
        self.pod1.podOverwhelmingLimits.set()
        self.pod1.podNotOverwhelmingLimits.unset()
        self.node1.AmountOfPodsOverwhelmingMemLimits = self.nextAmountOfoverwhelming_res

class MarkPodAsNonoverwhelmingMemLimits(PlannedAction):
    cost = 1
    pod1 = Pod()
    node1 = Select(Node == pod1.atNode)
    prevAmountOfoverwhelming  = Select( AddedNumber.result == node1.AmountOfPodsOverwhelmingMemLimits)
    prevAmountOfoverwhelming_op1  = Select( Number == prevAmountOfoverwhelming.operator1)
    greaterthan = GreaterThan()

    def selector(self):
        return Select(self.pod1.podOverwhelmingLimits == True and \
        self.greaterthan.lower == self.pod1.memLimit and \
        self.greaterthan.higher == self.pod1.currentRealMemConsumption and \
        self.prevAmountOfoverwhelming.operator2 == self.problem.numberFactory.getNumber(1))

    def effect(self):
        self.pod1.podOverwhelmingLimits.set()
        self.pod1.podNotOverwhelmingLimits.unset()
        self.node1.AmountOfPodsOverwhelmingMemLimits = self.prevAmountOfoverwhelming_op1


class MemoryErrorKillPodOverwhelmingLimits(PlannedAction):
    cost = 1
    node1 = Node()
    pod1 = Select( Pod.atNode == node1)
    greaterthan = GreaterThan()

    def selector(self):
        return Select(self.greaterthan.lower == self.node1.memCapacity and \
                self.greaterthan.higher == self.node1.currentRealMemConsumption and \
                self.node1.status == self.problem.statusNodeActive and \
                self.pod1.podOverwhelmingLimits == True)

    def effect(self):
        self.pod1.status.set(self.problem.statusNodeOomKilling)

class MemoryErrorKillPodNotOverwhelmingLimits(PlannedAction):
    cost = 2
    node1 = Node()
    pod1 = Select( Pod.atNode == node1)
    greaterthan = GreaterThan()
    def selector(self):
        return Select(self.greaterthan.lower == self.node1.memCapacity and \
        self.greaterthan.higher == self.node1.currentRealMemConsumption and \
        self.node1.AmountOfPodsOverwhelmingMemLimits == self.problem.numberFactory.getNumber(0))

    def effect(self):
        self.pod1.status.set(self.problem.statusNodeOomKilling)
        

class PodFailsBecauseOfKilling(PlannedAction):
    pod1 = Pod()
    # release initial pod resources from node  
    node1 = Select( Node == pod1.atNode)
    newMemRealConsumptionAtNode_op1 = Select( AddedNumber.result == node1.currentRealMemConsumption)
    newMemRealConsumptionAtNode_op1_res = Select( Number == newMemRealConsumptionAtNode_op1.operator1)
    newCpuRealConsumptionAtNode_op1 = Select( AddedNumber.result == node1.currentRealCpuConsumption)
    newCpuRealConsumptionAtNode_op1_res = Select( Number == newCpuRealConsumptionAtNode_op1.operator1)
    def selector(self):
        return Select( self.node1.status == self.problem.statusNodeOomKilling and \
        self.newMemRealConsumptionAtNode_op1.operator2 == self.pod1.realInitialMemConsumption and \
        self.newCpuRealConsumptionAtNode_op1.operator2 == self.pod1.realInitialCpuConsumption)

    def effect(self):
        self.pod1.status.set(self.problem.statusNodeFailed)
        self.node1.currentRealMemConsumption.set(self.newMemRealConsumptionAtNode_op1_res)
        self.node1.currentRealCpuConsumption.set(self.newCpuRealConsumptionAtNode_op1_res)
        self.node1.state.set(self.problem.stateNodeInactive)

        

class PodSucceds(PlannedAction):
    pod1 = Pod()
    # release initial pod resources from node  
    node1 = Select( Node == pod1.atNode)
    newMemRealConsumptionAtNode_op1 = Select(AddedNumber.result == node1.currentRealMemConsumption)
    newMemRealConsumptionAtNode_op1_res = Select( Number == newMemRealConsumptionAtNode_op1.operator1)
    newCpuRealConsumptionAtNode_op1 = Select(AddedNumber.result == node1.currentRealCpuConsumption)
    newCpuRealConsumptionAtNode_op1_res = Select( Number == newMemRealConsumptionAtNode_op1.operator1)
    
    def selector(self):
        return Select ( self.node1.status == self.problem.statusNodeRunning and \
        self.newMemRealConsumptionAtNode_op1.operator2 == self.pod1.realInitialMemConsumption and \
        self.newCpuRealConsumptionAtNode_op1.operator2 == self.pod1.realInitialCpuConsumption)
    
    def effect(self):
        self.pod1.status.set(self.problem.statusNodeSucceded)
        self.node1.currentRealMemConsumption.set(self.newMemRealConsumptionAtNode_op1_res)
        self.node1.currentRealCpuConsumption.set(self.newCpuRealConsumptionAtNode_op1_res)


class KubectlRecoverPod(PlannedAction):
    pod1 = Pod()
    
    def selector(self):
        return Select( self.pod1.status == self.problem.statusNodeFailed)
    def effect(self):
        self.pod1.status.set(self.problem.statusNodePending)

class PodGarbageCollectedFailedPod(PlannedAction):
    pod1 = Pod()
    def selector(self):
        return Select( self.pod1.status == self.problem.statusNodeFailed)
    def effect(self):
        self.pod1.status.set(self.problem.statusNodeDeleted)
        

class PodGarbageCollectedSuccededPod(PlannedAction):
    pod1 = Pod()
    def selector(self):
        return Select( self.pod1.status == self.problem.statusNodeSucceded) 

    def effect(self):
        self.pod1.status.set(self.problem.statusNodeDeleted)

class ExitBrakePointForRequest1(PlannedAction):
    cost = 9000
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(1)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)

class ExitBrakePointForRequest2(PlannedAction):
    cost = 8500
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(2)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)

class ExitBrakePointForRequest3(PlannedAction):
    cost = 8000
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(3)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)

class ExitBrakePointForRequest4(PlannedAction):
    cost = 7500
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(4)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)

class ExitBrakePointForRequest5(PlannedAction):
    cost = 7000
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(5)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)

class ExitBrakePointForRequest6(PlannedAction):
    cost = 6500
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(6)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)

class ExitBrakePointForRequest7(PlannedAction):
    cost = 6000
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(7)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)

class ExitBrakePointForRequest8(PlannedAction):
    cost = 5500
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(8)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)

class ExitBrakePointForRequest9(PlannedAction):
    cost = 4000
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(9)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)

class ExitBrakePointForRequest10(PlannedAction):
    cost = 3800
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(10)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)

class ExitBrakePointForRequest11(PlannedAction):
    cost = 3650
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(11)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)
        
class ExitBrakePointForRequest12(PlannedAction):
    cost = 3500
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(12)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)
        
class ExitBrakePointForRequest13(PlannedAction):
    cost = 3250
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(13)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)

class ExitBrakePointForRequest14(PlannedAction):
    cost = 3000
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(14)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)
        
class ExitBrakePointForRequest15(PlannedAction):
    cost = 2850
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(15)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)
        
class ExitBrakePointForRequest16(PlannedAction):
    cost = 2500
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(16)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)
        
class ExitBrakePointForRequest17(PlannedAction):
    cost = 2250
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(17)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)
        

class ExitBrakePointForRequest20(PlannedAction):
    cost = 2000
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(20)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)


#class SchedullerCreatesPod(PlannedAction):
# class updatePodMetricsReleaseStarted(PlannedAction):
#     cost = 1
#     request1    = Select( Request.status == resourcesReleased)
#     podCurrent  = Select( Pod == request1.atPod)
#     nodeCurrent = Select( Node == podCurrent.atNode)
    
    
#     def effect(self):
#         self.request1.status.set(requestReleasedLimitsUpdateStarted)
#         self.request1.atPod.unset()
#         self.request1.atNode.unset()

# class IncreasePodConsumtionStart(PlannedAction):
#     cost = 1
#     request1 = Request.status == atPodInput
    
#     def selector(self):
#         return self.request1.status == atPodInputStartCalc

#     def effect(self):
#         self.request1.cpuCalculation = self.request1.cpuRequest
#             request1 = request1.cpuCalculation == request1.

    
class Problem1(KubeBase):
    def actions(self):
        return [
            ToLoadbalancer, 
            DirectToNode, 
            ToNode, 
            SwitchToNextNode, 
            DirectToPod, 
            ToPod, 
            SwitchToNextPod, 
            ConsumeResourceMem, 
            ConsumeResourceCpu, 
            ConsumeResource, 
            ProcessTempRequest, 
            ProcessPersistentRequest, 
            ReleaseResourceCpu, 
            ReleaseResourceMem, 
            ReleasedResources, 
            FinishRequest, 
            TerminatePodAfterFinish, 
            TerminatePod, 
            ReadDeploymentConfig, 
            CreatePodManually, 
            SchedulerNofityUnboundedPod, 
            KubectlStartsPod, 
            MarkPodAsOverwhelmingMemLimits, 
            MarkPodAsNonoverwhelmingMemLimits, 
            MemoryErrorKillPodOverwhelmingLimits, 
            MemoryErrorKillPodNotOverwhelmingLimits, 
            PodFailsBecauseOfKilling, 
            PodSucceds, 
            KubectlRecoverPod, 
            PodGarbageCollectedFailedPod, 
            PodGarbageCollectedSuccededPod, 
            ExitBrakePointForRequest1,
            ExitBrakePointForRequest2,
            ExitBrakePointForRequest3,
            ExitBrakePointForRequest4,
            ExitBrakePointForRequest5,
            ExitBrakePointForRequest6,
            ExitBrakePointForRequest7,
            ExitBrakePointForRequest8,
            ExitBrakePointForRequest9,
            ExitBrakePointForRequest10,
            ExitBrakePointForRequest11,
            ExitBrakePointForRequest12,
            ExitBrakePointForRequest13,
            ExitBrakePointForRequest14,
            ExitBrakePointForRequest15,
            ExitBrakePointForRequest16,
            ExitBrakePointForRequest17,
            ExitBrakePointForRequest20
            ]

    def problem(self):
        self.numberFactory = NumberFactory()
        self.prepareNumbers()
        self.statusReqAtStart = self.addObject(Status())
        self.statusReqAtLoadbalancer = self.addObject(Status())
        self.statusReqAtKubeproxy = self.addObject(Status())
        self.statusReqAtPodInput = self.addObject(Status())
        self.statusReqMemResourceConsumed = self.addObject(Status())
        self.statusReqCpuResourceConsumed = self.addObject(Status())
        self.statusReqResourcesConsumed = self.addObject(Status())
        self.statusReqDirectedToPod = self.addObject(Status())
        self.statusReqRequestPIDToBeEnded = self.addObject(Status())
        self.statusReqCpuResourceReleased = self.addObject(Status())
        self.statusReqMemResourceReleased = self.addObject(Status())
        self.statusReqResourcesReleased = self.addObject(Status())
        
        self.statusReqRequestTerminated = self.addObject(Status())
        self.statusReqRequestFinished = self.addObject(Status())
        
        self.statusReqAtStart.sequence =  self.numberFactory.getNumber(1)
        self.statusReqAtLoadbalancer.sequence =  self.numberFactory.getNumber(2)
        self.statusReqAtKubeproxy.sequence =  self.numberFactory.getNumber(3)
        self.statusReqAtPodInput.sequence =  self.numberFactory.getNumber(4)
        self.statusReqMemResourceConsumed.sequence =  self.numberFactory.getNumber(5)
        self.statusReqCpuResourceConsumed.sequence =  self.numberFactory.getNumber(6)
        self.statusReqResourcesConsumed.sequence =  self.numberFactory.getNumber(7)
        self.statusReqDirectedToPod.sequence =  self.numberFactory.getNumber(8)
        self.statusReqRequestPIDToBeEnded.sequence =  self.numberFactory.getNumber(9)
        self.statusReqCpuResourceReleased.sequence =  self.numberFactory.getNumber(10)
        self.statusReqMemResourceReleased.sequence =  self.numberFactory.getNumber(11)
        self.statusReqResourcesReleased.sequence =  self.numberFactory.getNumber(12)
        self.statusReqRequestTerminated.sequence =  self.numberFactory.getNumber(13)
        self.statusReqRequestFinished.sequence =  self.numberFactory.getNumber(20)
        

        self.statusPodAtConfig = self.addObject(Status())
        self.statusPodActive = self.addObject(Status())
        self.statusPodPending = self.addObject(Status())
        self.statusPodAtManualCreation = self.addObject(Status())
        self.statusPodDirectedToNode = self.addObject(Status())
        self.statusPodBindedToNode = self.addObject(Status())
        self.statusPodRunning = self.addObject(Status())
        self.statusNodeOomKilling = self.addObject(Status())
        self.statusNodeFailed = self.addObject(Status())
        self.statusNodeRunning = self.addObject(Status())
        self.statusNodeSucceded = self.addObject(Status())
        self.statusNodePending = self.addObject(Status())
        self.statusNodeDeleted = self.addObject(Status())
        self.statusPodInactive = self.addObject(Status())
        
        self.statusNodeActive = self.addObject(Status())
        self.statusNodeInactive = self.addObject(Status())
        
        self.statePodActive = self.addObject(State())
        self.statePodInactive = self.addObject(State())
        self.stateRequestActive = self.addObject(State())
        self.stateRequestInactive = self.addObject(State())
        self.stateNodeActive = self.addObject(State())
        self.stateNodeInactive = self.addObject(State())
        
        
        
        self.typeTemporary = self.addObject(Type())
        self.typePersistent = self.addObject(Type())
        

        self.period1 = self.addObject(Period()) 
        
        self.сontainerConfig1 = self.addObject(ContainerConfig())
        self.сontainerConfig2 = self.addObject(ContainerConfig())
        self.сontainerConfig3 = self.addObject(ContainerConfig())
        
        
        
        self.node1 = self.addObject(Node())
        self.node1.state = self.stateNodeActive
        self.node1.status = self.statusNodeActive ##TODO - make Node activation mechanism
        self.node1.cpuCapacity = self.numberFactory.getNumber(5)
        self.node1.memCapacity = self.numberFactory.getNumber(5)
        self.node1.currentFormalCpuConsumption = self.numberFactory.getNumber(0)
        self.node1.currentFormalMemConsumption = self.numberFactory.getNumber(0)
        self.node1.currentRealMemConsumption = self.numberFactory.getNumber(0)
        self.node1.currentRealCpuConsumption = self.numberFactory.getNumber(0)
        self.node1.AmountOfPodsOverwhelmingMemLimits = self.numberFactory.getNumber(0)

        self.node2 = self.addObject(Node())
        self.node2.state = self.stateNodeActive
        self.node2.status = self.statusNodeActive
        self.node2.cpuCapacity = self.numberFactory.getNumber(6)
        self.node2.memCapacity = self.numberFactory.getNumber(6)
        self.node2.currentFormalCpuConsumption = self.numberFactory.getNumber(0)
        self.node2.currentFormalMemConsumption = self.numberFactory.getNumber(0)
        self.node2.currentRealMemConsumption = self.numberFactory.getNumber(0)
        self.node2.currentRealCpuConsumption = self.numberFactory.getNumber(0)
        self.node2.AmountOfPodsOverwhelmingMemLimits = self.numberFactory.getNumber(0)
        
        self.node3 = self.addObject(Node())
        self.node3.state = self.stateNodeActive
        self.node3.status = self.statusNodeActive        
        self.node3.cpuCapacity = self.numberFactory.getNumber(7)
        self.node3.memCapacity = self.numberFactory.getNumber(7)
        self.node3.currentFormalCpuConsumption = self.numberFactory.getNumber(0)
        self.node3.currentFormalMemConsumption = self.numberFactory.getNumber(0)
        self.node3.currentRealMemConsumption = self.numberFactory.getNumber(0)
        self.node3.currentRealCpuConsumption = self.numberFactory.getNumber(0)
        self.node3.AmountOfPodsOverwhelmingMemLimits = self.numberFactory.getNumber(0)
        
        
        self.pod1 = self.addObject(Pod())
        self.pod1.podConfig = self.сontainerConfig1
        self.pod1.currentRealCpuConsumption = self.numberFactory.getNumber(0)
        self.pod1.currentRealMemConsumption = self.numberFactory.getNumber(0)
        self.pod1.status = self.statusPodAtConfig
        self.pod1.state = self.statePodInactive
        self.pod1.requestedMem = self.numberFactory.getNumber(1)
        self.pod1.requestedCpu = self.numberFactory.getNumber(2)
        self.pod1.podNotOverwhelmingLimits = True
        self.pod1.realInitialMemConsumption = self.numberFactory.getNumber(1)
        self.pod1.realInitialCpuConsumption = self.numberFactory.getNumber(1)
        self.pod1.type = self.typeTemporary
        self.pod1.memLimit =  self.numberFactory.getNumber(3)
        self.pod1.cpuLimit =  self.numberFactory.getNumber(3)
        
        self.pod2 = self.addObject(Pod())
        self.pod2.podConfig = self.сontainerConfig2
        self.pod2.currentRealCpuConsumption = self.numberFactory.getNumber(0)
        self.pod2.currentRealMemConsumption = self.numberFactory.getNumber(0)
        self.pod2.status = self.statusPodAtConfig
        self.pod2.state = self.statePodInactive
        self.pod2.requestedMem = self.numberFactory.getNumber(1)
        self.pod2.requestedCpu = self.numberFactory.getNumber(2)
        self.pod2.podNotOverwhelmingLimits = True
        self.pod2.realInitialMemConsumption = self.numberFactory.getNumber(1)
        self.pod2.realInitialCpuConsumption = self.numberFactory.getNumber(1)        
        self.pod2.type = self.typeTemporary
        self.pod2.memLimit =  self.numberFactory.getNumber(3)
        self.pod2.cpuLimit =  self.numberFactory.getNumber(3)
         
        ## to-do:  for relations  it should give helpful error message when = instead of add.
        
        self.pod3 = self.addObject(Pod())
        self.pod3.podConfig = self.сontainerConfig3
        self.pod3.currentRealCpuConsumption = self.numberFactory.getNumber(0)
        self.pod3.currentRealMemConsumption = self.numberFactory.getNumber(0)
        self.pod3.status = self.statusPodAtConfig
        self.pod3.state = self.statePodInactive
        self.pod3.requestedMem = self.numberFactory.getNumber(1)
        self.pod3.requestedCpu = self.numberFactory.getNumber(1)
        self.pod3.podNotOverwhelmingLimits = True
        self.pod3.realInitialMemConsumption = self.numberFactory.getNumber(1)
        self.pod3.realInitialCpuConsumption = self.numberFactory.getNumber(1)
        self.pod3.type = self.typePersistent
        self.pod3.memLimit =  self.numberFactory.getNumber(3)
        self.pod3.cpuLimit =  self.numberFactory.getNumber(3)

        self.service1 = self.addObject(Service())
        self.service2 = self.addObject(Service())
        self.service3 = self.addObject(Service())

        self.сontainerConfig1.service = self.service1
        self.сontainerConfig2.service = self.service2   
        self.сontainerConfig3.service = self.service3

        
        self.request1 = self.addObject(Request())
        self.request1.launchPeriod = self.period1
        self.request1.status = self.statusReqAtStart
        self.request1.state = self.stateRequestInactive
        self.request1.targetService = self.service1
        self.request1.cpuRequest = self.numberFactory.getNumber(1)
        self.request1.memRequest = self.numberFactory.getNumber(1)
        self.request1.type = self.typeTemporary

        self.request2 = self.addObject(Request())
        self.request2.launchPeriod = self.period1
        self.request2.status = self.statusReqAtStart
        self.request2.state = self.stateRequestInactive
        self.request2.targetService = self.service1
        self.request2.cpuRequest = self.numberFactory.getNumber(1)
        self.request2.memRequest = self.numberFactory.getNumber(1)
        self.request2.type = self.typeTemporary


        self.request3 = self.addObject(Request())
        self.request3.launchPeriod = self.period1
        self.request3.status = self.statusReqAtStart
        self.request3.state = self.stateRequestInactive
        self.request3.targetService = self.service2
        self.request3.cpuRequest = self.numberFactory.getNumber(1)
        self.request3.memRequest = self.numberFactory.getNumber(1)
        self.request3.type = self.typePersistent


        self.request4 = self.addObject(Request())
        self.request4.launchPeriod = self.period1
        self.request4.status = self.statusReqAtStart
        self.request4.state = self.stateRequestInactive
        self.request4.targetService = self.service2
        self.request4.cpuRequest = self.numberFactory.getNumber(1)
        self.request4.memRequest = self.numberFactory.getNumber(1)
        self.request4.type = self.typePersistent
        
        self.request5 = self.addObject(Request())
        self.request5.launchPeriod = self.period1
        self.request5.status = self.statusReqAtStart
        self.request5.state = self.stateRequestInactive
        self.request5.targetService = self.service2
        self.request5.cpuRequest = self.numberFactory.getNumber(1)
        self.request5.memRequest = self.numberFactory.getNumber(1)
        self.request5.type = self.typePersistent
        
        self.request6 = self.addObject(Request())
        self.request6.launchPeriod = self.period1
        self.request6.status = self.statusReqAtStart
        self.request6.state = self.stateRequestInactive
        self.request6.targetService = self.service2
        self.request6.cpuRequest = self.numberFactory.getNumber(1)
        self.request6.memRequest = self.numberFactory.getNumber(1)
        self.request6.type = self.typePersistent
        
        self.request7 = self.addObject(Request())
        self.request7.launchPeriod = self.period1
        self.request7.status = self.statusReqAtStart
        self.request7.state = self.stateRequestInactive
        self.request7.targetService = self.service2
        self.request7.cpuRequest = self.numberFactory.getNumber(1)
        self.request7.memRequest = self.numberFactory.getNumber(1)
        self.request7.type = self.typePersistent
        

        self.request8 = self.addObject(Request())
        self.request8.launchPeriod = self.period1
        self.request8.status = self.statusReqAtStart
        self.request8.state = self.stateRequestInactive
        self.request8.targetService = self.service2
        self.request8.cpuRequest = self.numberFactory.getNumber(1)
        self.request8.memRequest = self.numberFactory.getNumber(1)
        self.request8.type = self.typePersistent
        

        self.request9 = self.addObject(Request())
        self.request9.launchPeriod = self.period1
        self.request9.status = self.statusReqAtStart
        self.request9.state = self.stateRequestInactive
        self.request9.targetService = self.service2
        self.request9.cpuRequest = self.numberFactory.getNumber(1)
        self.request9.memRequest = self.numberFactory.getNumber(1)
        self.request9.type = self.typePersistent


        self.request10 = self.addObject(Request())
        self.request10.launchPeriod = self.period1
        self.request10.status = self.statusReqAtStart
        self.request10.state = self.stateRequestInactive
        self.request10.targetService = self.service2
        self.request10.cpuRequest = self.numberFactory.getNumber(1)
        self.request10.memRequest = self.numberFactory.getNumber(1)
        self.request10.type = self.typePersistent

        self.request11 = self.addObject(Request())
        self.request11.launchPeriod = self.period1
        self.request11.status = self.statusReqAtStart
        self.request11.state = self.stateRequestInactive
        self.request11.targetService = self.service2
        self.request11.cpuRequest = self.numberFactory.getNumber(1)
        self.request11.memRequest = self.numberFactory.getNumber(1)
        self.request11.type = self.typePersistent
#Todo: request of pod are temporary ? 

        self.lb1 = self.addObject(Loadbalancer())
        self.lb1.atNode = self.node1
        self.lb1.selectionedService.add(self.service1)
        self.lb1.selectionedService.add(self.service2)
        self.lb1.selectionedService.add(self.service3)
        
        self.modeUsermode = self.addObject(Mode())
        self.modeIptables = self.addObject(Mode())
        
        
        self.kp1 = self.addObject(Kubeproxy())
        self.kp1.mode = self.modeUsermode
        self.kp1.atNode = self.node1
        self.kp1.selectionedPod.add(self.pod1)
        self.kp1.selectionedService.add(self.service1) 
        ## how to create relations??? 
        
        self.kp2 = self.addObject(Kubeproxy())
        self.kp2.mode = self.modeUsermode
        self.kp2.atNode = self.node2
        self.kp2.selectionedPod.add(self.pod1)
        self.kp2.selectionedPod.add(self.pod2)
        self.kp2.selectionedService.add(self.service2)

        self.kp3 = self.addObject(Kubeproxy())
        self.kp3.mode = self.modeUsermode
        self.kp3.atNode = self.node3
        self.kp3.selectionedPod.add(self.pod1)
        self.kp2.selectionedPod.add(self.pod3)
        self.kp3.selectionedService.add(self.service1)
        self.kp3.selectionedService.add(self.service2)

    def goal(self):
        return self.request1.status == self.statusReqRequestFinished and \
        self.request2.status == self.statusReqRequestFinished and \
        self.request3.status == self.statusReqRequestFinished and \
        self.request4.status == self.statusReqRequestFinished and \
        self.request5.status == self.statusReqRequestFinished and \
        self.request6.status == self.statusReqRequestFinished and \
        self.request7.status == self.statusReqRequestFinished and \
        self.request8.status == self.statusReqRequestFinished and \
        self.request9.status == self.statusReqRequestFinished and \
        self.request10.status == self.statusReqRequestFinished and \
        self.request11.status == self.statusReqRequestFinished

p = Problem1()
retCode = p.run()