from pypl import * 


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

class ContainerConfig(Imaginary):
        #Identity
    identified_by = ["containerconfigId"]
    identified_by = Property(containerConfigId=Number)
         # Properties

class Node(Imaginary):
    # Identity
    identified_by = ["nodeId"]
    identified_by = Property(nodeId=Number)
    # Properties 
    cpuCapacity = Property(Number)
    memCapacity = Property(Number)
    currentCpuConsumption = Property(Number)
    memCurrentConsumption = Property(Number)
Node.prevNode = Property(Node)

         
class Pod(Imaginary):
    #Identity
    identified_by = ["podId"]
    identified_by = Property( podId = Number)
    # Property
    podConfig = Property(ContainerConfig)
    node = Property(Node)
    currentCpuConsumption = Property( Number)
    currentMemConsumption = Property( Number)
    toNode = Property(Node)
    status = Property(Status)
Pod.prevPod = Property(Pod)    
    
class Service(Imaginary):
        # Identity
    identified_by = ["serviceId"]
    identified_by = Property(serviceId=Number)
         # Properties 
    lastPod = Property(Pod)
    kind = Property(Kind)
    atNode = Property(Node)

         # Relations
Service.selectionedPod = Relation(Pod)

class Period(Imaginary):
        # Identity
    identified_by = ["periodId"]
    identified_by = Property(periodId=Number)

         # Relations
Period.prevPeriod = Property(Period)         


class Container(Imaginary):
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

     

class Request(Imaginary):
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


         

class Loadbalancer(Imaginary):
        # Identity
    identified_by = ["lbId"]
    identified_by = Property(lbId=Number)
    lastNode = Property(Node)
    atNode = Property(Node)
         # Relations
Loadbalancer.selectionedService = Relation(Service)
        
class Kubeproxy(Imaginary):
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
         
class AddedNumber(Imaginary):
    cost = 1
    identified_by = ["operator1,operator2"]
    identified_by = Property(operator1=Number,operator2=Number)
    result = Property(Number)
     
     
class ToLoadbalancer(PlannedAction):
    cost = 1
    request1 = Request()
    serviceTarget = Select( request1.status == "atStart" and request1.targetService in Service.targetService)
    lb = Loadbalancer()
    lbServedServices = Select( Service in lb.selectionedService)

    def selector(self):
        return Select( self.serviceTarget == self.lbServedService)
    
    def effect(self):
        self.request1.status = "atLoadbalancer"
        self.request1.atNode = self.lb.atNode

class DirectToNode(PlannedAction):
    cost = 1
    request1 = Request()
    targetService = Select( request1.status == "atLoadbalancer" and Service == request1.targetService)
    podWithTargetService = Select( Pod == targetService.selectionedPod)
    nodeWithTargetService = Node()
    

    def selector(self):
        return Select( self.nodeWithTargetService == self.podWithTargetService.node)
    def effect(self):
        self.request1.status = "directedToNode"
        self.request1.toNode = nodeWithTargetService

    
class ToNode(PlannedAction):
    cost = 1 
    request1 = Select( Request.status == "directedToNode")

    def selector(self):
        return Select( self.request1.toNode.status == "active")

    def effect(self):
        self.request1.status = "atKubeproxy"
        self.request1.toNode = None 
        self.request1.atNode = request1.toNode


class SwitchToNextNode(PlannedAction):
    cost = 1
    request1 = Select( Request.status == "directedToNode")
    nextNode1 = Select( Node.prevNode == request1.toNode)
    def selector(self):
        return Select( self.request1.toNode.status == "inactive") 

    def effect(self):
        self.request1.toNode = self.nextNode1


class DirectToPod(PlannedAction):
    cost = 1
    request1 = Request()
    targetService = Select( request1.status == "atKubeproxy" and Service == request1.targetService)
    podWithTargetService = Select( Pod == targetService.selectionedPod)
    currectNode = Select( Node == request1.node)


    def selector(self):
        return Select( self.podWithTargetService == self.request1.atNode)

    def effect(self):
        self.request1.status = "directedToPod"
        self.request1.toPod = podWithTargetService


class ToPod(PlannedAction):
    cost = 1 
    request1 = Select( Request.status == "directedToPod")

    def selector(self):
        return Select(self.request1.toPod.status == "active") 

    def effect(self):
        self.request1.status = "atPodInput"
        self.request1.toPod = None 
        self.request1.atPod = request1.toPod


print(ToPod.compile())

class SwitchToNextPod(PlannedAction):
    cost = 1
    request1 = Select( Request.status == "directedToPod")
    nextPod1 = Select( Pod.prevPod == request1.toPod)
    nodeForPod = Select( Node == request1.toPod.atNode)
    kubeproxyatNode = Select( Kubeproxy.atNode == nodeForPod)
    def selector(self):
        return Select(self.request1.toPod.status == "inactive" and \
        self.kubeproxyatNode.mode == "usermode") 
    def effect(self):
        self.request1.toPod = self.nextPod1



class ConsumeResource(PlannedAction):
    cost = 1
    request1 = Select( Request.status == "atPodInput")
    currentPod = Select( Pod == request1.atPod)
    currentNode = Select( Node == request1.atNode)

    addedCpuConsumptionAtCurrentPod1 = Select( currentPod.currentCpuConsumption == AddedNumber.operator1) and \
    Select( request1.cpuRequest == AddedNumber.operator2)
    
    addedMemConsumptionAtCurrentPod1 = Select( currentPod.currentMemConsumption == AddedNumber.operator1) and \
    Select( request1.memRequest == AddedNumber.operator2)
    
    addedCpuConsumptionAtCurrentNode1 = Select( currentNode.currentCpuConsumption == AddedNumber.operator1) and \
    Select( request1.cpuRequest == AddedNumber.operator2)
    
    addedMemConsumptionAtCurrentNode1 = Select( currentNode.currentMemConsumption == AddedNumber.operator1) and \
    Select( request1.memRequest == AddedNumber.operator2)


    def effect(self):
        self.request1.status.set("resourcesConsumed")
        self.currentPod.currentCpuConsumption.set(addedCpuConsumptionAtCurrentPod1.result)
        self.currentPod.currentMemConsumption.set(addedMemConsumptionAtCurrentPod1.result)
        self.currentNode.currentCpuConsumption.set(addedCpuConsumptionAtCurrentNode1.result)
        self.currentNode.currentMemConsumption.set(addedMemConsumptionAtCurrentNode1.result)
 

class ProcessTempRequest(PlannedAction):
    cost = 1
    request1 = Select(Request.status == "resourcesConsumed")
    
    def selector(self):
        return Select(self.request1.type == "temporary")
    
    def effect(self):
        self.request1.status.set("requestPIDToBeEnded")
        
class ProcessPersistentRequest(PlannedAction):
    cost = 1
    request1 = Select(Request.status == "resourcesConsumed")
    def selector(self):
        return Select(self.request1.type != "temporary")

    def effect(self):
        self.request1.status.set("requestFinished")


class ReleaseResource(PlannedAction):
    cost = 1
    request1 = Select( Request.status == "requestPIDToBeEnded")
    currentPod = Select( Pod == request1.atPod)
    currentNode = Select( Node == request1.atNode)

    reducedCpuConsumptionAtCurrentPod1 = Select( currentPod.currentCpuConsumption == AddedNumber.result) and \
    Select( request1.cpuRequest == AddedNumber.operator2)
    
    reducedMemConsumptionAtCurrentPod1 = Select( currentPod.currentMemConsumption == AddedNumber.result) and \
    Select( request1.memRequest == AddedNumber.operator2)
    
    reducedCpuConsumptionAtCurrentNode1 = Select( currentNode.currentCpuConsumption == AddedNumber.result) and \
    Select( request1.cpuRequest == AddedNumber.operator2)
    
    reducedMemConsumptionAtCurrentNode1 = Select( currentNode.currentMemConsumption == AddedNumber.result) and \
    Select( request1.memRequest == AddedNumber.operator2)


    def effect(self):
        self.request1.status.set("resourcesReleased")
        self.currentPod.currentCpuConsumption.set(addedCpuConsumptionAtCurrentPod1.operator1)
        self.currentPod.currentMemConsumption.set(addedMemConsumptionAtCurrentPod1.operator1)
        self.currentNode.currentCpuConsumption.set(addedCpuConsumptionAtCurrentNode1.operator1)
        self.currentNode.currentMemConsumption.set(addedMemConsumptionAtCurrentNode1.operator1) 
    
class FinishRequest(PlannedAction):
    cost = 1
    request1 = Select( Request.status == "resourcesReleased")
    pod1 = Select(Pod == request1.atPod and Pod.podIsOnetime != True)
    
    def effect(self):
        self.request1.status.set("requestFinished")
        self.request1.atPod.unset()
        self.request1.atNode.unset()


class TerminatePodAfterFinish(PlannedAction):
    cost = 1
    request1 = Select( Request.status == "resourcesReleased")
    pod1 = Select(Pod == request1.atPod and Pod.podIsOnetime == True)
    
    def effect(self):
        self.request1.status.set("requestFinished")
        self.request1.atPod.unset()
        self.request1.atNode.unset()
        self.pod1.status.set("toBeTerminated")

class TerminatePodAfterFinish(PlannedAction):
    cost = 1
    pod1 = Select( Pod.status == "toBeTerminated")
    currentNode = Select( Node == pod1.atNode)
    reducedCpuConsumptionAtCurrentNode1 = Select( currentNode.currentCpuConsumption == AddedNumber.result) and \
    Select( pod1.currentCpuConsumption == AddedNumber.operator2)
    
    reducedMemConsumptionAtCurrentNode1 = Select( currentNode.currentMemConsumption == AddedNumber.result) and \
    Select( pod1.memCurrentConsumption == AddedNumber.operator2)
    def effect(self):
        self.node1.set("inactive") #TODO: divide status and state  for POds. state is to be active and nonactive. and status  would also include intermediate substates        

        
        
class updatePodMetricsInc(PlannedAction):
    cost = 1
    request1 = Select( Request.status == "resourcesReleased")

    def effect(self):
        self.request1.status.set("requestReleasedLimitsUpdated")
        self.request1.atPod.unset()
        self.request1.atNode.unset()
     
        

# class IncreasePodConsumtionStart(PlannedAction):
#     cost = 1
#     request1 = Request.status == "atPodInput"
    
#     def selector(self):
#         return self.request1.status == "atPodInputStartCalc"

#     def effect(self):
#         self.request1.cpuCalculation = self.request1.cpuRequest
#             request1 = request1.cpuCalculation == request1.
            
        