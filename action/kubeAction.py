from poodle import * 

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
            
        