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
        node1: Node):
        assert pod1.atNode == self.nodenull
        assert node1 == node1
        
        pod1.status = self.constSymbol["statusPodActive"]
        pod1.atNode = node1

    @planned
    def ReqToPod(self,
        request1: Request,
        podWithTargetService: Pod,
        currentNode: Node,
        addedCpuConsumptionAtPod1_res: AddedNumber,
        addedCpuConsumptionAtPod1_res_num: Number,
        addedCpuConsumptionAtCurrentNode1_res: AddedNumber,
        addedCpuConsumptionAtCurrentNode1_res_num: Number,
        addedMemConsumptionAtPod1_res: AddedNumber,
        addedMemConsumptionAtPod1_res_num: Number,
        addedMemConsumptionAtCurrentNode1_res: AddedNumber,
        addedMemConsumptionAtCurrentNode1_res_num: Number
        ):
            
        assert currentNode == request1.atNode  and \
        podWithTargetService.targetService == request1.targetService and \
        currentNode == podWithTargetService.atNode and \
        podWithTargetService.status == self.constSymbol["statusPodActive"] and \
        currentNode.status == self.constSymbol["statusNodeActive"]

        assert addedCpuConsumptionAtPod1_res.operator1 == podWithTargetService.currentRealCpuConsumption
        assert addedCpuConsumptionAtPod1_res.operator2 == request1.cpuRequest
        assert addedCpuConsumptionAtCurrentNode1_res.operator1 == currentNode.currentRealCpuConsumption
        assert addedCpuConsumptionAtCurrentNode1_res.operator2 == request1.cpuRequest
        assert addedCpuConsumptionAtCurrentNode1_res_num == addedCpuConsumptionAtCurrentNode1_res.result
        assert addedMemConsumptionAtPod1_res.operator1 == podWithTargetService.currentRealMemConsumption
        assert addedMemConsumptionAtPod1_res.operator2 == request1.memRequest
        assert addedMemConsumptionAtPod1_res_num == addedMemConsumptionAtPod1_res.result
        assert addedMemConsumptionAtCurrentNode1_res.operator1 == currentNode.currentRealMemConsumption
        assert addedMemConsumptionAtCurrentNode1_res.operator2 == request1.memRequest
        assert addedMemConsumptionAtCurrentNode1_res_num == addedMemConsumptionAtCurrentNode1_res.result

        # podWithTargetService.currentRealCpuConsumption = addedCpuConsumptionAtPod1_res_num
        # currentNode.currentRealCpuConsumption = addedCpuConsumptionAtCurrentNode1_res_num
        # podWithTargetService.currentRealMemConsumption = addedMemConsumptionAtPod1_res_num
        # currentNode.currentRealMemConsumption = addedMemConsumptionAtCurrentNode1_res_num

        request1.atPod = podWithTargetService

            

 
# p = Problem1()
# # print(ForwardPacketToInterface.compile_clips(p))
# p.run()
# for i in p.plan: print(i)
  
