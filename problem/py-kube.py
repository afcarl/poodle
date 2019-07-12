from poodle.poodle import * 
from object.commonObject import *
from object.addedNumbers import *

class NumberFactory():
    numberCollection = {}

    def __init__(self, num=1001):
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

class ConsumeResource(PlannedAction):
    cost = 1
    request1 =  Request()
    currentPod = Select( Pod == request1.atPod)
    currentNode = Select( Node == request1.atNode)

    addedCpuConsumptionAtCurrentPod1 = Select( AddedNumber.operator1 == currentPod.currentRealCpuConsumption)
    addedCpuConsumptionAtCurrentPod1_res = Select(  Number == addedCpuConsumptionAtCurrentPod1.result)
    
    addedMemConsumptionAtCurrentPod1 = Select( AddedNumber.operator1 == currentPod.currentRealMemConsumption) 
    addedMemConsumptionAtCurrentPod1_res = Select(  Number == addedMemConsumptionAtCurrentPod1.result)
    
    addedCpuConsumptionAtCurrentNode1 = Select( AddedNumber.operator1 == currentNode.currentRealCpuConsumption) 
    addedCpuConsumptionAtCurrentNode1_res = Select(  Number == addedCpuConsumptionAtCurrentNode1.result)
    
    addedMemConsumptionAtCurrentNode1 = Select( AddedNumber.operator1 == currentNode.currentRealMemConsumption)
    addedMemConsumptionAtCurrentNode1_res = Select(  Number == addedMemConsumptionAtCurrentNode1.result)
    
    #KB: RealCPUConsumption - is consumption calculated per active requests ( each request adds some level of consumption, realy on the CPU/Mem
    #KB: RealCPUConsumption - it is tracked for pod and node . Both. this is used by autoscale and scheduller and kubectl  while starting pods on node
    #KB: FormalCPUConcumption - it is consumption calculated for nodes only. Pods when try to start shoul check limits by this value.  
    
    def selector(self):
        return Select( self.request1.status == self.problem.statusReqAtPodInput and \
        self.addedCpuConsumptionAtCurrentPod1.operator2 == self.request1.cpuRequest and \
        self.addedMemConsumptionAtCurrentPod1.operator2 == self.request1.memRequest and \
        self.addedCpuConsumptionAtCurrentNode1.operator2 == self.request1.cpuRequest and \
        self.addedMemConsumptionAtCurrentNode1.operator2 == self.request1.memRequest )        


    def effect(self):
        self.request1.status.set(self.problem.statusReqResourcesConsumed)
        self.currentPod.currentRealCpuConsumption.set(self.addedCpuConsumptionAtCurrentPod1_res)
        self.currentPod.currentRealMemConsumption.set(self.addedMemConsumptionAtCurrentPod1_res)
        self.currentNode.currentRealCpuConsumption.set(self.addedCpuConsumptionAtCurrentNode1_res)
        self.currentNode.currentRealMemConsumption.set(self.addedMemConsumptionAtCurrentNode1_res)
 

class ProcessTempRequest(PlannedAction):
    cost = 1
    request1 = Request()
    
    def selector(self):
        return Select( self.request1.type == self.problem.typeTemporary and \
        self.request1.status == self.problem.statusReqResourcesConsumed)
    
    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestPIDToBeEnded)
        
class ProcessPersistentRequest(PlannedAction):
    cost = 1
    request1 = Request()
    
    def selector(self):
        return Select( self.request1.status == self.problem.statusReqResourcesConsumed and \
        self.request1.type != self.problem.typeTemporary)

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)


class ReleaseResource(PlannedAction):
    cost = 1
    request1 = Request() 
    currentPod = Select( Pod == request1.atPod)
    currentNode = Select( Node == request1.atNode)

    reducedCpuConsumptionAtCurrentPod1 = Select( AddedNumber.result == currentPod.currentRealCpuConsumption)
    reducedCpuConsumptionAtCurrentPod1_op1 = Select (Number == reducedCpuConsumptionAtCurrentPod1.operator1)
    
    reducedMemConsumptionAtCurrentPod1 = Select( AddedNumber.result == currentPod.currentRealMemConsumption) 
    reducedMemConsumptionAtCurrentPod1_op1 = Select (Number == reducedMemConsumptionAtCurrentPod1.operator1)
    
    reducedCpuConsumptionAtCurrentNode1 = Select( AddedNumber.result == currentNode.currentRealCpuConsumption) 
    reducedCpuConsumptionAtCurrentNode1_op1 = Select (Number == reducedCpuConsumptionAtCurrentNode1.operator1)
    
    reducedMemConsumptionAtCurrentNode1 = Select( AddedNumber.result == currentNode.currentRealMemConsumption)
    reducedMemConsumptionAtCurrentNode1_op1 = Select (Number == reducedMemConsumptionAtCurrentNode1.operator1)
    def selector(self):
        return Select( self.request1.status == self.problem.statusReqRequestPIDToBeEnded and \
        self.reducedCpuConsumptionAtCurrentPod1.operator2 == self.request1.cpuRequest and \
        self.reducedMemConsumptionAtCurrentPod1.operator2 == self.request1.memRequest and \
        self.reducedCpuConsumptionAtCurrentNode1.operator2 == self.request1.cpuRequest and \
        self.reducedMemConsumptionAtCurrentNode1.operator2 == self.request1.memRequest)


    def effect(self):
        self.request1.status.set(self.problem.statusReqResourcesReleased)
        self.currentPod.currentRealCpuConsumption.set(self.reducedCpuConsumptionAtCurrentPod1_op1)
        self.currentPod.currentRealMemConsumption.set(self.reducedMemConsumptionAtCurrentPod1_op1)
        self.currentNode.currentRealCpuConsumption.set(self.reducedCpuConsumptionAtCurrentNode1_op1)
        self.currentNode.currentRealMemConsumption.set(self.reducedMemConsumptionAtCurrentNode1_op1) 

class FinishRequest(PlannedAction):
    cost = 1
    request1 = Request()
    pod1 = Select( Pod == request1.atPod)
    node1 = Select( Node == request1.atNode)
    
    
    def selector(self):
        return Select( self.request1.status == self.problem.statusReqResourcesReleased and \
         self.pod1.podIsOnetime != True)
    
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
        self.pod1.podIsOnetime == True)
        
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
    # NodeWithSomefreeMem_op1 = AddedNumber.Select(operator2 = node1.currentFormalMemConsumption, result = node1.memCapacity)
    # NodeWithSomefreeCpu_op1 = AddedNumber.Select(operator2 = node1.currentFormalCpuConsumption, result = node1.cpuCapacity)
    # checkThatfreeMemIsEnoughForPodLaunch_op1 =  AddedNumber.Select(operator2 = pod1.requestedMem, result = NodeWithSomefreeMem_op1.operator1)
    # checkThatfreeCpuIsEnoughForPodLaunch_op1 = AddedNumber.Select(operator2 = pod1.requestedCpu, result = NodeWithSomefreeCpu_op1.operator1)
    newFormalMemConsumptionAtNode_res = AddedNumber.Select(operator1 = node1.currentFormalMemConsumption, operator2 = pod1.requestedMem)
    newFormalCpuConsumptionAtNode_res = AddedNumber.Select(operator1 = node1.currentFormalCpuConsumption, operator2 = pod1.requestedCpu)
    newFormalMemConsumptionAtNode_res_num = Select(Number == newFormalMemConsumptionAtNode_res.result)
    newFormalCpuConsumptionAtNode_res_num = Select(Number == newFormalCpuConsumptionAtNode_res.result)
    
    #to-do: Soft conditions are not supported yet ( prioritization of nodes :  for example healthy  nodes are selected  rather then non healthy if pod  requests such behavior 
    def selector(self):
        return Select( self.pod1.status == self.problem.statusPodPending)
    
    def effect(self):
        self.pod1.status.set(self.problem.statusPodBindedToNode)
        self.pod1.bindedToNode.set(self.node1)
        self.node1.currentFormalMemConsumption.set(self.newFormalMemConsumptionAtNode_res_num)
        self.node1.currentFormalCpuConsumption.set(self.newFormalCpuConsumptionAtNode_res_num)

class KubectlStartsPod(PlannedAction):
    pod1 = Pod()
    
    # consume real resources from node
    node1 = Select( Node == pod1.bindedToNode)
    newMemRealConsumptionAtNode_res = Select(AddedNumber.operator1 == node1.currentRealMemConsumption)
    newMemRealConsumptionAtNode_res_res = Select( Number == newMemRealConsumptionAtNode_res.result)
    newCpuRealConsumptionAtNode_res = Select(AddedNumber.operator1 == node1.currentRealCpuConsumption)
    newCpuRealConsumptionAtNode_res_res = Select( Number == newCpuRealConsumptionAtNode_res.result)
    
    def selector(self):
        return Select(self.pod1.status == self.problem.statusPodBindedToNode and \
        self.newMemRealConsumptionAtNode_res.operator2 == self.pod1.realInitialMemConsumption and \
        self.newCpuRealConsumptionAtNode_res.operator2 == self.pod1.realInitialCpuConsumption)
    
    def effect(self):
        self.pod1.status.set(self.problem.statusPodRunning)
        self.pod1.state.set(self.problem.statePodActive)
        self.pod1.atNode.set(self.node1)
        self.pod1.bindedToNode.unset(self.node1)
        self.node1.currentRealMemConsumption.set(self.newMemRealConsumptionAtNode_res_res)
        self.node1.currentRealCpuConsumption.set(self.newCpuRealConsumptionAtNode_res_res)

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

class ExitBrakePointForRequest1AtStart(PlannedAction):
    cost = 9000
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(1)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)

class ExitBrakePointForRequest2AtLoadbalancer(PlannedAction):
    cost = 8500
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(2)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)

class ExitBrakePointForRequest3AtKubeproxy(PlannedAction):
    cost = 8000
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(3)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)

class ExitBrakePointForRequest4AtPodInput(PlannedAction):
    cost = 7500
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(4)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)

class ExitBrakePointForRequest5ResourcesConsumed(PlannedAction):
    cost = 7000
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(5)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)

class ExitBrakePointForRequest6DirectedToPod(PlannedAction):
    cost = 6500
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(6)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)

class ExitBrakePointForRequest7RequestPIDToBeEnded(PlannedAction):
    cost = 6000
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(7)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)

class ExitBrakePointForRequest8ResourcesReleased(PlannedAction):
    cost = 5500
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(8)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)

class ExitBrakePointForRequest9RequestTerminated(PlannedAction):
    cost = 4000
    request1 = Request()
    status1 = Select( Status == request1.status)
    def selector(self):
        return Select( self.status1.sequence == self.problem.numberFactory.getNumber(9)) 

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)
        
class ExitBrakePointForRequest20RequestFinished(PlannedAction):
    cost = 3500
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
            ConsumeResource, 
            ProcessTempRequest, 
            ProcessPersistentRequest, 
            ReleaseResource, 
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
            ExitBrakePointForRequest1AtStart,
            ExitBrakePointForRequest2AtLoadbalancer,
            ExitBrakePointForRequest3AtKubeproxy,
            ExitBrakePointForRequest4AtPodInput,
            ExitBrakePointForRequest5ResourcesConsumed,
            ExitBrakePointForRequest6DirectedToPod,
            ExitBrakePointForRequest7RequestPIDToBeEnded,
            ExitBrakePointForRequest8ResourcesReleased,
            ExitBrakePointForRequest9RequestTerminated,
            ExitBrakePointForRequest20RequestFinished
            ]

    def problem(self):
        self.numberFactory = NumberFactory()
        self.prepareNumbers()
        self.statusReqAtStart = self.addObject(Status())
        self.statusReqAtLoadbalancer = self.addObject(Status())
        self.statusReqAtKubeproxy = self.addObject(Status())
        self.statusReqAtPodInput = self.addObject(Status())
        self.statusReqResourcesConsumed = self.addObject(Status())
        self.statusReqDirectedToPod = self.addObject(Status())
        self.statusReqRequestPIDToBeEnded = self.addObject(Status())
        self.statusReqResourcesReleased = self.addObject(Status())
        self.statusReqRequestTerminated = self.addObject(Status())
        self.statusReqRequestFinished = self.addObject(Status())
        
        self.statusReqAtStart.sequence =  self.numberFactory.getNumber(1)
        self.statusReqAtLoadbalancer.sequence =  self.numberFactory.getNumber(2)
        self.statusReqAtKubeproxy.sequence =  self.numberFactory.getNumber(3)
        self.statusReqAtPodInput.sequence =  self.numberFactory.getNumber(4)
        self.statusReqResourcesConsumed.sequence =  self.numberFactory.getNumber(5)
        self.statusReqDirectedToPod.sequence =  self.numberFactory.getNumber(6)
        self.statusReqRequestPIDToBeEnded.sequence =  self.numberFactory.getNumber(7)
        self.statusReqResourcesReleased.sequence =  self.numberFactory.getNumber(8)
        self.statusReqRequestTerminated.sequence =  self.numberFactory.getNumber(9)
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
        

        self.period1 = self.addObject(Period()) 
        
        self.сontainerConfig1 = self.addObject(ContainerConfig())
        self.сontainerConfig2 = self.addObject(ContainerConfig())
        self.сontainerConfig3 = self.addObject(ContainerConfig())
        
        
        
        self.node1 = self.addObject(Node())
        self.node1.state = self.stateNodeActive
        self.node1.status = self.statusNodeActive ##TODO - make Node activation mechanism
        self.node1.cpuCapacity = self.numberFactory.getNumber(5)
        self.node1.memCapacity = self.numberFactory.getNumber(10)
        self.node1.currentFormalCpuConsumption = self.numberFactory.getNumber(0)
        self.node1.currentFormalMemConsumption = self.numberFactory.getNumber(0)
        self.node1.currentRealMemConsumption = self.numberFactory.getNumber(0)
        self.node1.currentRealCpuConsumption = self.numberFactory.getNumber(0)
        self.node1.AmountOfPodsOverwhelmingMemLimits = self.numberFactory.getNumber(0)

        self.node2 = self.addObject(Node())
        self.node2.state = self.stateNodeActive
        self.node2.status = self.statusNodeActive
        self.node2.cpuCapacity = self.numberFactory.getNumber(10)
        self.node2.memCapacity = self.numberFactory.getNumber(10)
        self.node2.currentFormalCpuConsumption = self.numberFactory.getNumber(0)
        self.node2.currentFormalMemConsumption = self.numberFactory.getNumber(0)
        self.node2.currentRealMemConsumption = self.numberFactory.getNumber(0)
        self.node2.currentRealCpuConsumption = self.numberFactory.getNumber(0)
        self.node2.AmountOfPodsOverwhelmingMemLimits = self.numberFactory.getNumber(0)
        
        self.node3 = self.addObject(Node())
        self.node3.state = self.stateNodeActive
        self.node3.status = self.statusNodeActive        
        self.node3.cpuCapacity = self.numberFactory.getNumber(10)
        self.node3.memCapacity = self.numberFactory.getNumber(10)
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
        
        self.pod2 = self.addObject(Pod())
        self.pod2.podConfig = self.сontainerConfig2
        self.pod2.currentRealCpuConsumption = self.numberFactory.getNumber(0)
        self.pod2.currentRealMemConsumption = self.numberFactory.getNumber(0)
        self.pod2.status = self.statusPodAtConfig
        self.pod2.state = self.statePodInactive
        self.pod2.requestedMem = self.numberFactory.getNumber(1)
        self.pod2.requestedCpu = self.numberFactory.getNumber(2)
        self.pod2.podNotOverwhelmingLimits = True
         
        ## to-do:  for relations  it should give helpful error message when = instead of add.
        
        self.pod3 = self.addObject(Pod())
        self.pod3.podConfig = self.сontainerConfig3
        self.pod3.currentRealCpuConsumption = self.numberFactory.getNumber(0)
        self.pod3.currentRealMemConsumption = self.numberFactory.getNumber(0)
        self.pod3.status = self.statusPodAtConfig
        self.pod3.state = self.statePodInactive
        self.pod3.requestedMem = self.numberFactory.getNumber(1)
        self.pod3.requestedCpu = self.numberFactory.getNumber(2)
        self.pod3.podNotOverwhelmingLimits = True
        
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

        self.request2 = self.addObject(Request())
        self.request2.launchPeriod = self.period1
        self.request2.status = self.statusReqAtStart
        self.request2.state = self.stateRequestInactive
        self.request2.targetService = self.service1

        self.request3 = self.addObject(Request())
        self.request3.launchPeriod = self.period1
        self.request3.status = self.statusReqAtStart
        self.request3.state = self.stateRequestInactive
        self.request3.targetService = self.service2

        self.request4 = self.addObject(Request())
        self.request4.launchPeriod = self.period1
        self.request4.status = self.statusReqAtStart
        self.request4.state = self.stateRequestInactive
        self.request4.targetService = self.service2
        
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
        
        
        self.AddedNumber0_0 = self.addObject(AddedNumber()) 
        self.AddedNumber0_0.operator1 =  self.numberFactory.getNumber(0) 
        self.AddedNumber0_0.operator2 =  self.numberFactory.getNumber(0) 
        self.AddedNumber0_0.result =  self.numberFactory.getNumber(0)

        self.AddedNumber0_1 = self.addObject(AddedNumber()) 
        self.AddedNumber0_1.operator1 =  self.numberFactory.getNumber(0) 
        self.AddedNumber0_1.operator2 =  self.numberFactory.getNumber(1) 
        self.AddedNumber0_1.result =  self.numberFactory.getNumber(1)

        self.AddedNumber0_2 = self.addObject(AddedNumber()) 
        self.AddedNumber0_2.operator1 =  self.numberFactory.getNumber(0) 
        self.AddedNumber0_2.operator2 =  self.numberFactory.getNumber(2) 
        self.AddedNumber0_2.result =  self.numberFactory.getNumber(2)

        self.AddedNumber0_3 = self.addObject(AddedNumber()) 
        self.AddedNumber0_3.operator1 =  self.numberFactory.getNumber(0) 
        self.AddedNumber0_3.operator2 =  self.numberFactory.getNumber(3) 
        self.AddedNumber0_3.result =  self.numberFactory.getNumber(3)

        self.AddedNumber0_4 = self.addObject(AddedNumber()) 
        self.AddedNumber0_4.operator1 =  self.numberFactory.getNumber(0) 
        self.AddedNumber0_4.operator2 =  self.numberFactory.getNumber(4) 
        self.AddedNumber0_4.result =  self.numberFactory.getNumber(4)

        self.AddedNumber0_5 = self.addObject(AddedNumber()) 
        self.AddedNumber0_5.operator1 =  self.numberFactory.getNumber(0) 
        self.AddedNumber0_5.operator2 =  self.numberFactory.getNumber(5) 
        self.AddedNumber0_5.result =  self.numberFactory.getNumber(5)

        self.AddedNumber0_6 = self.addObject(AddedNumber()) 
        self.AddedNumber0_6.operator1 =  self.numberFactory.getNumber(0) 
        self.AddedNumber0_6.operator2 =  self.numberFactory.getNumber(6) 
        self.AddedNumber0_6.result =  self.numberFactory.getNumber(6)

        self.AddedNumber0_7 = self.addObject(AddedNumber()) 
        self.AddedNumber0_7.operator1 =  self.numberFactory.getNumber(0) 
        self.AddedNumber0_7.operator2 =  self.numberFactory.getNumber(7) 
        self.AddedNumber0_7.result =  self.numberFactory.getNumber(7)

        self.AddedNumber0_8 = self.addObject(AddedNumber()) 
        self.AddedNumber0_8.operator1 =  self.numberFactory.getNumber(0) 
        self.AddedNumber0_8.operator2 =  self.numberFactory.getNumber(8) 
        self.AddedNumber0_8.result =  self.numberFactory.getNumber(8)

        self.AddedNumber0_9 = self.addObject(AddedNumber()) 
        self.AddedNumber0_9.operator1 =  self.numberFactory.getNumber(0) 
        self.AddedNumber0_9.operator2 =  self.numberFactory.getNumber(9) 
        self.AddedNumber0_9.result =  self.numberFactory.getNumber(9)

        self.AddedNumber0_10 = self.addObject(AddedNumber()) 
        self.AddedNumber0_10.operator1 =  self.numberFactory.getNumber(0) 
        self.AddedNumber0_10.operator2 =  self.numberFactory.getNumber(10) 
        self.AddedNumber0_10.result =  self.numberFactory.getNumber(10)

        self.AddedNumber1_0 = self.addObject(AddedNumber()) 
        self.AddedNumber1_0.operator1 =  self.numberFactory.getNumber(1) 
        self.AddedNumber1_0.operator2 =  self.numberFactory.getNumber(0) 
        self.AddedNumber1_0.result =  self.numberFactory.getNumber(1)

        self.AddedNumber1_1 = self.addObject(AddedNumber()) 
        self.AddedNumber1_1.operator1 =  self.numberFactory.getNumber(1) 
        self.AddedNumber1_1.operator2 =  self.numberFactory.getNumber(1) 
        self.AddedNumber1_1.result =  self.numberFactory.getNumber(2)

        self.AddedNumber1_2 = self.addObject(AddedNumber()) 
        self.AddedNumber1_2.operator1 =  self.numberFactory.getNumber(1) 
        self.AddedNumber1_2.operator2 =  self.numberFactory.getNumber(2) 
        self.AddedNumber1_2.result =  self.numberFactory.getNumber(3)

        self.AddedNumber1_3 = self.addObject(AddedNumber()) 
        self.AddedNumber1_3.operator1 =  self.numberFactory.getNumber(1) 
        self.AddedNumber1_3.operator2 =  self.numberFactory.getNumber(3) 
        self.AddedNumber1_3.result =  self.numberFactory.getNumber(4)

        self.AddedNumber1_4 = self.addObject(AddedNumber()) 
        self.AddedNumber1_4.operator1 =  self.numberFactory.getNumber(1) 
        self.AddedNumber1_4.operator2 =  self.numberFactory.getNumber(4) 
        self.AddedNumber1_4.result =  self.numberFactory.getNumber(5)

        self.AddedNumber1_5 = self.addObject(AddedNumber()) 
        self.AddedNumber1_5.operator1 =  self.numberFactory.getNumber(1) 
        self.AddedNumber1_5.operator2 =  self.numberFactory.getNumber(5) 
        self.AddedNumber1_5.result =  self.numberFactory.getNumber(6)

        self.AddedNumber1_6 = self.addObject(AddedNumber()) 
        self.AddedNumber1_6.operator1 =  self.numberFactory.getNumber(1) 
        self.AddedNumber1_6.operator2 =  self.numberFactory.getNumber(6) 
        self.AddedNumber1_6.result =  self.numberFactory.getNumber(7)

        self.AddedNumber1_7 = self.addObject(AddedNumber()) 
        self.AddedNumber1_7.operator1 =  self.numberFactory.getNumber(1) 
        self.AddedNumber1_7.operator2 =  self.numberFactory.getNumber(7) 
        self.AddedNumber1_7.result =  self.numberFactory.getNumber(8)

        self.AddedNumber1_8 = self.addObject(AddedNumber()) 
        self.AddedNumber1_8.operator1 =  self.numberFactory.getNumber(1) 
        self.AddedNumber1_8.operator2 =  self.numberFactory.getNumber(8) 
        self.AddedNumber1_8.result =  self.numberFactory.getNumber(9)

        self.AddedNumber1_9 = self.addObject(AddedNumber()) 
        self.AddedNumber1_9.operator1 =  self.numberFactory.getNumber(1) 
        self.AddedNumber1_9.operator2 =  self.numberFactory.getNumber(9) 
        self.AddedNumber1_9.result =  self.numberFactory.getNumber(10)

        self.AddedNumber1_10 = self.addObject(AddedNumber()) 
        self.AddedNumber1_10.operator1 =  self.numberFactory.getNumber(1) 
        self.AddedNumber1_10.operator2 =  self.numberFactory.getNumber(10) 
        self.AddedNumber1_10.result =  self.numberFactory.getNumber(11)

        self.AddedNumber2_0 = self.addObject(AddedNumber()) 
        self.AddedNumber2_0.operator1 =  self.numberFactory.getNumber(2) 
        self.AddedNumber2_0.operator2 =  self.numberFactory.getNumber(0) 
        self.AddedNumber2_0.result =  self.numberFactory.getNumber(2)

        self.AddedNumber2_1 = self.addObject(AddedNumber()) 
        self.AddedNumber2_1.operator1 =  self.numberFactory.getNumber(2) 
        self.AddedNumber2_1.operator2 =  self.numberFactory.getNumber(1) 
        self.AddedNumber2_1.result =  self.numberFactory.getNumber(3)

        self.AddedNumber2_2 = self.addObject(AddedNumber()) 
        self.AddedNumber2_2.operator1 =  self.numberFactory.getNumber(2) 
        self.AddedNumber2_2.operator2 =  self.numberFactory.getNumber(2) 
        self.AddedNumber2_2.result =  self.numberFactory.getNumber(4)

        self.AddedNumber2_3 = self.addObject(AddedNumber()) 
        self.AddedNumber2_3.operator1 =  self.numberFactory.getNumber(2) 
        self.AddedNumber2_3.operator2 =  self.numberFactory.getNumber(3) 
        self.AddedNumber2_3.result =  self.numberFactory.getNumber(5)

        self.AddedNumber2_4 = self.addObject(AddedNumber()) 
        self.AddedNumber2_4.operator1 =  self.numberFactory.getNumber(2) 
        self.AddedNumber2_4.operator2 =  self.numberFactory.getNumber(4) 
        self.AddedNumber2_4.result =  self.numberFactory.getNumber(6)

        self.AddedNumber2_5 = self.addObject(AddedNumber()) 
        self.AddedNumber2_5.operator1 =  self.numberFactory.getNumber(2) 
        self.AddedNumber2_5.operator2 =  self.numberFactory.getNumber(5) 
        self.AddedNumber2_5.result =  self.numberFactory.getNumber(7)

        self.AddedNumber2_6 = self.addObject(AddedNumber()) 
        self.AddedNumber2_6.operator1 =  self.numberFactory.getNumber(2) 
        self.AddedNumber2_6.operator2 =  self.numberFactory.getNumber(6) 
        self.AddedNumber2_6.result =  self.numberFactory.getNumber(8)

        self.AddedNumber2_7 = self.addObject(AddedNumber()) 
        self.AddedNumber2_7.operator1 =  self.numberFactory.getNumber(2) 
        self.AddedNumber2_7.operator2 =  self.numberFactory.getNumber(7) 
        self.AddedNumber2_7.result =  self.numberFactory.getNumber(9)

        self.AddedNumber2_8 = self.addObject(AddedNumber()) 
        self.AddedNumber2_8.operator1 =  self.numberFactory.getNumber(2) 
        self.AddedNumber2_8.operator2 =  self.numberFactory.getNumber(8) 
        self.AddedNumber2_8.result =  self.numberFactory.getNumber(10)

        self.AddedNumber2_9 = self.addObject(AddedNumber()) 
        self.AddedNumber2_9.operator1 =  self.numberFactory.getNumber(2) 
        self.AddedNumber2_9.operator2 =  self.numberFactory.getNumber(9) 
        self.AddedNumber2_9.result =  self.numberFactory.getNumber(11)

        self.AddedNumber2_10 = self.addObject(AddedNumber()) 
        self.AddedNumber2_10.operator1 =  self.numberFactory.getNumber(2) 
        self.AddedNumber2_10.operator2 =  self.numberFactory.getNumber(10) 
        self.AddedNumber2_10.result =  self.numberFactory.getNumber(12)

        self.AddedNumber3_0 = self.addObject(AddedNumber()) 
        self.AddedNumber3_0.operator1 =  self.numberFactory.getNumber(3) 
        self.AddedNumber3_0.operator2 =  self.numberFactory.getNumber(0) 
        self.AddedNumber3_0.result =  self.numberFactory.getNumber(3)

        self.AddedNumber3_1 = self.addObject(AddedNumber()) 
        self.AddedNumber3_1.operator1 =  self.numberFactory.getNumber(3) 
        self.AddedNumber3_1.operator2 =  self.numberFactory.getNumber(1) 
        self.AddedNumber3_1.result =  self.numberFactory.getNumber(4)

        self.AddedNumber3_2 = self.addObject(AddedNumber()) 
        self.AddedNumber3_2.operator1 =  self.numberFactory.getNumber(3) 
        self.AddedNumber3_2.operator2 =  self.numberFactory.getNumber(2) 
        self.AddedNumber3_2.result =  self.numberFactory.getNumber(5)

        self.AddedNumber3_3 = self.addObject(AddedNumber()) 
        self.AddedNumber3_3.operator1 =  self.numberFactory.getNumber(3) 
        self.AddedNumber3_3.operator2 =  self.numberFactory.getNumber(3) 
        self.AddedNumber3_3.result =  self.numberFactory.getNumber(6)

        self.AddedNumber3_4 = self.addObject(AddedNumber()) 
        self.AddedNumber3_4.operator1 =  self.numberFactory.getNumber(3) 
        self.AddedNumber3_4.operator2 =  self.numberFactory.getNumber(4) 
        self.AddedNumber3_4.result =  self.numberFactory.getNumber(7)

        self.AddedNumber3_5 = self.addObject(AddedNumber()) 
        self.AddedNumber3_5.operator1 =  self.numberFactory.getNumber(3) 
        self.AddedNumber3_5.operator2 =  self.numberFactory.getNumber(5) 
        self.AddedNumber3_5.result =  self.numberFactory.getNumber(8)

        self.AddedNumber3_6 = self.addObject(AddedNumber()) 
        self.AddedNumber3_6.operator1 =  self.numberFactory.getNumber(3) 
        self.AddedNumber3_6.operator2 =  self.numberFactory.getNumber(6) 
        self.AddedNumber3_6.result =  self.numberFactory.getNumber(9)

        self.AddedNumber3_7 = self.addObject(AddedNumber()) 
        self.AddedNumber3_7.operator1 =  self.numberFactory.getNumber(3) 
        self.AddedNumber3_7.operator2 =  self.numberFactory.getNumber(7) 
        self.AddedNumber3_7.result =  self.numberFactory.getNumber(10)

        self.AddedNumber3_8 = self.addObject(AddedNumber()) 
        self.AddedNumber3_8.operator1 =  self.numberFactory.getNumber(3) 
        self.AddedNumber3_8.operator2 =  self.numberFactory.getNumber(8) 
        self.AddedNumber3_8.result =  self.numberFactory.getNumber(11)

        self.AddedNumber3_9 = self.addObject(AddedNumber()) 
        self.AddedNumber3_9.operator1 =  self.numberFactory.getNumber(3) 
        self.AddedNumber3_9.operator2 =  self.numberFactory.getNumber(9) 
        self.AddedNumber3_9.result =  self.numberFactory.getNumber(12)

        self.AddedNumber3_10 = self.addObject(AddedNumber()) 
        self.AddedNumber3_10.operator1 =  self.numberFactory.getNumber(3) 
        self.AddedNumber3_10.operator2 =  self.numberFactory.getNumber(10) 
        self.AddedNumber3_10.result =  self.numberFactory.getNumber(13)

        self.AddedNumber4_0 = self.addObject(AddedNumber()) 
        self.AddedNumber4_0.operator1 =  self.numberFactory.getNumber(4) 
        self.AddedNumber4_0.operator2 =  self.numberFactory.getNumber(0) 
        self.AddedNumber4_0.result =  self.numberFactory.getNumber(4)

        self.AddedNumber4_1 = self.addObject(AddedNumber()) 
        self.AddedNumber4_1.operator1 =  self.numberFactory.getNumber(4) 
        self.AddedNumber4_1.operator2 =  self.numberFactory.getNumber(1) 
        self.AddedNumber4_1.result =  self.numberFactory.getNumber(5)

        self.AddedNumber4_2 = self.addObject(AddedNumber()) 
        self.AddedNumber4_2.operator1 =  self.numberFactory.getNumber(4) 
        self.AddedNumber4_2.operator2 =  self.numberFactory.getNumber(2) 
        self.AddedNumber4_2.result =  self.numberFactory.getNumber(6)

        self.AddedNumber4_3 = self.addObject(AddedNumber()) 
        self.AddedNumber4_3.operator1 =  self.numberFactory.getNumber(4) 
        self.AddedNumber4_3.operator2 =  self.numberFactory.getNumber(3) 
        self.AddedNumber4_3.result =  self.numberFactory.getNumber(7)

        self.AddedNumber4_4 = self.addObject(AddedNumber()) 
        self.AddedNumber4_4.operator1 =  self.numberFactory.getNumber(4) 
        self.AddedNumber4_4.operator2 =  self.numberFactory.getNumber(4) 
        self.AddedNumber4_4.result =  self.numberFactory.getNumber(8)

        self.AddedNumber4_5 = self.addObject(AddedNumber()) 
        self.AddedNumber4_5.operator1 =  self.numberFactory.getNumber(4) 
        self.AddedNumber4_5.operator2 =  self.numberFactory.getNumber(5) 
        self.AddedNumber4_5.result =  self.numberFactory.getNumber(9)

        self.AddedNumber4_6 = self.addObject(AddedNumber()) 
        self.AddedNumber4_6.operator1 =  self.numberFactory.getNumber(4) 
        self.AddedNumber4_6.operator2 =  self.numberFactory.getNumber(6) 
        self.AddedNumber4_6.result =  self.numberFactory.getNumber(10)

        self.AddedNumber4_7 = self.addObject(AddedNumber()) 
        self.AddedNumber4_7.operator1 =  self.numberFactory.getNumber(4) 
        self.AddedNumber4_7.operator2 =  self.numberFactory.getNumber(7) 
        self.AddedNumber4_7.result =  self.numberFactory.getNumber(11)

        self.AddedNumber4_8 = self.addObject(AddedNumber()) 
        self.AddedNumber4_8.operator1 =  self.numberFactory.getNumber(4) 
        self.AddedNumber4_8.operator2 =  self.numberFactory.getNumber(8) 
        self.AddedNumber4_8.result =  self.numberFactory.getNumber(12)

        self.AddedNumber4_9 = self.addObject(AddedNumber()) 
        self.AddedNumber4_9.operator1 =  self.numberFactory.getNumber(4) 
        self.AddedNumber4_9.operator2 =  self.numberFactory.getNumber(9) 
        self.AddedNumber4_9.result =  self.numberFactory.getNumber(13)

        self.AddedNumber4_10 = self.addObject(AddedNumber()) 
        self.AddedNumber4_10.operator1 =  self.numberFactory.getNumber(4) 
        self.AddedNumber4_10.operator2 =  self.numberFactory.getNumber(10) 
        self.AddedNumber4_10.result =  self.numberFactory.getNumber(14)

        self.AddedNumber5_0 = self.addObject(AddedNumber()) 
        self.AddedNumber5_0.operator1 =  self.numberFactory.getNumber(5) 
        self.AddedNumber5_0.operator2 =  self.numberFactory.getNumber(0) 
        self.AddedNumber5_0.result =  self.numberFactory.getNumber(5)

        self.AddedNumber5_1 = self.addObject(AddedNumber()) 
        self.AddedNumber5_1.operator1 =  self.numberFactory.getNumber(5) 
        self.AddedNumber5_1.operator2 =  self.numberFactory.getNumber(1) 
        self.AddedNumber5_1.result =  self.numberFactory.getNumber(6)

        self.AddedNumber5_2 = self.addObject(AddedNumber()) 
        self.AddedNumber5_2.operator1 =  self.numberFactory.getNumber(5) 
        self.AddedNumber5_2.operator2 =  self.numberFactory.getNumber(2) 
        self.AddedNumber5_2.result =  self.numberFactory.getNumber(7)

        self.AddedNumber5_3 = self.addObject(AddedNumber()) 
        self.AddedNumber5_3.operator1 =  self.numberFactory.getNumber(5) 
        self.AddedNumber5_3.operator2 =  self.numberFactory.getNumber(3) 
        self.AddedNumber5_3.result =  self.numberFactory.getNumber(8)

        self.AddedNumber5_4 = self.addObject(AddedNumber()) 
        self.AddedNumber5_4.operator1 =  self.numberFactory.getNumber(5) 
        self.AddedNumber5_4.operator2 =  self.numberFactory.getNumber(4) 
        self.AddedNumber5_4.result =  self.numberFactory.getNumber(9)

        self.AddedNumber5_5 = self.addObject(AddedNumber()) 
        self.AddedNumber5_5.operator1 =  self.numberFactory.getNumber(5) 
        self.AddedNumber5_5.operator2 =  self.numberFactory.getNumber(5) 
        self.AddedNumber5_5.result =  self.numberFactory.getNumber(10)

        self.AddedNumber5_6 = self.addObject(AddedNumber()) 
        self.AddedNumber5_6.operator1 =  self.numberFactory.getNumber(5) 
        self.AddedNumber5_6.operator2 =  self.numberFactory.getNumber(6) 
        self.AddedNumber5_6.result =  self.numberFactory.getNumber(11)

        self.AddedNumber5_7 = self.addObject(AddedNumber()) 
        self.AddedNumber5_7.operator1 =  self.numberFactory.getNumber(5) 
        self.AddedNumber5_7.operator2 =  self.numberFactory.getNumber(7) 
        self.AddedNumber5_7.result =  self.numberFactory.getNumber(12)

        self.AddedNumber5_8 = self.addObject(AddedNumber()) 
        self.AddedNumber5_8.operator1 =  self.numberFactory.getNumber(5) 
        self.AddedNumber5_8.operator2 =  self.numberFactory.getNumber(8) 
        self.AddedNumber5_8.result =  self.numberFactory.getNumber(13)

        self.AddedNumber5_9 = self.addObject(AddedNumber()) 
        self.AddedNumber5_9.operator1 =  self.numberFactory.getNumber(5) 
        self.AddedNumber5_9.operator2 =  self.numberFactory.getNumber(9) 
        self.AddedNumber5_9.result =  self.numberFactory.getNumber(14)

        self.AddedNumber5_10 = self.addObject(AddedNumber()) 
        self.AddedNumber5_10.operator1 =  self.numberFactory.getNumber(5) 
        self.AddedNumber5_10.operator2 =  self.numberFactory.getNumber(10) 
        self.AddedNumber5_10.result =  self.numberFactory.getNumber(15)

        self.AddedNumber6_0 = self.addObject(AddedNumber()) 
        self.AddedNumber6_0.operator1 =  self.numberFactory.getNumber(6) 
        self.AddedNumber6_0.operator2 =  self.numberFactory.getNumber(0) 
        self.AddedNumber6_0.result =  self.numberFactory.getNumber(6)

        self.AddedNumber6_1 = self.addObject(AddedNumber()) 
        self.AddedNumber6_1.operator1 =  self.numberFactory.getNumber(6) 
        self.AddedNumber6_1.operator2 =  self.numberFactory.getNumber(1) 
        self.AddedNumber6_1.result =  self.numberFactory.getNumber(7)

        self.AddedNumber6_2 = self.addObject(AddedNumber()) 
        self.AddedNumber6_2.operator1 =  self.numberFactory.getNumber(6) 
        self.AddedNumber6_2.operator2 =  self.numberFactory.getNumber(2) 
        self.AddedNumber6_2.result =  self.numberFactory.getNumber(8)

        self.AddedNumber6_3 = self.addObject(AddedNumber()) 
        self.AddedNumber6_3.operator1 =  self.numberFactory.getNumber(6) 
        self.AddedNumber6_3.operator2 =  self.numberFactory.getNumber(3) 
        self.AddedNumber6_3.result =  self.numberFactory.getNumber(9)

        self.AddedNumber6_4 = self.addObject(AddedNumber()) 
        self.AddedNumber6_4.operator1 =  self.numberFactory.getNumber(6) 
        self.AddedNumber6_4.operator2 =  self.numberFactory.getNumber(4) 
        self.AddedNumber6_4.result =  self.numberFactory.getNumber(10)

        self.AddedNumber6_5 = self.addObject(AddedNumber()) 
        self.AddedNumber6_5.operator1 =  self.numberFactory.getNumber(6) 
        self.AddedNumber6_5.operator2 =  self.numberFactory.getNumber(5) 
        self.AddedNumber6_5.result =  self.numberFactory.getNumber(11)

        self.AddedNumber6_6 = self.addObject(AddedNumber()) 
        self.AddedNumber6_6.operator1 =  self.numberFactory.getNumber(6) 
        self.AddedNumber6_6.operator2 =  self.numberFactory.getNumber(6) 
        self.AddedNumber6_6.result =  self.numberFactory.getNumber(12)

        self.AddedNumber6_7 = self.addObject(AddedNumber()) 
        self.AddedNumber6_7.operator1 =  self.numberFactory.getNumber(6) 
        self.AddedNumber6_7.operator2 =  self.numberFactory.getNumber(7) 
        self.AddedNumber6_7.result =  self.numberFactory.getNumber(13)

        self.AddedNumber6_8 = self.addObject(AddedNumber()) 
        self.AddedNumber6_8.operator1 =  self.numberFactory.getNumber(6) 
        self.AddedNumber6_8.operator2 =  self.numberFactory.getNumber(8) 
        self.AddedNumber6_8.result =  self.numberFactory.getNumber(14)

        self.AddedNumber6_9 = self.addObject(AddedNumber()) 
        self.AddedNumber6_9.operator1 =  self.numberFactory.getNumber(6) 
        self.AddedNumber6_9.operator2 =  self.numberFactory.getNumber(9) 
        self.AddedNumber6_9.result =  self.numberFactory.getNumber(15)

        self.AddedNumber6_10 = self.addObject(AddedNumber()) 
        self.AddedNumber6_10.operator1 =  self.numberFactory.getNumber(6) 
        self.AddedNumber6_10.operator2 =  self.numberFactory.getNumber(10) 
        self.AddedNumber6_10.result =  self.numberFactory.getNumber(16)

        self.AddedNumber7_0 = self.addObject(AddedNumber()) 
        self.AddedNumber7_0.operator1 =  self.numberFactory.getNumber(7) 
        self.AddedNumber7_0.operator2 =  self.numberFactory.getNumber(0) 
        self.AddedNumber7_0.result =  self.numberFactory.getNumber(7)

        self.AddedNumber7_1 = self.addObject(AddedNumber()) 
        self.AddedNumber7_1.operator1 =  self.numberFactory.getNumber(7) 
        self.AddedNumber7_1.operator2 =  self.numberFactory.getNumber(1) 
        self.AddedNumber7_1.result =  self.numberFactory.getNumber(8)

        self.AddedNumber7_2 = self.addObject(AddedNumber()) 
        self.AddedNumber7_2.operator1 =  self.numberFactory.getNumber(7) 
        self.AddedNumber7_2.operator2 =  self.numberFactory.getNumber(2) 
        self.AddedNumber7_2.result =  self.numberFactory.getNumber(9)

        self.AddedNumber7_3 = self.addObject(AddedNumber()) 
        self.AddedNumber7_3.operator1 =  self.numberFactory.getNumber(7) 
        self.AddedNumber7_3.operator2 =  self.numberFactory.getNumber(3) 
        self.AddedNumber7_3.result =  self.numberFactory.getNumber(10)

        self.AddedNumber7_4 = self.addObject(AddedNumber()) 
        self.AddedNumber7_4.operator1 =  self.numberFactory.getNumber(7) 
        self.AddedNumber7_4.operator2 =  self.numberFactory.getNumber(4) 
        self.AddedNumber7_4.result =  self.numberFactory.getNumber(11)

        self.AddedNumber7_5 = self.addObject(AddedNumber()) 
        self.AddedNumber7_5.operator1 =  self.numberFactory.getNumber(7) 
        self.AddedNumber7_5.operator2 =  self.numberFactory.getNumber(5) 
        self.AddedNumber7_5.result =  self.numberFactory.getNumber(12)

        self.AddedNumber7_6 = self.addObject(AddedNumber()) 
        self.AddedNumber7_6.operator1 =  self.numberFactory.getNumber(7) 
        self.AddedNumber7_6.operator2 =  self.numberFactory.getNumber(6) 
        self.AddedNumber7_6.result =  self.numberFactory.getNumber(13)

        self.AddedNumber7_7 = self.addObject(AddedNumber()) 
        self.AddedNumber7_7.operator1 =  self.numberFactory.getNumber(7) 
        self.AddedNumber7_7.operator2 =  self.numberFactory.getNumber(7) 
        self.AddedNumber7_7.result =  self.numberFactory.getNumber(14)

        self.AddedNumber7_8 = self.addObject(AddedNumber()) 
        self.AddedNumber7_8.operator1 =  self.numberFactory.getNumber(7) 
        self.AddedNumber7_8.operator2 =  self.numberFactory.getNumber(8) 
        self.AddedNumber7_8.result =  self.numberFactory.getNumber(15)

        self.AddedNumber7_9 = self.addObject(AddedNumber()) 
        self.AddedNumber7_9.operator1 =  self.numberFactory.getNumber(7) 
        self.AddedNumber7_9.operator2 =  self.numberFactory.getNumber(9) 
        self.AddedNumber7_9.result =  self.numberFactory.getNumber(16)

        self.AddedNumber7_10 = self.addObject(AddedNumber()) 
        self.AddedNumber7_10.operator1 =  self.numberFactory.getNumber(7) 
        self.AddedNumber7_10.operator2 =  self.numberFactory.getNumber(10) 
        self.AddedNumber7_10.result =  self.numberFactory.getNumber(17)

        self.AddedNumber8_0 = self.addObject(AddedNumber()) 
        self.AddedNumber8_0.operator1 =  self.numberFactory.getNumber(8) 
        self.AddedNumber8_0.operator2 =  self.numberFactory.getNumber(0) 
        self.AddedNumber8_0.result =  self.numberFactory.getNumber(8)

        self.AddedNumber8_1 = self.addObject(AddedNumber()) 
        self.AddedNumber8_1.operator1 =  self.numberFactory.getNumber(8) 
        self.AddedNumber8_1.operator2 =  self.numberFactory.getNumber(1) 
        self.AddedNumber8_1.result =  self.numberFactory.getNumber(9)

        self.AddedNumber8_2 = self.addObject(AddedNumber()) 
        self.AddedNumber8_2.operator1 =  self.numberFactory.getNumber(8) 
        self.AddedNumber8_2.operator2 =  self.numberFactory.getNumber(2) 
        self.AddedNumber8_2.result =  self.numberFactory.getNumber(10)

        self.AddedNumber8_3 = self.addObject(AddedNumber()) 
        self.AddedNumber8_3.operator1 =  self.numberFactory.getNumber(8) 
        self.AddedNumber8_3.operator2 =  self.numberFactory.getNumber(3) 
        self.AddedNumber8_3.result =  self.numberFactory.getNumber(11)

        self.AddedNumber8_4 = self.addObject(AddedNumber()) 
        self.AddedNumber8_4.operator1 =  self.numberFactory.getNumber(8) 
        self.AddedNumber8_4.operator2 =  self.numberFactory.getNumber(4) 
        self.AddedNumber8_4.result =  self.numberFactory.getNumber(12)

        self.AddedNumber8_5 = self.addObject(AddedNumber()) 
        self.AddedNumber8_5.operator1 =  self.numberFactory.getNumber(8) 
        self.AddedNumber8_5.operator2 =  self.numberFactory.getNumber(5) 
        self.AddedNumber8_5.result =  self.numberFactory.getNumber(13)

        self.AddedNumber8_6 = self.addObject(AddedNumber()) 
        self.AddedNumber8_6.operator1 =  self.numberFactory.getNumber(8) 
        self.AddedNumber8_6.operator2 =  self.numberFactory.getNumber(6) 
        self.AddedNumber8_6.result =  self.numberFactory.getNumber(14)

        self.AddedNumber8_7 = self.addObject(AddedNumber()) 
        self.AddedNumber8_7.operator1 =  self.numberFactory.getNumber(8) 
        self.AddedNumber8_7.operator2 =  self.numberFactory.getNumber(7) 
        self.AddedNumber8_7.result =  self.numberFactory.getNumber(15)

        self.AddedNumber8_8 = self.addObject(AddedNumber()) 
        self.AddedNumber8_8.operator1 =  self.numberFactory.getNumber(8) 
        self.AddedNumber8_8.operator2 =  self.numberFactory.getNumber(8) 
        self.AddedNumber8_8.result =  self.numberFactory.getNumber(16)

        self.AddedNumber8_9 = self.addObject(AddedNumber()) 
        self.AddedNumber8_9.operator1 =  self.numberFactory.getNumber(8) 
        self.AddedNumber8_9.operator2 =  self.numberFactory.getNumber(9) 
        self.AddedNumber8_9.result =  self.numberFactory.getNumber(17)

        self.AddedNumber8_10 = self.addObject(AddedNumber()) 
        self.AddedNumber8_10.operator1 =  self.numberFactory.getNumber(8) 
        self.AddedNumber8_10.operator2 =  self.numberFactory.getNumber(10) 
        self.AddedNumber8_10.result =  self.numberFactory.getNumber(18)

        self.AddedNumber9_0 = self.addObject(AddedNumber()) 
        self.AddedNumber9_0.operator1 =  self.numberFactory.getNumber(9) 
        self.AddedNumber9_0.operator2 =  self.numberFactory.getNumber(0) 
        self.AddedNumber9_0.result =  self.numberFactory.getNumber(9)

        self.AddedNumber9_1 = self.addObject(AddedNumber()) 
        self.AddedNumber9_1.operator1 =  self.numberFactory.getNumber(9) 
        self.AddedNumber9_1.operator2 =  self.numberFactory.getNumber(1) 
        self.AddedNumber9_1.result =  self.numberFactory.getNumber(10)

        self.AddedNumber9_2 = self.addObject(AddedNumber()) 
        self.AddedNumber9_2.operator1 =  self.numberFactory.getNumber(9) 
        self.AddedNumber9_2.operator2 =  self.numberFactory.getNumber(2) 
        self.AddedNumber9_2.result =  self.numberFactory.getNumber(11)

        self.AddedNumber9_3 = self.addObject(AddedNumber()) 
        self.AddedNumber9_3.operator1 =  self.numberFactory.getNumber(9) 
        self.AddedNumber9_3.operator2 =  self.numberFactory.getNumber(3) 
        self.AddedNumber9_3.result =  self.numberFactory.getNumber(12)

        self.AddedNumber9_4 = self.addObject(AddedNumber()) 
        self.AddedNumber9_4.operator1 =  self.numberFactory.getNumber(9) 
        self.AddedNumber9_4.operator2 =  self.numberFactory.getNumber(4) 
        self.AddedNumber9_4.result =  self.numberFactory.getNumber(13)

        self.AddedNumber9_5 = self.addObject(AddedNumber()) 
        self.AddedNumber9_5.operator1 =  self.numberFactory.getNumber(9) 
        self.AddedNumber9_5.operator2 =  self.numberFactory.getNumber(5) 
        self.AddedNumber9_5.result =  self.numberFactory.getNumber(14)

        self.AddedNumber9_6 = self.addObject(AddedNumber()) 
        self.AddedNumber9_6.operator1 =  self.numberFactory.getNumber(9) 
        self.AddedNumber9_6.operator2 =  self.numberFactory.getNumber(6) 
        self.AddedNumber9_6.result =  self.numberFactory.getNumber(15)

        self.AddedNumber9_7 = self.addObject(AddedNumber()) 
        self.AddedNumber9_7.operator1 =  self.numberFactory.getNumber(9) 
        self.AddedNumber9_7.operator2 =  self.numberFactory.getNumber(7) 
        self.AddedNumber9_7.result =  self.numberFactory.getNumber(16)

        self.AddedNumber9_8 = self.addObject(AddedNumber()) 
        self.AddedNumber9_8.operator1 =  self.numberFactory.getNumber(9) 
        self.AddedNumber9_8.operator2 =  self.numberFactory.getNumber(8) 
        self.AddedNumber9_8.result =  self.numberFactory.getNumber(17)

        self.AddedNumber9_9 = self.addObject(AddedNumber()) 
        self.AddedNumber9_9.operator1 =  self.numberFactory.getNumber(9) 
        self.AddedNumber9_9.operator2 =  self.numberFactory.getNumber(9) 
        self.AddedNumber9_9.result =  self.numberFactory.getNumber(18)

        self.AddedNumber9_10 = self.addObject(AddedNumber()) 
        self.AddedNumber9_10.operator1 =  self.numberFactory.getNumber(9) 
        self.AddedNumber9_10.operator2 =  self.numberFactory.getNumber(10) 
        self.AddedNumber9_10.result =  self.numberFactory.getNumber(19)

        self.AddedNumber10_0 = self.addObject(AddedNumber()) 
        self.AddedNumber10_0.operator1 =  self.numberFactory.getNumber(10) 
        self.AddedNumber10_0.operator2 =  self.numberFactory.getNumber(0) 
        self.AddedNumber10_0.result =  self.numberFactory.getNumber(10)

        self.AddedNumber10_1 = self.addObject(AddedNumber()) 
        self.AddedNumber10_1.operator1 =  self.numberFactory.getNumber(10) 
        self.AddedNumber10_1.operator2 =  self.numberFactory.getNumber(1) 
        self.AddedNumber10_1.result =  self.numberFactory.getNumber(11)

        self.AddedNumber10_2 = self.addObject(AddedNumber()) 
        self.AddedNumber10_2.operator1 =  self.numberFactory.getNumber(10) 
        self.AddedNumber10_2.operator2 =  self.numberFactory.getNumber(2) 
        self.AddedNumber10_2.result =  self.numberFactory.getNumber(12)

        self.AddedNumber10_3 = self.addObject(AddedNumber()) 
        self.AddedNumber10_3.operator1 =  self.numberFactory.getNumber(10) 
        self.AddedNumber10_3.operator2 =  self.numberFactory.getNumber(3) 
        self.AddedNumber10_3.result =  self.numberFactory.getNumber(13)

        self.AddedNumber10_4 = self.addObject(AddedNumber()) 
        self.AddedNumber10_4.operator1 =  self.numberFactory.getNumber(10) 
        self.AddedNumber10_4.operator2 =  self.numberFactory.getNumber(4) 
        self.AddedNumber10_4.result =  self.numberFactory.getNumber(14)

        self.AddedNumber10_5 = self.addObject(AddedNumber()) 
        self.AddedNumber10_5.operator1 =  self.numberFactory.getNumber(10) 
        self.AddedNumber10_5.operator2 =  self.numberFactory.getNumber(5) 
        self.AddedNumber10_5.result =  self.numberFactory.getNumber(15)

        self.AddedNumber10_6 = self.addObject(AddedNumber()) 
        self.AddedNumber10_6.operator1 =  self.numberFactory.getNumber(10) 
        self.AddedNumber10_6.operator2 =  self.numberFactory.getNumber(6) 
        self.AddedNumber10_6.result =  self.numberFactory.getNumber(16)

        self.AddedNumber10_7 = self.addObject(AddedNumber()) 
        self.AddedNumber10_7.operator1 =  self.numberFactory.getNumber(10) 
        self.AddedNumber10_7.operator2 =  self.numberFactory.getNumber(7) 
        self.AddedNumber10_7.result =  self.numberFactory.getNumber(17)

        self.AddedNumber10_8 = self.addObject(AddedNumber()) 
        self.AddedNumber10_8.operator1 =  self.numberFactory.getNumber(10) 
        self.AddedNumber10_8.operator2 =  self.numberFactory.getNumber(8) 
        self.AddedNumber10_8.result =  self.numberFactory.getNumber(18)

        self.AddedNumber10_9 = self.addObject(AddedNumber()) 
        self.AddedNumber10_9.operator1 =  self.numberFactory.getNumber(10) 
        self.AddedNumber10_9.operator2 =  self.numberFactory.getNumber(9) 
        self.AddedNumber10_9.result =  self.numberFactory.getNumber(19)

        self.AddedNumber10_10 = self.addObject(AddedNumber()) 
        self.AddedNumber10_10.operator1 =  self.numberFactory.getNumber(10) 
        self.AddedNumber10_10.operator2 =  self.numberFactory.getNumber(10) 
        self.AddedNumber10_10.result =  self.numberFactory.getNumber(20)
									

        self.greaterThan1_0 = self.addObject(GreaterThan()) 
        self.greaterThan1_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan1_0.higher =  self.numberFactory.getNumber(1)
									

        self.greaterThan2_0 = self.addObject(GreaterThan()) 
        self.greaterThan2_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan2_0.higher =  self.numberFactory.getNumber(2)
	
        self.greaterThan2_1 = self.addObject(GreaterThan()) 
        self.greaterThan2_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan2_1.higher =  self.numberFactory.getNumber(2)
								

        self.greaterThan3_0 = self.addObject(GreaterThan()) 
        self.greaterThan3_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan3_0.higher =  self.numberFactory.getNumber(3)
	
        self.greaterThan3_1 = self.addObject(GreaterThan()) 
        self.greaterThan3_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan3_1.higher =  self.numberFactory.getNumber(3)
	
        self.greaterThan3_2 = self.addObject(GreaterThan()) 
        self.greaterThan3_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan3_2.higher =  self.numberFactory.getNumber(3)
							

        self.greaterThan4_0 = self.addObject(GreaterThan()) 
        self.greaterThan4_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan4_0.higher =  self.numberFactory.getNumber(4)
	
        self.greaterThan4_1 = self.addObject(GreaterThan()) 
        self.greaterThan4_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan4_1.higher =  self.numberFactory.getNumber(4)
	
        self.greaterThan4_2 = self.addObject(GreaterThan()) 
        self.greaterThan4_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan4_2.higher =  self.numberFactory.getNumber(4)
	
        self.greaterThan4_3 = self.addObject(GreaterThan()) 
        self.greaterThan4_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan4_3.higher =  self.numberFactory.getNumber(4)
						

        self.greaterThan5_0 = self.addObject(GreaterThan()) 
        self.greaterThan5_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan5_0.higher =  self.numberFactory.getNumber(5)
	
        self.greaterThan5_1 = self.addObject(GreaterThan()) 
        self.greaterThan5_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan5_1.higher =  self.numberFactory.getNumber(5)
	
        self.greaterThan5_2 = self.addObject(GreaterThan()) 
        self.greaterThan5_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan5_2.higher =  self.numberFactory.getNumber(5)
	
        self.greaterThan5_3 = self.addObject(GreaterThan()) 
        self.greaterThan5_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan5_3.higher =  self.numberFactory.getNumber(5)
	
        self.greaterThan5_4 = self.addObject(GreaterThan()) 
        self.greaterThan5_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan5_4.higher =  self.numberFactory.getNumber(5)
					

        self.greaterThan6_0 = self.addObject(GreaterThan()) 
        self.greaterThan6_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan6_0.higher =  self.numberFactory.getNumber(6)
	
        self.greaterThan6_1 = self.addObject(GreaterThan()) 
        self.greaterThan6_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan6_1.higher =  self.numberFactory.getNumber(6)
	
        self.greaterThan6_2 = self.addObject(GreaterThan()) 
        self.greaterThan6_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan6_2.higher =  self.numberFactory.getNumber(6)
	
        self.greaterThan6_3 = self.addObject(GreaterThan()) 
        self.greaterThan6_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan6_3.higher =  self.numberFactory.getNumber(6)
	
        self.greaterThan6_4 = self.addObject(GreaterThan()) 
        self.greaterThan6_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan6_4.higher =  self.numberFactory.getNumber(6)
	
        self.greaterThan6_5 = self.addObject(GreaterThan()) 
        self.greaterThan6_5.lower =  self.numberFactory.getNumber(5) 
        self.greaterThan6_5.higher =  self.numberFactory.getNumber(6)
				

        self.greaterThan7_0 = self.addObject(GreaterThan()) 
        self.greaterThan7_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan7_0.higher =  self.numberFactory.getNumber(7)
	
        self.greaterThan7_1 = self.addObject(GreaterThan()) 
        self.greaterThan7_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan7_1.higher =  self.numberFactory.getNumber(7)
	
        self.greaterThan7_2 = self.addObject(GreaterThan()) 
        self.greaterThan7_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan7_2.higher =  self.numberFactory.getNumber(7)
	
        self.greaterThan7_3 = self.addObject(GreaterThan()) 
        self.greaterThan7_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan7_3.higher =  self.numberFactory.getNumber(7)
	
        self.greaterThan7_4 = self.addObject(GreaterThan()) 
        self.greaterThan7_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan7_4.higher =  self.numberFactory.getNumber(7)
	
        self.greaterThan7_5 = self.addObject(GreaterThan()) 
        self.greaterThan7_5.lower =  self.numberFactory.getNumber(5) 
        self.greaterThan7_5.higher =  self.numberFactory.getNumber(7)
	
        self.greaterThan7_6 = self.addObject(GreaterThan()) 
        self.greaterThan7_6.lower =  self.numberFactory.getNumber(6) 
        self.greaterThan7_6.higher =  self.numberFactory.getNumber(7)
			

        self.greaterThan8_0 = self.addObject(GreaterThan()) 
        self.greaterThan8_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan8_0.higher =  self.numberFactory.getNumber(8)
	
        self.greaterThan8_1 = self.addObject(GreaterThan()) 
        self.greaterThan8_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan8_1.higher =  self.numberFactory.getNumber(8)
	
        self.greaterThan8_2 = self.addObject(GreaterThan()) 
        self.greaterThan8_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan8_2.higher =  self.numberFactory.getNumber(8)
	
        self.greaterThan8_3 = self.addObject(GreaterThan()) 
        self.greaterThan8_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan8_3.higher =  self.numberFactory.getNumber(8)
	
        self.greaterThan8_4 = self.addObject(GreaterThan()) 
        self.greaterThan8_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan8_4.higher =  self.numberFactory.getNumber(8)
	
        self.greaterThan8_5 = self.addObject(GreaterThan()) 
        self.greaterThan8_5.lower =  self.numberFactory.getNumber(5) 
        self.greaterThan8_5.higher =  self.numberFactory.getNumber(8)
	
        self.greaterThan8_6 = self.addObject(GreaterThan()) 
        self.greaterThan8_6.lower =  self.numberFactory.getNumber(6) 
        self.greaterThan8_6.higher =  self.numberFactory.getNumber(8)
	
        self.greaterThan8_7 = self.addObject(GreaterThan()) 
        self.greaterThan8_7.lower =  self.numberFactory.getNumber(7) 
        self.greaterThan8_7.higher =  self.numberFactory.getNumber(8)
		

        self.greaterThan9_0 = self.addObject(GreaterThan()) 
        self.greaterThan9_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan9_0.higher =  self.numberFactory.getNumber(9)
	
        self.greaterThan9_1 = self.addObject(GreaterThan()) 
        self.greaterThan9_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan9_1.higher =  self.numberFactory.getNumber(9)
	
        self.greaterThan9_2 = self.addObject(GreaterThan()) 
        self.greaterThan9_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan9_2.higher =  self.numberFactory.getNumber(9)
	
        self.greaterThan9_3 = self.addObject(GreaterThan()) 
        self.greaterThan9_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan9_3.higher =  self.numberFactory.getNumber(9)
	
        self.greaterThan9_4 = self.addObject(GreaterThan()) 
        self.greaterThan9_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan9_4.higher =  self.numberFactory.getNumber(9)
	
        self.greaterThan9_5 = self.addObject(GreaterThan()) 
        self.greaterThan9_5.lower =  self.numberFactory.getNumber(5) 
        self.greaterThan9_5.higher =  self.numberFactory.getNumber(9)
	
        self.greaterThan9_6 = self.addObject(GreaterThan()) 
        self.greaterThan9_6.lower =  self.numberFactory.getNumber(6) 
        self.greaterThan9_6.higher =  self.numberFactory.getNumber(9)
	
        self.greaterThan9_7 = self.addObject(GreaterThan()) 
        self.greaterThan9_7.lower =  self.numberFactory.getNumber(7) 
        self.greaterThan9_7.higher =  self.numberFactory.getNumber(9)
	
        self.greaterThan9_8 = self.addObject(GreaterThan()) 
        self.greaterThan9_8.lower =  self.numberFactory.getNumber(8) 
        self.greaterThan9_8.higher =  self.numberFactory.getNumber(9)
	

        self.greaterThan10_0 = self.addObject(GreaterThan()) 
        self.greaterThan10_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan10_0.higher =  self.numberFactory.getNumber(10)
	
        self.greaterThan10_1 = self.addObject(GreaterThan()) 
        self.greaterThan10_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan10_1.higher =  self.numberFactory.getNumber(10)
	
        self.greaterThan10_2 = self.addObject(GreaterThan()) 
        self.greaterThan10_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan10_2.higher =  self.numberFactory.getNumber(10)
	
        self.greaterThan10_3 = self.addObject(GreaterThan()) 
        self.greaterThan10_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan10_3.higher =  self.numberFactory.getNumber(10)
	
        self.greaterThan10_4 = self.addObject(GreaterThan()) 
        self.greaterThan10_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan10_4.higher =  self.numberFactory.getNumber(10)
	
        self.greaterThan10_5 = self.addObject(GreaterThan()) 
        self.greaterThan10_5.lower =  self.numberFactory.getNumber(5) 
        self.greaterThan10_5.higher =  self.numberFactory.getNumber(10)
	
        self.greaterThan10_6 = self.addObject(GreaterThan()) 
        self.greaterThan10_6.lower =  self.numberFactory.getNumber(6) 
        self.greaterThan10_6.higher =  self.numberFactory.getNumber(10)
	
        self.greaterThan10_7 = self.addObject(GreaterThan()) 
        self.greaterThan10_7.lower =  self.numberFactory.getNumber(7) 
        self.greaterThan10_7.higher =  self.numberFactory.getNumber(10)
	
        self.greaterThan10_8 = self.addObject(GreaterThan()) 
        self.greaterThan10_8.lower =  self.numberFactory.getNumber(8) 
        self.greaterThan10_8.higher =  self.numberFactory.getNumber(10)
	
        self.greaterThan10_9 = self.addObject(GreaterThan()) 
        self.greaterThan10_9.lower =  self.numberFactory.getNumber(9) 
        self.greaterThan10_9.higher =  self.numberFactory.getNumber(10)


        
    def goal(self):
        return self.request1.status == self.statusReqRequestFinished and \
        self.request2.status == self.statusReqRequestFinished and \
        self.request3.status == self.statusReqRequestFinished and \
        self.request4.status == self.statusReqRequestFinished and \
        self.pod1.status == self.statusPodPending

p = Problem1()
retCode = p.run()