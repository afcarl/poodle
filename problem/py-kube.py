from poodle.poodle import * 
from action.pydlNetAction import *
from object.networkObject import *

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
    pass
    # Identity
    # Properties 
    # Relations 

class ContainerConfig(Object):
        #Identity
    identified_by = ["containerconfigId"]
    identified_by = Property(containerConfigId=Number)
         # Properties

class Node(Object):
    # Identity
    identified_by = ["nodeId"]
    identified_by = Property(nodeId=Number)
    # Properties 
    cpuCapacity = Property(Number)
    memCapacity = Property(Number)
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
    node = Property(Node)
    currentRealCpuConsumption = Property( Number)
    currentRealMemConsumption = Property( Number)
    atNode = Property(Node)
    toNode = Property(Node)
    status = Property(Status)
    bindedToNode = Property(Node)
    requestedMem = Property(Number)
    requestedCpu = Property(Number)
    podOverwhelmingLimits = StateFact()
    podNotOverwhelmingLimits = StateFact()
    podIsOnetime = StateFact()


Pod.prevPod = Property(Pod)    
    
# class Event(PlannedAction):
#     #Identity
#     identified_by = ["eventId"]
#     identified_by = Property( eventId = Number)
#     # Property
#     node = Property(Node)
#     extraValue = Property(Number)
#     eventType = Property(EventType)

# class EventType(Object):
#     #Identity
    
class Service(Object):
        # Identity
    identified_by = ["serviceId"]
    identified_by = Property(serviceId=Number)
         # Properties 
    lastPod = Property(Pod)
    atNode = Property(Node)

         # Relations
Service.selectionedPod = Relation(Pod)

class Period(Object):
        # Identity
    identified_by = ["periodId"]
    identified_by = Property(periodId=Number)

         # Relations
Period.prevPeriod = Property(Period)         


class Container(Object):
        #Identity
    identified_by = ["containerId"]
    identified_by = Property(containerId=Number)
        # Properties
    hasPod = Property(Pod)
    cpuRequest = Property(Number)
    memRequest = Property(Number)
    cpuLimit = Property(Number)
    memLimit = Property(Number)
    config = Property(ContainerConfig)

     

class Request(Object):
        # Identity
    identified_by = ["requestId"]
    identified_by = Property(requestId=Number)
         # Properties 
    
    launchPeriod = Property(Period)
    status = Property(Status)
    atPod = Property(Pod)
    atNode = Property(Node)
    toPod = Property(Pod)
    toNode = Property(Node)    
    targetService = Property(Service)
         # Relations


         

class Loadbalancer(Object):
        # Identity
    identified_by = ["lbId"]
    identified_by = Property(lbId=Number)
    lastNode = Property(Node)
    atNode = Property(Node)
         # Relations
Loadbalancer.selectionedService = Relation(Service)
        
class Kubeproxy(Object):
    # Identity
    identified_by = ["kpId"]
    identified_by = Property(kpId=Number)
        

    # Properties 
    mode = Property(Mode)
    lastPod = Property(Pod)
    atNode = Property(Node)
    # Relations
Kubeproxy.selectionedPod = Relation(Pod)
Kubeproxy.selectionedService = Relation(Service)

         # Relations
         
class AddedNumber(Object):
    cost = 1
    identified_by = ["operator1,operator2"]
    identified_by = Property(operator1=Number,operator2=Number)
    
    operator1 = Property(Number)
    operator2 = Property(Number)
    result = Property(Number)
     
     
class ToLoadbalancer(PlannedAction):
    cost = 1
    request1 = Request()
    serviceTarget = Select(request1.targetService ==  Service)
    lb = Loadbalancer()
    lbServedServices = Select( Service in lb.selectionedService)

    def selector(self):
        return Select( self.serviceTarget == self.lbServedService and request1.status == self.problem.statusReqAtStart)
    
    def effect(self):
        self.request1.status = self.problem.statusReqAtLoadbalanser
        self.request1.atNode = self.lb.atNode

class DirectToNode(PlannedAction):
    cost = 1
    request1 = Request()
    targetService = Select( Service == request1.targetService)
    podWithTargetService = Select( Pod == targetService.selectionedPod)
    nodeWithTargetService = Node()
    
    

#(pod ?number)

# (Object ?entitytype - entitytypes ?obj-id - Number)
# (pod-memRequest ?podId1 - Number ?podId2 - Number ?memRequest - Number)

# (pod-memRequest ?pod - Pod ?memRequest - Number)

#    podtemplate =  ...
#    maxNumberofPod = ....
#    nextNumberofPod = ... 
    # newPod = Pod.pod_id == nextNumberofPod
     
    def selector(self):
        return Select( self.nodeWithTargetService == self.podWithTargetService.node and request1.status == self.problem.statusReqAtLoadbalanser)

    def effect(self):
        self.request1.status = self.problem.statusPodDirectedToNode
        self.request1.toNode = nodeWithTargetService
        
        # newPod = self.problem.addObject(Pod())
        # newPod.memRequest = self.template1.memRequest

        # self.node.pod.add(self.problem.pod1)
        
        # self.newPod.set()
        # newPod.podConfig = ...
        
#        self.newPod.status = "pending"
#        self.newPod.memRequest = ...


    
class ToNode(PlannedAction):
    cost = 1 
    request1 = Request()
    node1 = Select( Node == request1.toNode)
    

    def selector(self):
        return Select( self.node1.status == self.problem.statusNodeActive and request1.status == self.problem.statusPodDirectedToNode)

    def effect(self):
        self.request1.status = self.problem.statusReqAtKubeproxy
        self.request1.toNode = None 
        self.request1.atNode = request1.toNode


class SwitchToNextNode(PlannedAction):
    cost = 1
    request1 = Request()
    node1 = Select( Node == request1.toNode)
    nextNode1 = Select( Node.prevNode == node1)
    def selector(self):
        return Select( self.node1.status == self.problem.statusNodeInactive and request1.status == self.problem.statusPodDirectedToNode)

    def effect(self):
        self.request1.toNode = self.nextNode1


class DirectToPod(PlannedAction):
    cost = 1
    request1 = Request()
    targetService = Select( Service == request1.targetService)
    podWithTargetService = Select( Pod == targetService.selectionedPod)
    currectNode = Select( Node == request1.atNode)


    def selector(self):
        return Select( self.podWithTargetService == self.request1.atNode and request1.status == self.problem.statusReqAtKubeproxy)

    def effect(self):
        self.request1.status = self.problem.statusPodDirectedToNode
        self.request1.toPod = podWithTargetService


class ToPod(PlannedAction):
    cost = 1 
    request1 = Request()
    pod1 = Select( Pod == request1.toPod)

    def selector(self):
        return Select( self.pod1.status == self.problem.statusPodActive and \
        request1.status == self.problem.statusPodDirectedToNode) 

    def effect(self):
        self.request1.status = self.problem.statusReqAtPodInput
        self.request1.toPod = None 
        self.request1.atPod = pod1



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
    addedMemConsumptionAtCurrentPod1 = Select( AddedNumber.operator1 == currentPod.currentRealMemConsumption) 
    addedCpuConsumptionAtCurrentNode1 = Select( AddedNumber.operator1 == currentNode.currentRealCpuConsumption) 
    addedMemConsumptionAtCurrentNode1 = Select( AddedNumber.operator1 == currentNode.currentRealMemConsumption)
    
    #KB: RealCPUConsumption - is consumption calculated per active requests ( each request adds some level of consumption, realy on the CPU/Mem
    #KB: RealCPUConsumption - it is tracked for pod and node . Both. this is used by autoscale and scheduller and kubectl  while starting pods on node
    #KB: FormalCPUConcumption - it is consumption calculated for nodes only. Pods when try to start shoul check limits by this value.  
    
    def selector(self):
        return Select( request1.status == self.problem.statusReqAtPodInput and \
        addedCpuConsumptionAtCurrentPod1.operator2 == request1.cpuRequest and \
        addedMemConsumptionAtCurrentPod1.operator2 == request1.memRequest and \
        addedCpuConsumptionAtCurrentNode1.operator2 == request1.cpuRequest and \
        addedMemConsumptionAtCurrentNode1.operator2 == request1.memRequest )        


    def effect(self):
        self.request1.status.set(self.problem.statusReqResourcesConsumed)
        self.currentPod.currentRealCpuConsumption.set(addedCpuConsumptionAtCurrentPod1.result)
        self.currentPod.currentRealMemConsumption.set(addedMemConsumptionAtCurrentPod1.result)
        self.currentNode.currentRealCpuConsumption.set(addedCpuConsumptionAtCurrentNode1.result)
        self.currentNode.currentRealMemConsumption.set(addedMemConsumptionAtCurrentNode1.result)
 

class ProcessTempRequest(PlannedAction):
    cost = 1
    request1 = Request()
    
    def selector(self):
        return Select( self.request1.type == self.problem.typeTemporary and request1.status == self.problem.statusReqResourcesConsumed)
    
    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestPIDToBeEnded)
        
class ProcessPersistentRequest(PlannedAction):
    cost = 1
    request1 = Request()
    
    def selector(self):
        return Select( request1.status == self.problem.statusReqResourcesConsumed and \
        self.request1.type != self.problem.typeTemporary)

    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)


class ReleaseResource(PlannedAction):
    cost = 1
    request1 = Request() 
    currentPod = Select( Pod == request1.atPod)
    currentNode = Select( Node == request1.atNode)

    reducedCpuConsumptionAtCurrentPod1 = Select( AddedNumber.result == currentPod.currentRealCpuConsumption) 
    reducedMemConsumptionAtCurrentPod1 = Select( AddedNumber.result == currentPod.currentRealMemConsumption) 
    reducedCpuConsumptionAtCurrentNode1 = Select( AddedNumber.result == currentNode.currentRealCpuConsumption) 
    reducedMemConsumptionAtCurrentNode1 = Select( AddedNumber.result == currentNode.currentRealMemConsumption)
    
    def selector(self):
        return Select( request1.status == self.problem.statusReqRequestPIDToBeEnded and \
        reducedCpuConsumptionAtCurrentPod1.operator2 == request1.cpuRequest and \
        reducedMemConsumptionAtCurrentPod1.operator2 == request1.memRequest and \
        reducedCpuConsumptionAtCurrentNode1.operator2 == request1.cpuRequest and \
        reducedMemConsumptionAtCurrentNode1.operator2 == request1.memRequest)


    def effect(self):
        self.request1.status.set(self.problem.statusReqResourcesReleased)
        self.currentPod.currentRealCpuConsumption.set(addedCpuConsumptionAtCurrentPod1.operator1)
        self.currentPod.currentRealMemConsumption.set(addedMemConsumptionAtCurrentPod1.operator1)
        self.currentNode.currentRealCpuConsumption.set(addedCpuConsumptionAtCurrentNode1.operator1)
        self.currentNode.currentRealMemConsumption.set(addedMemConsumptionAtCurrentNode1.operator1) 

class FinishRequest(PlannedAction):
    cost = 1
    request1 = Request()
    pod1 = Select(Pod == request1.atPod)
    
    
    def selector(self):
        return Select( request1.status == self.problem.statusReqResourcesReleased and \
         pod1.podIsOnetime != True)
    
    def effect(self):
        self.request1.status.set( self.problem.statusReqRequestFinished)
        self.request1.atPod.unset()
        self.request1.atNode.unset()

class TerminatePodAfterFinish(PlannedAction):
    cost = 1
    request1 = Request()
    pod1 = Select(Pod == request1.atPod)

    def selector(self):
        return Select( request1.status == self.problem.statusReqResourcesReleased and \
        pod1.podIsOnetime == True)
        
    def effect(self):
        self.request1.status.set(self.problem.statusReqRequestFinished)
        self.request1.atPod.unset()
        self.request1.atNode.unset()
        self.pod1.status.set(self.problem.statusReqRequestTerminated)

class TerminatePod(PlannedAction):
    cost = 1
    pod1 = Pod()
    currentNode = Select( Node == pod1.atNode)
    reducedCpuConsumptionAtCurrentNode1 = Select( AddedNumber.result == currentNode.currentFormalCpuConsumption)
    reducedMemConsumptionAtCurrentNode1 = Select( AddedNumber.result == currentNode.currentFormalMemConsumption)
  
    def selector(self):
        return Select( request1.status == self.problem.statusReqRequestPIDToBeEnded and
        reducedCpuConsumptionAtCurrentNode1.operator2 == pod1.currentFormalCpuConsumption and
        reducedMemConsumptionAtCurrentNode1.operator2 == pod1.currentFormalMemConsumption)

    def effect(self):
        self.pod1.set(self.problem.statusPodInactive) #TODO: divide status and state  for POds. state is to be active and nonactive. and status  would also include intermediate substates        
        self.currentNode.currentFormalCpuConsumption = reducedCpuConsumptionAtCurrentNode1.operator1
        self.currentNode.currentFormalMemConsumption = reducedMemConsumptionAtCurrentNode1.operator1


############
# Scaling
### Replicas

class ReadDeploymentConfig(PlannedAction):
    pod1 = Pod()
    def selector(self):
        Select(self.pod1.status == self.problem.statusPodAtConfig)
    
    def effect(self):
        self.pod1.set(self.problem.statusPodPending) 

class CreatePodManually(PlannedAction):
    pod1 = Pod()
    def selector(self):
        return Select(request1.status == self.problem.statusPodAtManualCreation)

    def effect(self):
        self.pod1.set(self.problem.statusPodPending)

class SchedulerNofityUnboundedPod(PlannedAction):
    pod1 = Pod()
    node1 = Node()
    freeMem_op1 = AddedNumber()
    freeMem_op2 = AddedNumber()
    
    freeMem_op1 = Select( AddedNumber.operator2 == node1.currentFormalMemConsumption)
    #ffffreeMem_op1 = AddedNumber.Select(operator2 = node1.currentMemConsumption, result = node1.memCapacity)

    freeCpu_op1 = Select( AddedNumber.operator2 == node1.currentFormalCpuConsumption)
    leftMem_op1 = Select( AddedNumber.operator2 == pod1.requestedMem) 
    leftCpu_op1 = Select( AddedNumber.operator2 == pod1.requestedCpu) 
    newMemConsumptionAtNode_res = Select( AddedNumber.operator1 == node1.currentFormalMemConsumption)
    newCpuConsumptionAtNode_res = Select( AddedNumber.operator1 == node1.currentFormalCpuConsumption)
    
    #to-do: Soft conditions are not supported yet ( prioritization of nodes :  for example healthy  nodes are selected  rather then non healthy if pod  requests such behavior 
    def selector(self):
        return Select( pod1.status == self.problem.statusPodPending and \
            freeMem_op1.result == node1.memCapacity and \
            freeCpu_op1.result == node1.cpuCapacity and \
            leftMem_op1.result == freeMem_op1.operator1 and \
            leftCpu_op1.result == freeCpu_op1.operator1 and \
            newFormalMemConsumptionAtNode_res.operator2 == pod1.requestedMem and \
            newFormalCpuConsumptionAtNode_res.operator2 == pod1.requestedCpu
            )
    
    def effect(self):
        self.pod1.status.set(self.problem.statusPodBindedToNode)
        self.pod1.bindedToNode.set(node1)
        self.node1.currentFormalMemConsumption.set(newFormalMemConsumptionAtNode_res.result)
        self.node1.currentFormalCpuConsumption.set(newFormalCpuConsumptionAtNode_res.result)

class KubectlStartsNode(PlannedAction):
    pod1 = Pod()
    
    # consume real resources from node
    node1 = Select( Node == pod1.bindedToNode)
    newMemRealConsumptionAtNode_res = Select(AddedNumber.operator1 == node1.currentRealMemConsumption)
    newCpuRealConsumptionAtNode_res = Select(AddedNumber.operator1 == node1.currentRealCpuConsumption)
    def selector(self):
        return Select(pod1.status == self.problem.statusPodBindedToNode and \
        newMemRealConsumptionAtNode_res.operator2 == pod1.realInitialMemConsumption and \
        newCpuRealConsumptionAtNode_res.operator2 == pod1.realInitialCpuConsumption)
    
    def effect(self):
        self.pod1.status.set(self.problem.statusPodRunning)
        self.pod1.atNode.set(node1)
        self.pod1.bindedToNode.unset(node1)
        self.node1.currentRealMemConsumption.set(newMemConsumptionAtNode_res.result)
        self.node1.currentRealCpuConsumption.set(newCpuConsumptionAtNode_res.result)

class MarkPodAsOverwhelmingMemLimits(PlannedAction):
    pod1 = Pod()
    node1 = Select( Node == pod1.atNode)
    nextAmountOfoverwhelming  = AddedNumber.operator1 == node1.AmountOfPodsOverwhelmingMemLimits

    def selector(self):
        return Select( 
            self.pod1.podNotOverwhelmingLimits == True and \
            self.Greaterthan.lower == pod1.memLimit and \
        Greaterthan.higher == pod1.currentMemConsumption and \
        self.nextAmountOfoverwhelming.operator2 == self.problem.numberFactory.getNumber(1))

    def effect(self):
        self.pod1.podOverwhelmingLimits = True
        self.pod1.podNotOverwhelmingLimits = False
        self.node1.AmountOfPodsOverwhelmingMemLimits = nextAmountOfoverwhelming.result

class MarkPodAsNonoverwhelmingMemLimits(PlannedAction):
    pod1 = Pod()
    node1 = Select(Node == pod1.atNode)
    prevAmountOfoverwhelming  = AddedNumber.result == node1.AmountOfPodsOverwhelmingMemLimits

    def selector(self):
        return Select(pod1.podOverwhelmingLimits == True and \
        self.Greaterthan.lower == pod1.memLimit and \
        Greaterthan.higher == pod1.currentMemConsumption and \
        self.prevAmountOfoverwhelming.operator2 == self.problem.numberFactory.getNumber(1))

    def effect(self):
        self.pod1.podOverwhelmingLimits = True
        self.pod1.podNotOverwhelmingLimits = False
        self.node1.AmountOfPodsOverwhelmingMemLimits = prevAmountOfoverwhelming.operator1


class MemoryErrorKillPodOverwhelmingLimits(PlannedAction):
    node1 = Node()
    pod1 = Select( Pod.atNode == node1)
    def selector(self):
        return Select(self.Greaterthan.lower == node1.memCapacity and Greaterthan.higher == node1.currentRealMemConsumption and \
                node1.status == self.problem.statusNodeActive and \
                pod1.podOverwhelmingLimits == True)

    def effect(self):
        self.pod1.substatus.set(self.problem.statusNodeOomKilling)

class MemoryErrorKillPodNotOverwhelmingLimits(PlannedAction):
    node1 = Node()
    pod1 = Select( Pod.atNode == node1)
    def selector(self):
        return Select(self.Greaterthan.lower == node1.memCapacity and Greaterthan.higher == node1.currentRealMemConsumption and \
        node1.AmountOfPodsOverwhelmingMemLimits == self.problem.numberFactory.getNumber(0))

    def effect(self):
        self.pod1.substatus.set(self.problem.statusNodeOomKilling)
        

class PodFailsBecauseOfKilling(PlannedAction):
    pod1 = Pod()
    # release initial pod resources from node  
    node1 = Select( Node == pod1.atNode)
    newMemRealConsumptionAtNode_op1 = Select( AddedNumber.result == node1.currentRealMemConsumption)
    newCpuRealConsumptionAtNode_op1 = Select( AddedNumber.result == node1.currentRealCpuConsumption)
    def selector(self):
        return Select( node1.status == self.problem.statusNodeOomKilling and \
        newMemRealConsumptionAtNode_op1.operator2 == pod1.realInitialMemConsumption and \
        newCpuRealConsumptionAtNode_op1.operator2 == pod1.realInitialCpuConsumption)

    def effect(self):
        self.pod1.status.set(self.problem.statusNodeFailed)
        self.node1.currentRealMemConsumption.set(newMemConsumptionAtNode_op1.result)
        self.node1.currentRealCpuConsumption.set(newCpuConsumptionAtNode_op1.result)

        

class PodSucceds(PlannedAction):
    pod1 = Pod()
    # release initial pod resources from node  
    node1 = Select( Node == pod1.atNode)
    newMemRealConsumptionAtNode_op1 = Select(AddedNumber.result == node1.currentRealMemConsumption)
    newCpuRealConsumptionAtNode_op1 = Select(AddedNumber.result == node1.currentRealCpuConsumption)
    
    def selector(self):
        return Select ( node1.status == self.problem.statusNodeRunning and \
        newMemRealConsumptionAtNode_op1.operator2 == pod1.realInitialMemConsumption and \
        newCpuRealConsumptionAtNode_op1.operator2 == pod1.realInitialCpuConsumption)
    
    def effect(self):
        self.pod1.status.set(self.problem.statusNodeSucceded)
        self.node1.currentRealMemConsumption.set(newMemConsumptionAtNode_op1.result)
        self.node1.currentRealCpuConsumption.set(newCpuConsumptionAtNode_op1.result)


class KubectlRecoverPod(PlannedAction):
    pod1 = Pod()
    
    def selector(self):
        return Select( pod1.status == self.problem.statusNodeFailed)
    def effect(self):
        self.pod1.status.set(self.problem.statusNodePending)

class PodGarbageCollectedFailedPod(PlannedAction):
    pod1 = Pod()
    def selector(self):
        return Select( pod1.status == self.problem.statusNodeFailed)
    def effect(self):
        self.pod1.status.set(self.problem.statusNodeDeleted)

class PodGarbageCollectedSuccededPod(PlannedAction):
    pod1 = Pod()
    def selector(self):
        return Select( pod1.status == self.problem.statusNodeSucceded) 

    def effect(self):
        self.pod1.status.set(self.problem.statusNodeDeleted)

# class updatePodMetricsReleaseStarted(PlannedAction):
#     cost = 1
#     request1    = Select( Request.status == "resourcesReleased")
#     podCurrent  = Select( Pod == request1.atPod)
#     nodeCurrent = Select( Node == podCurrent.atNode)
    
    
#     def effect(self):
#         self.request1.status.set("requestReleasedLimitsUpdateStarted")
#         self.request1.atPod.unset()
#         self.request1.atNode.unset()

# class IncreasePodConsumtionStart(PlannedAction):
#     cost = 1
#     request1 = Request.status == "atPodInput"
    
#     def selector(self):
#         return self.request1.status == "atPodInputStartCalc"

#     def effect(self):
#         self.request1.cpuCalculation = self.request1.cpuRequest
#             request1 = request1.cpuCalculation == request1.
            
class Problem1(Problem):
    def actions(self):
        return [globals()[x] for x in globals() if isinstance(globals()[x], PlannedAction)]

    def problem(self):
        self.numberFactory = NumberFactory()
        
        self.statusReqAtStart = self.addObject(Status())
        self.statusReqAtLoadbalanser = self.addObject(Status())
        self.statusReqAtKubeproxy = self.addObject(Status())
        self.statusReqAtPodInput = self.addObject(Status())
        self.statusReqResourcesConsumed = self.addObject(Status())
        self.statusReqDirectedToPod = self.addObject(Status())
        self.statusReqRequestPIDToBeEnded = self.addObject(Status())
        self.statusReqRequestFinished = self.addObject(Status())
        self.statusReqResourcesReleased = self.addObject(Status())
        self.statusReqRequestFinished = self.addObject(Status())

        self.statusPodAtConfig = self.addObject(Status())
        self.statusPodActive = self.addObject(Status())
        self.statusPodPending = self.addObject(Status())
        self.statusPodAtManualCreation = self.addObject(Status())
        self.statusPodBindedToNode = self.addObject(Status())
        self.statusPodRunning = self.addObject(Status())
        self.statusNodeOomKilling = self.addObject(Status())
        self.statusNodeFailed = self.addObject(Status())
        self.statusNodeRunning = self.addObject(Status())
        self.statusNodeSucceded = self.addObject(Status())
        self.statusNodePending = self.addObject(Status())
        self.statusNodeDeleted = self.addObject(Status())
        
        self.statusNodeActive = self.addObject(Status())
        self.statusNodeInactive = self.addObject(Status())
        
        self.typeTemporary = self.addObject(Type())
        

        self.period1 = self.addObject(Period()) 
        
        self.сontainerConfig1 = self.addObject(ContainerConfig())
        self.сontainerConfig2 = self.addObject(ContainerConfig())
        self.сontainerConfig3 = self.addObject(ContainerConfig())
        
        self.node1 = self.addObject(Node())
        self.node1.cpuCapacity = self.numberFactory.getNumber(500)
        self.node1.memCapacity = self.numberFactory.getNumber(100)
        self.node1.currentFormalCpuConsumption = self.numberFactory.getNumber(0)
        self.node1.currentFormalMemConsumption = self.numberFactory.getNumber(0)
        self.node1.currentRealMemConsumption = self.numberFactory.getNumber(0)
        self.node1.currentRealCpuConsumption = self.numberFactory.getNumber(0)
        self.node1.AmountOfPodsOverwhelmingMemLimits = self.numberFactory.getNumber(0)

        self.node2 = self.addObject(Node())
        self.node2.cpuCapacity = self.numberFactory.getNumber(0)
        self.node2.memCapacity = self.numberFactory.getNumber(0)
        self.node2.currentFormalCpuConsumption = self.numberFactory.getNumber(0)
        self.node2.currentFormalMemConsumption = self.numberFactory.getNumber(0)
        self.node2.currentRealMemConsumption = self.numberFactory.getNumber(0)
        self.node2.currentRealCpuConsumption = self.numberFactory.getNumber(0)
        self.node2.AmountOfPodsOverwhelmingMemLimits = self.numberFactory.getNumber(0)
        
        self.node3 = self.addObject(Node())
        self.node3.cpuCapacity = self.numberFactory.getNumber(0)
        self.node3.memCapacity = self.numberFactory.getNumber(0)
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
        self.pod1.requestedMem = self.numberFactory.getNumber(10)
        self.pod1.requestedCpu = self.numberFactory.getNumber(50)
        self.pod1.podNotOverwhelmingLimits = True
        
        self.pod2 = self.addObject(Pod())
        self.pod2.podConfig = self.сontainerConfig2
        self.pod2.currentRealCpuConsumption = self.numberFactory.getNumber(0)
        self.pod2.currentRealMemConsumption = self.numberFactory.getNumber(0)
        self.pod2.status = self.statusPodAtConfig
        self.pod2.requestedMem = self.numberFactory.getNumber(10)
        self.pod2.requestedCpu = self.numberFactory.getNumber(50)
        self.pod2.podNotOverwhelmingLimits = True
         
        ## to-do:  for relations  it should give helpful error message when = instead of add.
        
        self.pod3 = self.addObject(Pod())
        self.pod3.podConfig = self.сontainerConfig3
        self.pod3.currentRealCpuConsumption = self.numberFactory.getNumber(0)
        self.pod3.currentRealMemConsumption = self.numberFactory.getNumber(0)
        self.pod3.status = self.statusPodAtConfig
        self.pod3.requestedMem = self.numberFactory.getNumber(10)
        self.pod3.requestedCpu = self.numberFactory.getNumber(50)
        self.pod3.podNotOverwhelmingLimits = True
        
        self.service1 = self.addObject(Service())
        self.service2 = self.addObject(Service())
        self.service3 = self.addObject(Service())
        
        self.request1 = self.addObject(Request())
        self.request1.launchPeriod = self.period1
        self.request1.status = self.statusReqAtStart
        self.request1.targetService = self.service1

        self.request2 = self.addObject(Request())
        self.request2.launchPeriod = self.period1
        self.request2.status = self.statusReqAtStart
        self.request2.targetService = self.service1

        self.request3 = self.addObject(Request())
        self.request3.launchPeriod = self.period1
        self.request3.status = self.statusReqAtStart
        self.request3.targetService = self.service2

        self.request4 = self.addObject(Request())
        self.request4.launchPeriod = self.period1
        self.request4.status = self.statusReqAtStart
        self.request4.targetService = self.service2
        
        self.lb1 = self.addObject(Loadbalancer())
        self.lb1.atNode = self.node1
        
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
        return self.request1 == self.statusReqRequestFinished and \
        self.request2 == self.statusReqRequestFinished and \
        self.request3 == self.statusReqRequestFinished and \
        self.request4 == self.statusReqRequestFinished

p = Problem1()
retCode = p.run()