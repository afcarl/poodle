import pytest
from poodle import *
from poodle.arithmetic import *
import poodle.problem

class Type(Object): 
    pass

class Status(Object): 
    pass

STATUS_TESTNULL = Status()
STATUS_TEST0 = Status()
STATUS_TEST1 = Status()
STATUS_TEST2 = Status()
STATUS_TEST3 = Status()
STATUS_TEST4 = Status()
STATUS_TEST5 = Status()
STATUS_TEST6 = Status()
STATUS_TEST7 = Status()
STATUS_TEST8 = Status()
STATUS_TEST9 = Status()
STATUS_TEST10 = Status()
TYPE_NULL = Type()
TYPE_NOTNULL = Type()

class Node(Object):
    cpuCapacity: int
    memCapacity: int
    status: Status
    currentFormalCpuConsumption: int
    currentFormalMemConsumption: int
    currentRealMemConsumption: int
    currentRealCpuConsumption: int
    AmountOfPodsOverwhelmingMemLimits: int
    podAmount: int


class Pod(Object):
    podId: int
    realInitialMemConsumption: int
    realInitialCpuConsumption: int
    currentRealCpuConsumption: int
    currentRealMemConsumption: int
    atNode: Node
    toNode: Node
    status: Status
    bindedToNode: Node
    memLimit: int
    memLimitsStatus: Status
    cpuLimit: int
    cpuLimitsStatus: Status
    memRequest: int
    cpuRequest: int
    amountOfActiveRequests: int
    counterOfNodesPassed: int
    targetService: "Service"

class Scheduler(Object):
    queueLength: int
    # active = Bool
    status: Status
Scheduler.podQueue = Relation(Pod)

class GlobalVar(Object):
    numberOfRejectedReq: int
    currentFormalCpuConsumption: int
    currentFormalMemConsumption: int
    memCapacity: int
    currentRealMemConsumption: int
    currentRealCpuConsumption: int
    issue: Type
    lastNodeUsedByRRalg: Node
    lastNodeUsedByPodRRalg: Node
    amountOfNodes: int
    schedulerStatus: Status
    amountOfPods: int
    queueLength: int

class Service(Object):
    lastPod: Pod
    atNode: Node
    amountOfActivePods: int
    status: Status
    
    
class ProblemExample(poodle.problem.Problem):    
    @planned
    def TestForNoSum(self, 
        pod1: Pod,
        nullNode: Node,
        anyNode: Node):
        assert pod1.toNode == nullNode
        pod1.toNode = anyNode
        pod1.status = STATUS_TEST0
    
    def problem(self):
        self.service1 = self.addObject(Service('service1'))
        self.service1.amountOfActivePods = 0
       
       
        self.nodeNull = self.addObject(Node('Null'))
        self.nodeNull.type =  TYPE_NULL

        
        self.node1 = self.addObject(Node('node1'))
        self.node1.cpuCapacity = 3
        self.node1.memCapacity = 3
        self.node1.currentFormalCpuConsumption = 2
        self.node1.currentFormalMemConsumption = 2
        self.node1.currentRealMemConsumption =0
        self.node1.currentRealCpuConsumption =0
        self.node1.AmountOfPodsOverwhelmingMemLimits =0
        self.node1.type =  TYPE_NOTNULL


        self.node2 = self.addObject(Node('node2'))
        self.node2.cpuCapacity = 3
        self.node2.memCapacity = 3
        self.node2.memCapacityBarier = 4
        self.node2.currentFormalCpuConsumption = 2
        self.node2.currentFormalMemConsumption = 2
        self.node2.currentRealMemConsumption =0
        self.node2.currentRealCpuConsumption =0
        self.node2.AmountOfPodsOverwhelmingMemLimits =0
        self.node2.type =  TYPE_NOTNULL

        self.pod1 = self.addObject(Pod('pod1'))
        self.pod1.currentRealCpuConsumption =0
        self.pod1.currentRealMemConsumption =0
        self.pod1.status = STATUS_TESTNULL
        self.pod1.memRequest = 1
        self.pod1.cpuRequest = 1
        self.pod1.podNotOverwhelmingLimits = True
        self.pod1.realInitialMemConsumption =0
        self.pod1.realInitialCpuConsumption =0
        self.pod1.memLimit =  1
        self.pod1.cpuLimit =  1
        self.pod1.atNode = self.node2
        self.pod1.toNode = self.nodeNull
        self.pod1.amountOfActiveRequests =0
        self.pod1.targetService = self.service1
        
        
        self.pod2 = self.addObject(Pod('pod2'))
        self.pod2.currentRealCpuConsumption =0
        self.pod2.currentRealMemConsumption =0
        self.pod2.status = STATUS_TESTNULL
        self.pod2.memRequest = 1
        self.pod2.cpuRequest = 1
        self.pod2.realInitialMemConsumption =0
        self.pod2.realInitialCpuConsumption =0        
        self.pod2.memLimit =  1
        self.pod2.cpuLimit =  1
        self.pod2.atNode = self.node2   
        self.pod2.toNode = self.nodeNull
        self.pod2.amountOfActiveRequests =0

        self.globalVar1 = self.addObject(GlobalVar())
        self.globalVar1.numberOfRejectedReq =0
        self.globalVar1.lastPod = self.pod1
        self.globalVar1.memCapacity = 6
        self.globalVar1.currentFormalCpuConsumption  = 4
        self.globalVar1.currentFormalMemConsumption  = 4
        self.globalVar1.queueLength =0
        self.globalVar1.amountOfPods = 5
          
        self.scheduler1 = self.addObject(Scheduler('scheduler1'))
        self.scheduler1.podQueue.add(self.pod1)
        self.scheduler1.podQueue.add(self.pod2)
        self.scheduler1.queueLength = 2

    @planned
    def TestOfOneSum(self, 
        podStarted: Pod,
        node1: Node,
        scheduler1: Scheduler,
        serviceTargetForPod: Service,
        globalVar1: GlobalVar
        ):
        assert podStarted.targetService == serviceTargetForPod
        node1.currentFormalCpuConsumption += podStarted.cpuRequest
        podStarted.atNode = node1        
        podStarted.status = STATUS_TEST1
        
    @planned
    def TestOfTwoSums(self, 
        podStarted: Pod,
        node1: Node,
        scheduler1: Scheduler,
        serviceTargetForPod: Service,
        globalVar1: GlobalVar
        ):

        assert podStarted.targetService == serviceTargetForPod
        node1.currentFormalCpuConsumption += podStarted.cpuRequest
        node1.currentFormalMemConsumption += podStarted.memRequest
        podStarted.atNode = node1        
        podStarted.status = STATUS_TEST2

    @planned
    def TestOfThreeSums(self, 
        podStarted: Pod,
        node1: Node,
        scheduler1: Scheduler,
        serviceTargetForPod: Service,
        globalVar1: GlobalVar
        ):

        assert podStarted.targetService == serviceTargetForPod
        node1.currentFormalCpuConsumption += podStarted.cpuRequest
        node1.currentFormalMemConsumption += podStarted.memRequest
        globalVar1.currentFormalCpuConsumption += podStarted.cpuRequest
        podStarted.atNode = node1        
        podStarted.status = STATUS_TEST3

class Problem4(ProblemExample):
    @planned
    def TestOfFourSums(self, 
        podStarted: Pod,
        node1: Node,
        scheduler1: Scheduler,
        serviceTargetForPod: Service,
        globalVar1: GlobalVar
        ):

        assert podStarted.targetService == serviceTargetForPod
        node1.currentFormalCpuConsumption += podStarted.cpuRequest
        node1.currentFormalMemConsumption += podStarted.memRequest
        globalVar1.currentFormalCpuConsumption += podStarted.cpuRequest
        globalVar1.currentFormalMemConsumption += podStarted.memRequest

        podStarted.atNode = node1        
        podStarted.status = STATUS_TEST4

class Problem5(ProblemExample):
    @planned
    def TestOfFiveSums(self, 
        podStarted: Pod,
        node1: Node,
        scheduler1: Scheduler,
        serviceTargetForPod: Service,
        globalVar1: GlobalVar
        ):

        assert podStarted.targetService == serviceTargetForPod
        node1.currentFormalCpuConsumption += podStarted.cpuRequest
        node1.currentFormalMemConsumption += podStarted.memRequest
        globalVar1.currentFormalCpuConsumption += podStarted.cpuRequest
        globalVar1.currentFormalMemConsumption += podStarted.memRequest
        serviceTargetForPod.amountOfActivePods += 1

        podStarted.atNode = node1        
        podStarted.status = STATUS_TEST5

class Problem6(ProblemExample):

    @planned
    def TestOfSixSums(self, 
        podStarted: Pod,
        node1: Node,
        scheduler1: Scheduler,
        serviceTargetForPod: Service,
        globalVar1: GlobalVar
        ):

        assert podStarted.targetService == serviceTargetForPod
        node1.currentFormalCpuConsumption += podStarted.cpuRequest
        node1.currentFormalMemConsumption += podStarted.memRequest
        globalVar1.currentFormalCpuConsumption += podStarted.cpuRequest
        globalVar1.currentFormalMemConsumption += podStarted.memRequest
        serviceTargetForPod.amountOfActivePods += 1
        scheduler1.queueLength -= 1

        podStarted.atNode = node1        
        podStarted.status = STATUS_TEST6


class Problem7(ProblemExample):

    @planned
    def TestOf7Sums(self, 
        podStarted: Pod,
        node1: Node,
        scheduler1: Scheduler,
        serviceTargetForPod: Service,
        globalVar1: GlobalVar
        ):

        assert podStarted.targetService == serviceTargetForPod
        node1.currentFormalCpuConsumption += podStarted.cpuRequest
        node1.currentFormalMemConsumption += podStarted.memRequest
        globalVar1.currentFormalCpuConsumption += podStarted.cpuRequest
        globalVar1.currentFormalMemConsumption += podStarted.memRequest
        serviceTargetForPod.amountOfActivePods += 1
        podStarted.cpuRequest += 1
        

        scheduler1.queueLength -= 1

        podStarted.atNode = node1        
        podStarted.status = STATUS_TEST7

class Problem8(ProblemExample):
    @planned
    def TestOf8Sums(self, 
        podStarted: Pod,
        node1: Node,
        scheduler1: Scheduler,
        serviceTargetForPod: Service,
        globalVar1: GlobalVar
        ):

        assert podStarted.targetService == serviceTargetForPod
        node1.currentFormalCpuConsumption += podStarted.cpuRequest
        node1.currentFormalMemConsumption += podStarted.memRequest
        globalVar1.currentFormalCpuConsumption += podStarted.cpuRequest
        globalVar1.currentFormalMemConsumption += podStarted.memRequest
        serviceTargetForPod.amountOfActivePods += 1
        podStarted.cpuRequest += 1
        podStarted.memRequest += 1

        scheduler1.queueLength -= 1

        podStarted.atNode = node1        
        podStarted.status = STATUS_TEST8

class Problem9(ProblemExample):
    @planned
    def TestOf9Sums(self, 
        podStarted: Pod,
        node1: Node,
        scheduler1: Scheduler,
        serviceTargetForPod: Service,
        globalVar1: GlobalVar
        ):

        assert podStarted.targetService == serviceTargetForPod
        node1.currentFormalCpuConsumption += podStarted.cpuRequest
        node1.currentFormalMemConsumption += podStarted.memRequest
        globalVar1.currentFormalCpuConsumption += podStarted.cpuRequest
        globalVar1.currentFormalMemConsumption += podStarted.memRequest
        serviceTargetForPod.amountOfActivePods += 1
        podStarted.cpuRequest += 1
        podStarted.memRequest += 1
        node1.currentFormalCpuConsumption += 1
        scheduler1.queueLength -= 1

        podStarted.atNode = node1        
        podStarted.status = STATUS_TEST9

class Problem10(ProblemExample):
    @planned
    def TestOf10Sums(self, 
        podStarted: Pod,
        node1: Node,
        scheduler1: Scheduler,
        serviceTargetForPod: Service,
        globalVar1: GlobalVar
        ):

        assert podStarted.targetService == serviceTargetForPod
        node1.currentFormalCpuConsumption += podStarted.cpuRequest
        node1.currentFormalMemConsumption += podStarted.memRequest
        globalVar1.currentFormalCpuConsumption += podStarted.cpuRequest
        globalVar1.currentFormalMemConsumption += podStarted.memRequest
        serviceTargetForPod.amountOfActivePods += 1
        podStarted.cpuRequest += 1
        podStarted.memRequest += 1
        node1.currentFormalCpuConsumption += 1
        scheduler1.queueLength -= 1
        node1.currentFormalMemConsumption += 1

        podStarted.atNode = node1        
        podStarted.status = STATUS_TEST10
          
class Goal1(ProblemExample):
    def goal(self):
        return self.pod1.status == STATUS_TEST1

def test_math_split1():
    p = Goal1()
    p.run()
    for a in p.plan: a
    
class Goal2(ProblemExample):
    def goal(self):
        return self.pod1.status == STATUS_TEST2

def test_math_split2():
    p = Goal2()
    p.run()
    for a in p.plan: a
    
class Goal3(ProblemExample):
    def goal(self):
        return self.pod1.status == STATUS_TEST3

def test_math_split3():
    p = Goal3()
    p.run()
    for a in p.plan: a

class Goal4(Problem4):
    def goal(self):
        return self.pod1.status == STATUS_TEST4

def test_math_split4():
    p = Goal4()
    p.run()
    for a in p.plan: a

class Goal5(Problem5):
    def goal(self):
        return self.pod1.status == STATUS_TEST5

def test_math_split5():
    p = Goal5()
    p.run()
    for a in p.plan: a
    
class Goal6(Problem6):
    def goal(self):
        return self.pod1.status == STATUS_TEST6

def test_math_split6():
    p = Goal6()
    p.run()
    for a in p.plan: a
    
def test_math_split7():
    p = Goal7()
    p.run()
    for a in p.plan: a

class Goal7(Problem7):
    def goal(self):
        return self.pod1.status == STATUS_TEST7

@pytest.mark.skip(reason="Does not pass - TODO FIXME")
def test_math_split8():
    p = Goal8()
    p.run()
    for a in p.plan: a

class Goal8(Problem8):
    def goal(self):
        return self.pod1.status == STATUS_TEST8

@pytest.mark.skip(reason="TODO: Does not pass - too slow")
def test_math_split9():
    p = Goal9()
    p.run()
    for a in p.plan: a

class Goal9(Problem9):
    def goal(self):
        return self.pod1.status == STATUS_TEST9

class Goal10(Problem10):
    def goal(self):
        return self.pod1.status == STATUS_TEST10

@pytest.mark.skip(reason="TODO: Does not pass - too slow")
def test_math_split10():
    p = Goal10()
    p.run()
    for a in p.plan: a
