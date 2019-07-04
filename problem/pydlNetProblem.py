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

class Problem1(Problem):

    def actions(self):
        return [ ConsumePacketSelect, ForwardPacketToInterface ]

    def problem(self):
        
        self.ip_factory = IPFactory() # need IP factory as all new objects would be different
        ip_factory = self.ip_factory
        
        self.packet = self.addObject(Packet())
        packet2 = Packet()
        packet2.is_consumed = True
        self.packet.next = packet2
        self.packet.dst_ipaddr = ip_factory.gen_ip("192.168.3.3")
        self.host1 = Host()
        interface = Interface(value='eth0')
        interface.has_ipaddr = ip_factory.gen_ip("192.168.3.1")
        self.host1.has_interface.add(interface)
        self.host2 = Host()
        self.interface2 = Interface(value='eth0')
        self.interface2.has_ipaddr = ip_factory.gen_ip("192.168.3.2")
        # self.interface2.has_ipaddr = self.host1
        
        self.interface3 = Interface(value='eth1')
        self.interface3.has_ipaddr = ip_factory.gen_ip("192.168.3.3")
        
        self.host2.has_interface.add(self.interface2)
        self.host2.has_interface.add(self.interface3)
        
        interface.adjacent_interface.add(self.interface2)
        self.interface2.adjacent_interface.add(interface)
        
        # host2.has_interface = [interface2, interface3] # TODO
        
        # this does not work! TODO: protect from this happening
        #self.packet.at_interface_input = self.host1.has_interface
        self.packet.at_interface_output = interface

    def goal(self):
        return self.packet.is_consumed == True
        
p = Problem1()
p.run("consumePacket")
