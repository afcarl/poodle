from poodle.poodle import * 

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
     
     