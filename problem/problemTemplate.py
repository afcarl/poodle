from action.pydlKubeAction import *  
from object.commonObject import *
from object.addedNumbers10 import *

class ProblemTemplate(KubeBase):
    constSymbol = {}
    pod = []
    node = []
    kubeProxy = []
    loadbalancer = []
    service = []
    request = []
    containerConfig = []
    def actions(self):
        return [
            # ReqToNodeFromLb
            # ReqReceivedByLB, 
            # ReqSentToNodeByLb, 
            # ReqReceivedByNodeFromLb, 
            # ReqLbSwitchedNodeByRoundRobinAlg, 
            # ReqReceivedByPod, 
            # ReqDirectedToPodByKpRrAlg,
            # ReqDirectedByKPToNextPodByRRAlg,
            # RejectRequestBecauseNoPod,
            # ConsumeResourceMem, 
            # ConsumeResourceCpu, 
            # ConsumeResource, 
            # # # RefuseFromPodBecauseCannotConsumeResourceCpu,
            # ProcessTempRequest, 
            # ProcessPersistentRequest, 
            # ReleaseResourceCpu, 
            # ReleaseResourceMem, 
            # ReleasedResources, 
            # FinishRequest, 
            # TerminatePodAfterFinish, 
            # # TerminatePod, 
            # ReadDeploymentConfig, 
            # CreatePodManually, 
            # SchedulerNofityUnboundPod, 
            # KubectlStartsPod, 
            # MarkPodAsOverwhelmingMemLimits, 
            # MarkPodAsNonoverwhelmingMemLimits, 
            # MemoryErrorKillPodOverwhelmingLimits, 
            # MemoryErrorKillPodNotOverwhelmingLimits, 
            # PodFailsBecauseOfKilling, 
            # # PodSucceds, 
            # # KubectlRecoverPod, 
            # PodGarbageCollectedFailedPod, 
            # PodGarbageCollectedSuccededPod, 
            # ExitBrakePointForRequest1,
            # ExitBrakePointForRequest2,
            # ExitBrakePointForRequest3,
            # ExitBrakePointForRequest4,
            # ExitBrakePointForRequest5,
            # ExitBrakePointForRequest6,
            # ExitBrakePointForRequest7,
            # ExitBrakePointForRequest8,
            # ExitBrakePointForRequest9,
            # ExitBrakePointForRequest10,
            # ExitBrakePointForRequest11,
            # ExitBrakePointForRequest12,
            # ExitBrakePointForRequest13,
            # ExitBrakePointForRequest14,
            # ExitBrakePointForRequest15,
            # ExitBrakePointForRequest16,
            # ExitBrakePointForRequest17,
            # ExitBrakePointForRequest20
            ]

    def constFactory(self, statusNameList, objType):
        for statusName in statusNameList:
            self.constSymbol[statusName] = self.addObject(objType(statusName))

    def problem(self):
        self.numberFactory = NumberFactory(500)
        self.prepareNumbers()

        statusList = ["statusReqAtStart",
        "statusReqAtLoadbalancer",
        "statusReqAtKubeproxy",
        "statusReqAtPodInput",
        "statusReqMemResourceConsumed",
        "statusReqCpuResourceConsumed",
        "statusReqResourcesConsumed",
        "statusReqDirectedToPod",
        "statusReqRequestPIDToBeEnded",
        "statusReqCpuResourceReleased",
        "statusReqMemResourceReleased",
        "statusReqResourcesReleased",
        "statusReqRequestTerminated",
        "statusReqRequestFinished",
        "statusPodAtConfig",
        "statusPodReadyToStart",
        "statusPodActive",
        "statusPodPending",
        "statusPodAtManualCreation",
        "statusPodDirectedToNode",
        "statusPodBindedToNode",
        "statusPodRunning",
        "statusPodSucceeded", # may be lost be careful
        "statusNodeOomKilling",
        "statusNodeFailed",
        "statusNodeRunning",
        "statusNodeSucceded",
        "statusNodePending",
        "statusNodeDeleted",
        "statusPodInactive",
        "statusNodeActive",
        "statusNodeInactive",
        "statusReqDirectedToNode",
        "statusReqNodeCapacityOverwhelmed"]
        self.constFactory(statusList, Status)

        stateList = [
        "statePodSucceeded",
        "statePodRunning",
        "statePodActive",
        "statePodInactive",
        "stateRequestActive",
        "stateRequestInactive",
        "stateNodeActive",
        "stateNodeInactive"]
        self.constFactory(stateList, State)

        typeList = ["typeTemporary","typePersistent"]
        self.constFactory(typeList, Type)
        
        modeList = ["modeUsermode","modeIptables"]
        self.constFactory(modeList, Mode)

        self.constSymbol["statusReqAtStart"].sequence =  self.numberFactory.getNumber(1)
        self.constSymbol["statusReqAtLoadbalancer"].sequence =  self.numberFactory.getNumber(2)
        self.constSymbol["statusReqAtKubeproxy"].sequence =  self.numberFactory.getNumber(3)
        self.constSymbol["statusReqDirectedToPod"].sequence =  self.numberFactory.getNumber(4)
        self.constSymbol["statusReqAtPodInput"].sequence =  self.numberFactory.getNumber(5)
        self.constSymbol["statusReqCpuResourceConsumed"].sequence =  self.numberFactory.getNumber(6)
        self.constSymbol["statusReqMemResourceConsumed"].sequence =  self.numberFactory.getNumber(7)
        self.constSymbol["statusReqResourcesConsumed"].sequence =  self.numberFactory.getNumber(8)
        self.constSymbol["statusReqRequestPIDToBeEnded"].sequence =  self.numberFactory.getNumber(9)
        self.constSymbol["statusReqCpuResourceReleased"].sequence =  self.numberFactory.getNumber(10)
        self.constSymbol["statusReqMemResourceReleased"].sequence =  self.numberFactory.getNumber(11)
        self.constSymbol["statusReqResourcesReleased"].sequence =  self.numberFactory.getNumber(12)
        self.constSymbol["statusReqRequestTerminated"].sequence =  self.numberFactory.getNumber(13)
        self.constSymbol["statusReqRequestFinished"].sequence =  self.numberFactory.getNumber(20)