from poodle.poodle import *
from object.kubeObject import *
from problem.problemTemplate import *

class PacketActionModel:
    
    @planned # also @chained
    def ReqToNodeFromLb(self, 
            request1: Request, 
            loadbalancerAtWhichRequestIs: Loadbalancer,
            lastNodeUsedByLb: Node,
            nextNodeToBeUsedByLb: Node):

        assert loadbalancerAtWhichRequestIs == request1.atLb and \
        nextNodeToBeUsedByLb.prevNode == loadbalancerAtWhichRequestIs.lastNode and \
        request1.isAtLoadbalancer == True
        assert request1.status == self.constSymbol["statusReqAtStart"]
        
        request1.atNode = nextNodeToBeUsedByLb
        loadbalancerAtWhichRequestIs.lastNode = nextNodeToBeUsedByLb

        request1.atNode = nextNodeToBeUsedByLb
        loadbalancerAtWhichRequestIs.lastNode = nextNodeToBeUsedByLb
        request1.isAtLoadbalancer = False
        request1.status = self.constSymbol["statusReqAtKubeproxy"]

    @planned
    def ReqToNextNodeRR(self,
        request1: Request, 
        nodeAtWhichRequestIs: Node,
        nextNodeAccordingToRoundRobin: Node):

        assert nodeAtWhichRequestIs == request1.atNode and \
        nextNodeAccordingToRoundRobin.prevNode == nodeAtWhichRequestIs
        
        request1.atNode = nextNodeAccordingToRoundRobin
        

    @planned
    def PodStarted(self,
        pod1: Pod,
        node1: Node,
        newFormalMemConsumptionAtNode_res: AddedNumber,
        newFormalMemConsumptionAtNode_res_num: Number,
        memCapacityPlusOne_res: AddedNumber,
        memCapacityPlusOne_res_num: Number,
        greaterThanMem: GreaterThan,
        greaterThanCpu: GreaterThan
        ):
        assert pod1.atNode == self.nodenull
        assert newFormalMemConsumptionAtNode_res.operator1 == node1.currentFormalMemConsumption
        assert newFormalMemConsumptionAtNode_res.operator2 == pod1.requestedMem
        assert newFormalMemConsumptionAtNode_res_num == newFormalMemConsumptionAtNode_res.result
        
        assert memCapacityPlusOne_res.operator1 == node1.memCapacity
        assert memCapacityPlusOne_res.operator2 == self.numberFactory.getNumber(1)
        assert memCapacityPlusOne_res_num == memCapacityPlusOne_res.result 
        
        assert greaterThanMem.lower == newFormalMemConsumptionAtNode_res_num
        assert greaterThanMem.higher == memCapacityPlusOne_res_num
        
        pod1.status = self.constSymbol["statusPodActive"]
        pod1.atNode = node1

  
    #to-do: Soft conditions are not supported yet ( prioritization of nodes :  for example healthy  nodes are selected  rather then non healthy if pod  requests such behavior 
    def selector(self):
        return Select( self.pod1.status == self.problem.constSymbol['statusPodPending'] and \
        self.num1 == self.problem.numberFactory.getNumber(1))
        
    def effect(self):
        self.pod1.status.set(self.problem.constSymbol['statusPodBindedToNode'])
        self.pod1.bindedToNode.init_unsafe(self.node1)
        self.node1.currentFormalMemConsumption.set(self.newFormalMemConsumptionAtNode_res_num)
        self.node1.currentFormalCpuConsumption.set(self.newFormalCpuConsumptionAtNode_res_num)



    @planned
    def TechConsumeCpuForReqToPod(self,
        request1: Request,
        podWithTargetService: Pod,
        currentNode: Node,
        addedCpuConsumptionAtPod1_res: AddedNumber,
        addedCpuConsumptionAtPod1_res_num: Number,
        addedCpuConsumptionAtCurrentNode1_res: AddedNumber,
        addedCpuConsumptionAtCurrentNode1_res_num: Number,
        increasedByOneCpuCapacity_res: AddedNumber,
        greaterThanCpu: GreaterThan,
        ):
            
        assert currentNode == request1.atNode  and \
        podWithTargetService.targetService == request1.targetService and \
        currentNode == podWithTargetService.atNode and \
        podWithTargetService.status == self.constSymbol["statusPodActive"] and \
        currentNode.status == self.constSymbol["statusNodeActive"]

        assert addedCpuConsumptionAtPod1_res.operator1 == podWithTargetService.currentRealCpuConsumption
        assert addedCpuConsumptionAtPod1_res.operator2 == request1.cpuRequest
        assert addedCpuConsumptionAtPod1_res_num == addedCpuConsumptionAtPod1_res.result
        assert addedCpuConsumptionAtCurrentNode1_res.operator1 == currentNode.currentRealCpuConsumption
        assert addedCpuConsumptionAtCurrentNode1_res.operator2 == request1.cpuRequest
        assert addedCpuConsumptionAtCurrentNode1_res_num == addedCpuConsumptionAtCurrentNode1_res.result

        assert increasedByOneCpuCapacity_res.operator1 == currentNode.cpuCapacity#              |
        assert increasedByOneCpuCapacity_res.operator2 == self.numberFactory.getNumber(1)#      |
        assert greaterThanCpu.lower == currentNode.currentRealCpuConsumption#                      |
        assert greaterThanCpu.higher == addedCpuConsumptionAtCurrentNode1_res_num#                      |
     
        podWithTargetService.currentRealCpuConsumption = addedCpuConsumptionAtPod1_res_num
        currentNode.currentRealCpuConsumption = addedCpuConsumptionAtCurrentNode1_res_num
        request1.cpuRequestConsumed = True


    @planned
    def TechConsumeMemForReqToPod(self,
        request1: Request,
        podWithTargetService: Pod,
        currentNode: Node,
        addedMemConsumptionAtPod1_res: AddedNumber,
        addedMemConsumptionAtPod1_res_num: Number,
        addedMemConsumptionAtCurrentNode1_res: AddedNumber,
        addedMemConsumptionAtCurrentNode1_res_num: Number,
        increasedByOneMemCapacity_res: AddedNumber,
        greaterThanMem: GreaterThan
        ):
            
        assert currentNode == request1.atNode  and \
        podWithTargetService.targetService == request1.targetService and \
        currentNode == podWithTargetService.atNode and \
        podWithTargetService.status == self.constSymbol["statusPodActive"] and \
        currentNode.status == self.constSymbol["statusNodeActive"]

        assert addedMemConsumptionAtPod1_res.operator1 == podWithTargetService.currentRealMemConsumption
        assert addedMemConsumptionAtPod1_res.operator2 == request1.memRequest
        assert addedMemConsumptionAtPod1_res_num == addedMemConsumptionAtPod1_res.result
        assert addedMemConsumptionAtCurrentNode1_res.operator1 == currentNode.currentRealMemConsumption
        assert addedMemConsumptionAtCurrentNode1_res.operator2 == request1.memRequest
        assert addedMemConsumptionAtCurrentNode1_res_num == addedMemConsumptionAtCurrentNode1_res.result

        assert increasedByOneMemCapacity_res.operator1 == currentNode.memCapacity#          -----
        assert increasedByOneMemCapacity_res.operator2 == self.numberFactory.getNumber(1)#      |
        assert greaterThanMem.lower == addedMemConsumptionAtCurrentNode1_res_num#                      |   from class ConsumeResource(PlannedAction)
        assert greaterThanMem.higher == increasedByOneMemCapacity_res.result#                      |

        podWithTargetService.currentRealMemConsumption = addedMemConsumptionAtPod1_res_num# ---TODO too slowwwww
        currentNode.currentRealMemConsumption = addedMemConsumptionAtCurrentNode1_res_num#   --/
        request1.memRequestConsumed = True

    @planned
    def ReqToPod(self,
        request1: Request,
        podWithTargetService: Pod,
        currentNode: Node):
            
        assert currentNode == request1.atNode
        assert podWithTargetService.targetService == request1.targetService
        assert currentNode == podWithTargetService.atNode
        assert podWithTargetService.status == self.constSymbol["statusPodActive"]
        assert currentNode.status == self.constSymbol["statusNodeActive"]
        assert request1.cpuRequestConsumed == True
        assert request1.memRequestConsumed == True

        request1.atPod = podWithTargetService

#class ProcessPersistentRequest(PlannedAction):
    @planned
    def ProcessPersistentRequest(self,
        request1: Request,
        pod1: Pod
        ):
    
        assert request1.atPod == pod1
        assert request1.type == self.constSymbol['typePersistent']
 
        # request1.atPod = pod1
        request1.isFinished = True
        
# p = Problem1()
# # print(ForwardPacketToInterface.compile_clips(p))
# p.run()
# for i in p.plan: print(i)
  
