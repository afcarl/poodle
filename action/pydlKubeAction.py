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
        request1.status == self.constSymbol['statusReqAtLoadbalancer']
        
        request1.atNode = nextNodeToBeUsedByLb
        loadbalancerAtWhichRequestIs.lastNode = nextNodeToBeUsedByLb
        self.request1.status == self.constSymbol['statusReqDirectedToNode']

    @planned
    def ReqToNextNodeRR(self,
            request1: Request, 
            nodeAtWhichRequestIs: Node,
            nextNodeAccordingToRoundRobin: Node):

        assert nodeAtWhichRequestIs == request1.atNode and \
        nextNodeAccordingToRoundRobin.prevNode == nodeAtWhichRequestIs
        
        request1.atNode = nextNodeAccordingToRoundRobin
        

pp = PacketActionModel()
print(pp.ReqToNodeFromLb.plan_class.compile(pp))
 
# p = Problem1()
# # print(ForwardPacketToInterface.compile_clips(p))
# p.run()
# for i in p.plan: print(i)
  
