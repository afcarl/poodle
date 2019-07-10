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

class SimpleTestProblem1(Problem):

    def actions(self):
        return [ ConsumePacketSelect, ForwardPacketToInterface, CreateRoute, HopToRoute ]

    def problem(self):
        
        self.ip_factory = self.addObject(IPFactory()) # need IP factory as all new objects would be different
        ip_factory = self.ip_factory
        
        self.packet = self.addObject(Packet())
        packet2 = self.addObject(Packet())
        packet2.is_consumed = True
        self.packet.next = packet2
        self.packet.dst_ipaddr = self.addObject(ip_factory.gen_ip("192.168.3.3"))
        self.host1 = self.addObject(Host())
        interface = self.addObject(Interface(value='eth0'))
        interface.has_ipaddr = self.addObject(ip_factory.gen_ip("192.168.3.1"))
        self.interface_dummyinput = self.addObject(Interface("eth1"))
        self.host1.has_interface.add(interface)
        self.host1.has_interface.add(self.interface_dummyinput)
        self.host2 = Host()
        self.interface2 = self.addObject(Interface(value='eth0'))
        self.interface2.has_ipaddr = self.addObject(ip_factory.gen_ip("192.168.3.2"))
        # self.interface2.has_ipaddr = self.host1
        
        self.interface3 = self.addObject(Interface(value='eth1'))
        self.interface3.has_ipaddr = self.addObject(ip_factory.gen_ip("192.168.3.3"))
        
        self.host2.has_interface.add(self.interface2)
        self.host2.has_interface.add(self.interface3)
        
        interface.adjacent_interface.add(self.interface2)
        self.interface2.adjacent_interface.add(interface)
        
        # host2.has_interface = [interface2, interface3] # TODO
        
        # this does not work! TODO: protect from this happening
        #self.packet.at_interface_input = self.host1.has_interface
        #self.packet.at_interface_output = interface
        self.packet.at_interface_input = self.interface_dummyinput

    def goal(self):
        return self.packet.is_consumed == True

p = SimpleTestProblem1()
retCode = p.run()
log.info("fast downward retcode {0}".format(retCode))



        
