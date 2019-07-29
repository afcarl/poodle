from poodle.poodle import * 
from action.pydlKubeAction import *
from object.kubeObject import *

from problem.problemTemplate import ProblemTemplate
from object.commonObject import *
from object.addedNumbers10 import *

class Problem1(ProblemTemplate, PacketActionModel):

    def problem(self):
        super().problem()
        self.period1 = self.addObject(Period()) 
        
        self.сontainerConfig1 = self.addObject(ContainerConfig())
        self.сontainerConfig2 = self.addObject(ContainerConfig())
        self.сontainerConfig3 = self.addObject(ContainerConfig())
        
        self.nullLink = self.addObject( Loadbalancer('Null'))
        
        self.nodenull = self.addObject(Node('Null'))
        self.nodenull.state = self.constSymbol["stateNodeInactive"]
        
        self.node1 = self.addObject(Node('node1'))
        self.node1.state = self.constSymbol["stateNodeActive"]
        self.node1.status = self.constSymbol["statusNodeActive"] ##TODO - make Node activation mechanism
        self.node1.cpuCapacity = self.numberFactory.getNumber(4)
        self.node1.memCapacity = self.numberFactory.getNumber(4)
        self.node1.currentFormalCpuConsumption = self.numberFactory.getNumber(0)
        self.node1.currentFormalMemConsumption = self.numberFactory.getNumber(0)
        self.node1.currentRealMemConsumption = self.numberFactory.getNumber(0)
        self.node1.currentRealCpuConsumption = self.numberFactory.getNumber(0)
        self.node1.AmountOfPodsOverwhelmingMemLimits = self.numberFactory.getNumber(0)


        self.node2 = self.addObject(Node('node2'))
        self.node2.state = self.constSymbol["stateNodeActive"]
        self.node2.status = self.constSymbol["statusNodeActive"]
        self.node2.cpuCapacity = self.numberFactory.getNumber(4)
        self.node2.memCapacity = self.numberFactory.getNumber(4)
        self.node2.currentFormalCpuConsumption = self.numberFactory.getNumber(0)
        self.node2.currentFormalMemConsumption = self.numberFactory.getNumber(0)
        self.node2.currentRealMemConsumption = self.numberFactory.getNumber(0)
        self.node2.currentRealCpuConsumption = self.numberFactory.getNumber(0)
        self.node2.AmountOfPodsOverwhelmingMemLimits = self.numberFactory.getNumber(0)

        self.node3 = self.addObject(Node('node3'))
        self.node3.state = self.constSymbol["stateNodeActive"]
        self.node3.status = self.constSymbol["statusNodeActive"]
        self.node3.cpuCapacity = self.numberFactory.getNumber(1)
        self.node3.memCapacity = self.numberFactory.getNumber(1)
        self.node3.currentFormalCpuConsumption = self.numberFactory.getNumber(0)
        self.node3.currentFormalMemConsumption = self.numberFactory.getNumber(0)
        self.node3.currentRealMemConsumption = self.numberFactory.getNumber(0)
        self.node3.currentRealCpuConsumption = self.numberFactory.getNumber(0)
        self.node3.AmountOfPodsOverwhelmingMemLimits = self.numberFactory.getNumber(0)


        self.node3.prevNode = self.node2
        self.node2.prevNode = self.node1
        self.node1.prevNode = self.node3        
        
        self.nullPod = self.addObject(Pod('nullPod'))
        self.pod1 = self.addObject(Pod('pod1'))
        self.pod1.podConfig = self.сontainerConfig1
        self.pod1.currentRealCpuConsumption = self.numberFactory.getNumber(0)
        self.pod1.currentRealMemConsumption = self.numberFactory.getNumber(0)
        self.pod1.status = self.constSymbol["statusPodAtConfig"]
        self.pod1.state = self.constSymbol["statePodInactive"]
        self.pod1.requestedMem = self.numberFactory.getNumber(1)
        self.pod1.requestedCpu = self.numberFactory.getNumber(1)
        self.pod1.podNotOverwhelmingLimits = True
        self.pod1.realInitialMemConsumption = self.numberFactory.getNumber(1)
        self.pod1.realInitialCpuConsumption = self.numberFactory.getNumber(1)
        self.pod1.type = self.constSymbol["typeTemporary"]
        self.pod1.memLimit =  self.numberFactory.getNumber(1)
        self.pod1.cpuLimit =  self.numberFactory.getNumber(1)
        self.pod1.atNode = self.nodenull


        
        self.pod2 = self.addObject(Pod('pod2'))
        self.pod2.podConfig = self.сontainerConfig2
        self.pod2.currentRealCpuConsumption = self.numberFactory.getNumber(0)
        self.pod2.currentRealMemConsumption = self.numberFactory.getNumber(0)
        self.pod2.status = self.constSymbol["statusPodAtConfig"]
        self.pod2.state = self.constSymbol["statePodInactive"]
        self.pod2.requestedMem = self.numberFactory.getNumber(1)
        self.pod2.requestedCpu = self.numberFactory.getNumber(1)
        self.pod2.podNotOverwhelmingLimits = True
        self.pod2.realInitialMemConsumption = self.numberFactory.getNumber(1)
        self.pod2.realInitialCpuConsumption = self.numberFactory.getNumber(1)        
        self.pod2.type = self.constSymbol["typeTemporary"]
        self.pod2.memLimit =  self.numberFactory.getNumber(3)
        self.pod2.cpuLimit =  self.numberFactory.getNumber(3)
        self.pod2.prevPod = self.pod1         
        self.pod2.atNode = self.nodenull        
        ## to-do:  for relations  it should give helpful error message when = instead of add.
        
        self.pod3 = self.addObject(Pod('pod3'))
        self.pod3.podConfig = self.сontainerConfig1
        self.pod3.currentRealCpuConsumption = self.numberFactory.getNumber(0)
        self.pod3.currentRealMemConsumption = self.numberFactory.getNumber(0)
        self.pod3.status = self.constSymbol["statusPodAtConfig"]
        self.pod3.state = self.constSymbol["statePodInactive"]
        self.pod3.requestedMem = self.numberFactory.getNumber(1)
        self.pod3.requestedCpu = self.numberFactory.getNumber(1)
        self.pod3.podNotOverwhelmingLimits = True
        self.pod3.realInitialMemConsumption = self.numberFactory.getNumber(1)
        self.pod3.realInitialCpuConsumption = self.numberFactory.getNumber(1)
        self.pod3.type = self.constSymbol["typePersistent"]
        self.pod3.memLimit =  self.numberFactory.getNumber(2)
        self.pod3.cpuLimit =  self.numberFactory.getNumber(2)
        self.pod3.atNode = self.nodenull        
        
        
        self.pod3.prevPod = self.pod2
        self.pod1.prevPod = self.pod3
        

        
        self.service1 = self.addObject(Service('service1'))
        self.service2 = self.addObject(Service('service2'))
        
        self.service2.selectionedPod.add(self.pod3)
        self.service1.selectionedPod.add(self.pod2)
        self.service1.selectionedPod.add(self.pod1)

        self.pod1.targetService = self.service1
        self.pod2.targetService = self.service1
        self.pod3.targetService = self.service2

        self.lb1 = self.addObject(Loadbalancer())
        self.lb1.atNode = self.node1
        self.lb1.selectionedService.add(self.service1)
        self.lb1.selectionedService.add(self.service2)
        self.lb1.lastNode = self.node1

        self.сontainerConfig1.service = self.service1
        self.сontainerConfig2.service = self.service2   

        
        self.request1 = self.addObject(Request('request1'))
        self.request1.launchPeriod = self.period1
        self.request1.status = self.constSymbol["statusReqAtStart"]
        self.request1.state = self.constSymbol["stateRequestInactive"]
        self.request1.targetService = self.service1
        self.request1.cpuRequest = self.numberFactory.getNumber(2)
        self.request1.memRequest = self.numberFactory.getNumber(2)
        self.request1.type = self.constSymbol["typeTemporary"]
        self.request1.atLb = self.lb1
        self.request1.isAtLoadbalancer = True
        self.request1.atPod = self.nullPod

        self.request2 = self.addObject(Request())
        self.request2.launchPeriod = self.period1
        self.request2.status = self.constSymbol["statusReqAtStart"]
        self.request2.state = self.constSymbol["stateRequestInactive"]
        self.request2.targetService = self.service1
        self.request2.cpuRequest = self.numberFactory.getNumber(2)
        self.request2.memRequest = self.numberFactory.getNumber(2)
        self.request2.type = self.constSymbol["typePersistent"]
        self.request2.atLb = self.lb1
        self.request2.isAtLoadbalancer = True
        self.request2.atPod = self.nullPod

        self.request3 = self.addObject(Request())
        self.request3.launchPeriod = self.period1
        self.request3.status = self.constSymbol["statusReqAtStart"]
        self.request3.state = self.constSymbol["stateRequestInactive"]
        self.request3.targetService = self.service1
        self.request3.cpuRequest = self.numberFactory.getNumber(1)
        self.request3.memRequest = self.numberFactory.getNumber(1)
        self.request3.type = self.constSymbol["typePersistent"]
        self.request3.atLb = self.lb1
        self.request3.isAtLoadbalancer = True
        self.request3.atPod = self.nullPod


        # self.request4 = self.addObject(Request())
        # self.request4.launchPeriod = self.period1
        # self.request4.status = self.constSymbol["statusReqAtStart"]
        # self.request4.state = self.constSymbol["stateRequestInactive"]
        # self.request4.targetService = self.service2
        # self.request4.cpuRequest = self.numberFactory.getNumber(1)
        # self.request4.memRequest = self.numberFactory.getNumber(1)
        # self.request4.type = self.constSymbol["typePersistent"]
        # self.request4.atLb = self.lb1
        # self.request4.isAtLoadbalancer = True
        
        # self.request5 = self.addObject(Request())
        # self.request5.launchPeriod = self.period1
        # self.request5.status = self.constSymbol["statusReqAtStart"]
        # self.request5.state = self.constSymbol["stateRequestInactive"]
        # self.request5.targetService = self.service2
        # self.request5.cpuRequest = self.numberFactory.getNumber(1)
        # self.request5.memRequest = self.numberFactory.getNumber(1)
        # self.request5.type = self.constSymbol["typePersistent"]
        # self.request5.atLb = self.lb1
        # self.request5.isAtLoadbalancer = True
        
        # self.request6 = self.addObject(Request())
        # self.request6.launchPeriod = self.period1
        # self.request6.status = self.constSymbol["statusReqAtStart"]
        # self.request6.state = self.constSymbol["stateRequestInactive"]
        # self.request6.targetService = self.service2
        # self.request6.cpuRequest = self.numberFactory.getNumber(1)
        # self.request6.memRequest = self.numberFactory.getNumber(1)
        # self.request6.type = self.constSymbol["typePersistent"]
        # self.request6.atLb = self.lb1
        
        # self.request7 = self.addObject(Request())
        # self.request7.launchPeriod = self.period1
        # self.request7.status = self.constSymbol["statusReqAtStart"]
        # self.request7.state = self.constSymbol["stateRequestInactive"]
        # self.request7.targetService = self.service2
        # self.request7.cpuRequest = self.numberFactory.getNumber(1)
        # self.request7.memRequest = self.numberFactory.getNumber(1)
        # self.request7.type = self.constSymbol["typePersistent"]
        # self.request7.atLb = self.lb1
        

        # self.request8 = self.addObject(Request())
        # self.request8.launchPeriod = self.period1
        # self.request8.status = self.constSymbol["statusReqAtStart"]
        # self.request8.state = self.constSymbol["stateRequestInactive"]
        # self.request8.targetService = self.service2
        # self.request8.cpuRequest = self.numberFactory.getNumber(1)
        # self.request8.memRequest = self.numberFactory.getNumber(1)
        # self.request8.type = self.constSymbol["typePersistent"]
        # self.request8.atLb = self.lb1
        

        # self.request9 = self.addObject(Request())
        # self.request9.launchPeriod = self.period1
        # self.request9.status = self.constSymbol["statusReqAtStart"]
        # self.request9.state = self.constSymbol["stateRequestInactive"]
        # self.request9.targetService = self.service2
        # self.request9.cpuRequest = self.numberFactory.getNumber(1)
        # self.request9.memRequest = self.numberFactory.getNumber(1)
        # self.request9.type = self.constSymbol["typePersistent"]
        # self.request9.atLb = self.lb1


        # self.request10 = self.addObject(Request())
        # self.request10.launchPeriod = self.period1
        # self.request10.status = self.constSymbol["statusReqAtStart"]
        # self.request10.state = self.constSymbol["stateRequestInactive"]
        # self.request10.targetService = self.service2
        # self.request10.cpuRequest = self.numberFactory.getNumber(1)
        # self.request10.memRequest = self.numberFactory.getNumber(1)
        # self.request10.type = self.constSymbol["typePersistent"]
        # self.request10.atLb = self.lb1

        # self.request11 = self.addObject(Request())
        # self.request11.launchPeriod = self.period1
        # self.request11.status = self.constSymbol["statusReqAtStart"]
        # self.request11.state = self.constSymbol["stateRequestInactive"]
        # self.request11.targetService = self.service2
        # self.request11.cpuRequest = self.numberFactory.getNumber(1)
        # self.request11.memRequest = self.numberFactory.getNumber(1)
        # self.request11.type = self.constSymbol["typePersistent"]
        # self.request11.atLb = self.lb1
#Todo: request of pod are temporary ? 


        
        self.modeUsermode = self.addObject(Mode())
        self.modeIptables = self.addObject(Mode())
        
        
        self.kp1 = self.addObject(Kubeproxy())
        self.kp1.mode = self.constSymbol["modeUsermode"]
        self.kp1.atNode = self.node1
        self.kp1.lastPod = self.pod1
        ## how to create relations??? 
        
        self.kp2 = self.addObject(Kubeproxy())
        self.kp2.mode = self.constSymbol["modeUsermode"]
        self.kp2.atNode = self.node2
        self.kp2.lastPod = self.pod1
        
        self.kp3 = self.addObject(Kubeproxy())
        self.kp3.mode = self.constSymbol["modeUsermode"]
        self.kp3.atNode = self.node3
        self.kp3.lastPod = self.pod1
        
        self.globalVar1 = self.addObject(GlobalVar())
        self.globalVar1.numberOfRejectedReq = self.numberFactory.getNumber(0)
        self.globalVar1.lastPod = self.pod1
        
        
        


    def goal(self):
        return self.request1.atNode == self.node2 and \
        self.request2.atNode == self.node2 and \
        self.request1.atPod == self.pod1 and \
        self.request2.atPod == self.pod1 and \
        self.node2.currentRealCpuConsumption == self.numberFactory.getNumber(4) and\
        self.node2.currentRealMemConsumption == self.numberFactory.getNumber(4) and\
        self.request2.isFinished == True
        
        # return self.pod1.atNode == self.node1

        # self.request1.status == self.constSymbol["statusReqRequestFinished"] and \
        # self.request2.status == self.constSymbol["statusReqRequestFinished"]  and \
        # self.request3.status == self.constSymbol["statusReqRequestFinished"] 
        # # self.request4.status == self.constSymbol["statusReqRequestFinished"] and \
        # self.request5.status == self.constSymbol["statusReqRequestFinished"] and \
        # self.request6.status == self.constSymbol["statusReqRequestFinished"] and \
        # self.request7.status == self.constSymbol["statusReqRequestFinished"] and \
        # self.request8.status == self.constSymbol["statusReqRequestFinished"] and \
        # self.request9.status == self.constSymbol["statusReqRequestFinished"] and \
        # self.request10.status == self.constSymbol["statusReqRequestFinished"] and \
        # self.request11.status == self.constSymbol["statusReqRequestFinished"] 
        # and
        # self.lb1.switchingPerformed == True
        # self.pod1.status == self.constSymbol["statusNodeOomKilling"] 
        # self.pod3.podOverwhelmingLimits == True
        
        


    
        
    # def solution(self):
    #     return[
    #         #!!  - peristent request 1
    #         ReadDeploymentConfig, 
    #         SchedulerNofityUnboundPod, 
    #         KubectlStartsPod, 
    #         ReqReceivedByLB, 
    #         ReqSentToNodeByLb, 
    #         ReqReceivedByNodeFromLb, 
    #          ReqLbSwichedNodeByRoundRobinAlg, 
    #         ReqDirectedByKPToNextPodByRRAlg, 
    #         ReqReceivedByPod, 
    #         ConsumeResourceMem, 
    #         ConsumeResourceCpu, 
    #         ConsumeResource, 
    #         ProcessPersistentRequest, 
    #         #pod2 - temporary request 2
    #         ReadDeploymentConfig, 
    #         SchedulerNofityUnboundPod, 
    #         KubectlStartsPod, 
    #         ReqReceivedByLB, 
    #         ReqSentToNodeByLb, 
    #         ReqReceivedByNodeFromLb, 
    #          ReqLbSwichedNodeByRoundRobinAlg, 
    #         ReqDirectedByKPToNextPodByRRAlg, 
    #         ReqReceivedByPod, 
    #         ConsumeResourceMem, 
    #         ConsumeResourceCpu, 
    #         ConsumeResource, 
    #         ProcessTempRequest, 
    #         ReleaseResourceCpu, 
    #         ReleaseResourceMem, 
    #         ReleasedResources, 
    #         FinishRequest, 
    #         #pod3 - persistent request 3
    #         ReadDeploymentConfig, 
    #         SchedulerNofityUnboundPod, 
    #         KubectlStartsPod, 
    #         ReqReceivedByLB, 
    #         ReqSentToNodeByLb, 
    #         ReqReceivedByNodeFromLb, 
    #          ReqLbSwichedNodeByRoundRobinAlg, 
    #         ReqDirectedByKPToNextPodByRRAlg, 
    #         ReqReceivedByPod, 
    #         ConsumeResourceMem, 
    #         ConsumeResourceCpu, 
    #         ConsumeResource, 
    #         ProcessPersistentRequest, 
    #         #pod4 - persistent request 4
    #         ReadDeploymentConfig, 
    #         SchedulerNofityUnboundPod, 
    #         KubectlStartsPod, 
    #         ReqReceivedByLB, 
    #         ReqSentToNodeByLb, 
    #         ReqReceivedByNodeFromLb, 
    #          ReqLbSwichedNodeByRoundRobinAlg, 
    #         ReqDirectedByKPToNextPodByRRAlg, 
    #         ReqReceivedByPod, 
    #         ConsumeResourceMem, 
    #         ConsumeResourceCpu, 
    #         ConsumeResource, 
    #         ProcessPersistentRequest, 
    #         #pod5 - persistent request 5
    #         ReadDeploymentConfig, 
    #         SchedulerNofityUnboundPod, 
    #         KubectlStartsPod, 
    #         ReqReceivedByLB, 
    #         ReqSentToNodeByLb, 
    #         ReqReceivedByNodeFromLb, 
    #          ReqLbSwichedNodeByRoundRobinAlg, 
    #         ReqDirectedByKPToNextPodByRRAlg, 
    #         ReqReceivedByPod, 
    #         ConsumeResourceMem, 
    #         ConsumeResourceCpu, 
    #         ConsumeResource, 
    #         ProcessPersistentRequest, 
    #         # - persistent request 6. Not enough Mem. OomKill anouther pod overwhelming limits    
    #         ReadDeploymentConfig, 
    #         SchedulerNofityUnboundPod, 
    #         KubectlStartsPod, 
    #         ReqReceivedByLB, 
    #         ReqSentToNodeByLb, 
    #         ReqReceivedByNodeFromLb, 
    #         MarkPodAsOverwhelmingMemLimits, 
    #         MemoryErrorKillPodOverwhelmingLimits, 
    #         PodFailsBecauseOfKilling, 
    #         ReqDirectedByKPToNextPodByRRAlg, 
    #         ReqReceivedByPod, 
    #         ConsumeResourceMem, 
    #         ConsumeResourceCpu, 
    #         ConsumeResource, 
    #         ProcessPersistentRequest, 
    #         # - persistent request 7. Not enough Mem. OomKill anouther pod non overwhelming limits    
    #         ReadDeploymentConfig, 
    #         SchedulerNofityUnboundPod, 
    #         KubectlStartsPod, 
    #         ReqReceivedByLB, 
    #         ReqSentToNodeByLb, 
    #         ReqReceivedByNodeFromLb, 
    #         MarkPodAsOverwhelmingMemLimits, 
    #         MemoryErrorKillPodNotOverwhelmingLimits, 
    #         PodFailsBecauseOfKilling, 
    #         ReqDirectedByKPToNextPodByRRAlg, 
    #         ReqReceivedByPod, 
    #         ConsumeResourceMem, 
    #         ConsumeResourceCpu, 
    #         ConsumeResource, 
    #         ProcessPersistentRequest
    #         ]
    # def solution(self):
    #     return[
    #         ReqToNodeFromLb, 
    #         ]
p = Problem1()

# if p.check_solution(50): print("PLAN CHECK OK")

retCode = p.run()
log.info("fast downward retcode {0}".format(retCode))

print("Created plan:")
i=0
for p in p.plan:
    i=i+1
    print(i,":",p)
