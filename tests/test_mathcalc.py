import pytest
from poodle import *
from poodle.arithmetic import *
import poodle.problem
from typing import Set

class Type(Object): 
    pass

class Status(Object): 
    pass

STATUS_UP = Status()
STATUS_DOWN = Status()

TYPE_NULL = Type()
TYPE_NOTNULL = Type()

class Node(Object):
    capacity: int
    freeCapacity: int
    containersCount: int
    pods: Set["Pod"]
    type: Type
    
class NodeList(Object):
    totalCapacity: int
    totalfreeCapacity: int

class PodList(Object):
    pendingPods: Set["Pod"]
    pendingPodsCounter: int
    allocatedPods: Set["Pod"]
    allocatedPodsCounter: int    

class Pod(Object):
    size: int
    atNode: Node


class Problem(poodle.problem.Problem):    
    @planned
    def PutPodToNode(self, 
        pod1: Pod,
        node1: Node,
        podList1: PodList,
        nodeList1: NodeList):
        assert pod1 in  podList1.pendingPods
        assert node1.freeCapacity > pod1.size - 1
        assert node1.type == TYPE_NOTNULL
        node1.freeCapacity -= pod1.size
        nodeList1.totalfreeCapacity -= pod1.size
        podList1.pendingPods.remove(pod1)
        podList1.allocatedPods.add(pod1)
        node1.pods.add(pod1)
        podList1.pendingPodsCounter -= 1
        podList1.allocatedPodsCounter += 1
        pod1.atNode = node1
        node1.containersCount += 1
    
    
    @planned(cost=1000)
    def SpareNodeCapacity(self, 
        nodeList1: NodeList):
        nodeList1.totalfreeCapacity -= 1

    @planned(cost=1000)
    def SpareTotalNodeCapacity(self, 
        nodeList1: NodeList,
        node1: Node):
        assert node1.freeCapacity == node1.capacity
        nodeList1.totalfreeCapacity -= node1.capacity

    
    @planned(cost=1000)
    def SparePod(self, 
        podList1: PodList,
        pod1: Pod):
        assert pod1 in podList1.pendingPods
        podList1.pendingPods.remove(pod1)
        podList1.pendingPodsCounter -= 1
        

    def problem(self):
        self.nullNode = self.addObject(Node('nodeNull'))
        self.nullNode.type = TYPE_NULL
        
        self.podList1 = self.addObject(PodList('podList1'))
        self.podList1.pendingPodsCounter = 0
        self.podList1.allocatedPodsCounter = 0
        
        self.nodeList1 = self.addObject(NodeList("nodeList1"))
        self.nodeList1.totalfreeCapacity = 0
        self.nodeList1.totalCapacity = 0
        
        amountOfpodsSize= [[1,5],[2,5]] # [size,amount]
        amountOfnodesSize= [[5,1],[2,5]] # [size,amount]
        
        pendingPodsCounterLoc = 0
        
        for row  in amountOfpodsSize:
            for i in range(row[1]):
                pod = self.addObject(Pod(f"pod{i}"))
                pod.size = row[0]
                pod.atNode = self.nullNode
                self.podList1.pendingPods.add(pod)
                pendingPodsCounterLoc += 1
        
        self.podList1.pendingPodsCounter = pendingPodsCounterLoc

        totalfreeCapacityLoc = 0
        totalCapacityLoc= 0
        
        for row  in amountOfnodesSize:
            for i in range(row[1]):
                node = self.addObject(Node(f"node{i}"))
                node.capacity = row[0]
                node.freeCapacity = row[0]
                totalfreeCapacityLoc += row[0]
                totalCapacityLoc += row[0]
                node.type = TYPE_NOTNULL
                node.containersCount = 0

        self.nodeList1.totalfreeCapacity = totalfreeCapacityLoc
        self.nodeList1.totalCapacity = totalCapacityLoc

class Goal1(Problem):
    def goal(self):
        return self.nodeList1.totalfreeCapacity == 0 and self.podList1.pendingPodsCounter == 0

def test_math_split1():
    p = Goal1()
    p.run()
    for a in p.plan: a
    
