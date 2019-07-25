from poodle.poodle import * 
from action.pydlNetAction import *
from object.networkObject import *

class IPFactory():
    def __init__(self):
        self.ip_addresses = {}
        
    def gen_ip(self, ipaddr_text):
        if ipaddr_text in self.ip_addresses:
            return self.ip_addresses[ipaddr_text]
        else:
            new_ipaddr_object = IPAddr(ipaddr_text)
            self.ip_addresses[ipaddr_text] = new_ipaddr_object
            return new_ipaddr_object

class RouteExistsReturn(PlannedAction):
    cost = 100
    host = Host()
    table = Select(Table in host.has_table)
    route = Select(Route in table.has_route)
    packet = Select(Packet.at_interface_input in host.has_interface)
    
    def effect(self):
        self.packet.is_consumed = True
        
        

class PacketAtOutputReturn(PlannedAction):
    cost = 100
    packet = Packet()
    iface = Interface()
    def selector(self):
        return Select(self.packet.at_interface_output == self.iface)
    def effect(self):
        self.packet.is_consumed = True

class PacketAtOutputReturnInput(PlannedAction):
    cost = 100
    packet = Packet()
    iface = Interface()
    def selector(self):
        return Select(self.packet.at_interface_input == self.iface)
    def effect(self):
        self.packet.is_consumed = True

class NetworkGoal(Problem):
    def goal(self):
        return self.packet.is_consumed == True
        

class SimpleTestProblem1(NetworkGoal):

    def actions(self):
        return [ ConsumePacketSelect, ForwardPacketToInterface, CreateRoute, 
                HopToRoute, 
                # PacketAtOutputReturn,
                # RouteExistsReturn
                ]

    def problem(self):
        self.null_interface = Interface("NULL")
        self.null_table = Table("NULL")
        
        self.ip_factory = self.addObject(IPFactory()) # need IP factory as all new objects would be different
        ip_factory = self.ip_factory
        
        self.packet = self.addObject(Packet("pkt1"))
        packet2 = self.addObject(Packet("pkt2"))
        packet2.is_consumed = True
        self.packet.next = packet2
        self.packet.current_packet = True
        
        self.packet.dst_ipaddr = self.addObject(ip_factory.gen_ip("192.168.3.3"))
        self.host1 = self.addObject(Host())
        self.interface = self.addObject(Interface(value='eth0'))
        self.interface.has_ipaddr = self.addObject(ip_factory.gen_ip("192.168.3.1"))
        self.interface_dummyinput = self.addObject(Interface("eth1"))
        self.host1.has_interface.add(self.interface)
        self.host1.has_interface.add(self.interface_dummyinput)
        self.host2 = Host()
        self.interface2 = self.addObject(Interface(value='eth0'))
        self.interface2.has_ipaddr = self.addObject(ip_factory.gen_ip("192.168.3.2"))
        # self.interface2.has_ipaddr = self.host1
        
        # Now add tables to host1:
        self.t = self.addObject(Table())
        self.host1.has_table.add(self.t)
        
        self.interface3 = self.addObject(Interface(value='eth1'))
        self.interface3.has_ipaddr = self.addObject(ip_factory.gen_ip("192.168.3.3"))
        
        self.host2.has_interface.add(self.interface2)
        self.host2.has_interface.add(self.interface3)
        
        self.interface.adjacent_interface.add(self.interface2)
        self.interface2.adjacent_interface.add(self.interface)
        
        # host2.has_interface = [interface2, interface3] # TODO
        
        # this does not work! TODO: protect from this happening
        #self.packet.at_interface_input = self.host1.has_interface
        # self.packet.at_interface_output = self.interface
        # Imaginary test:
        self.packet.at_interface_input = self.interface_dummyinput
    
    def solution(self):
        # solution and goal must not exist in same definition of class
        # need to have another check for that - TODO
        return [ # TODO: check if the list here is fully included in actions
            # Select(Packet.at_interface_input in self.host1.has_interface),
            CreateRoute,
            HopToRoute,
            ForwardPacketToInterface,
            #Hinted( # hints are required to select the correct match
            #    action=ForwardPacketToInterface, 
            #    hints=(ForwardPacketToInterface.interface2 == self.interface2)
            #),
            ConsumePacketSelect
        ]

p = SimpleTestProblem1()

if p.check_solution(50): print("PLAN CHECK OK")

retCode = p.run()
log.info("fast downward retcode {0}".format(retCode))

print("Created plan:")
i=0
for p in p.plan:
    i=i+1
    print(i,":",p)
