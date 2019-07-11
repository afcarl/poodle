from poodle.poodle import *
from object.networkObject import *

class ConsumePacket(PlannedAction):
    cost = 1
    template="template/ConsumePacketSelectTest.j2"
    
    interface1 = Interface()
    # current_host = Host.has_interface.contains(interface1)
    # current_host = Host.has_interface // interface1
    current_host = interface1 |IN| Host.has_interface
    
    # packet = current_host.has_interface |EQ| Packet.at_interface_input \
    packet = Packet.at_interface_input |EQ| current_host.has_interface \
            #   or current_host.has_interface |IN| Packet.at_interface_output
    # (Packet-at_interface_input ?Packet-6 ?Interface-3)
    # (Host-has_interface ?Host-4 ?Interface-3)
    interface_any = Interface |IN| current_host.has_interface
    packet_next = packet.next |EQ| Packet 
    
    # packet_next = Packet |EQ| packet.next # TODO: implement other-way-around???
    # packet_next = packet.next |EQ| Packet 
    # TODO: implement reverse order EQ!!
    # host_more = Host.has_interface |EQ| packet_next.at_interface_input
    # host_more =  packet_next.at_interface_input |EQ| Host.has_interface
    # (Host-has_interface ?host-1 ?interface-1)
    # (Packet-at_interface_input ?packet-1 ?interface-1)
    # packet2 = packet.related_to |IN| Host.has_interface
    
    def selector(self):
        return self.packet.dst_ipaddr |EQ| self.interface_any.has_ipaddr \
                and self.interface1.has_ipaddr |EQ| self.packet.dst_ipaddr
    
    def effect(self):
        self.packet_next.current_packet.set() # = True
        # self.packet.next.current_packet.set() # = True # TODO: support for dot-dot
        # (Packet-current_packet )
        self.packet.is_consumed.set() # = False
        self.packet.current_packet.unset()

#print('"'+ConsumePacket.compile(None).strip()+'"')

class ConsumePacketSelectInv(PlannedAction):
    cost = 1
    
    interface1 = Interface()
    current_host = Select( interface1 in Host.has_interface )
    packet = Select( current_host.has_interface == Packet.at_interface_input )
            #   or current_host.has_interface in Packet.at_interface_output
            # TODO: protect against using 'or' operator by checking _selector for emptiness
            # alternatively, we can detect all ORs this way: returning False
            # and checking if there was previous result.
            # we can then stack up all OR'ed and generate separate actions
    interface_any = Select( Interface in current_host.has_interface )
    packet_next = Select( Packet == packet.next )
    
    def selector(self):
        # TODO: when implementing and/or protection - compilation mode should switch to return True
        return Select(self.packet.dst_ipaddr == self.interface_any.has_ipaddr \
                and self.interface1.has_ipaddr == self.packet.dst_ipaddr)
    
    def effect(self):
        self.packet_next.current_packet.set() # = True
        # self.packet.next.current_packet.set() # = True # TODO: support for dot-dot
        # (Packet-current_packet )
        self.packet.is_consumed.set() # = False
        self.packet.current_packet.unset()

#print('"'+ConsumePacketSelectInv.compile(None).strip()+'"')

class ConsumePacketSelect(PlannedAction):
    cost = 1
    
    interface1 = Interface()
    current_host = Select( interface1 in Host.has_interface )
    packet = Select( Packet.at_interface_input == current_host.has_interface )
            #   or current_host.has_interface in Packet.at_interface_output
            # TODO: protect against using 'or' operator by checking _selector for emptiness
            # alternatively, we can detect all ORs this way: returning False
            # and checking if there was previous result.
            # we can then stack up all OR'ed and generate separate actions
    interface_any = Select( Interface in current_host.has_interface )
    packet_next = Select( packet.next == Packet )
    
    def selector(self):
        # TODO: when implementing and/or protection - compilation mode should switch to return True
        return Select(self.packet.dst_ipaddr == self.interface_any.has_ipaddr)
                # and self.interface1.has_ipaddr == self.packet.dst_ipaddr) # incorrect, add to unit test
    
    def effect(self):
        self.packet_next.current_packet.set() # = True
        # self.packet.next.current_packet.set() # = True # TODO: support for dot-dot
        # (Packet-current_packet )
        self.packet.is_consumed.set() # = False
        self.packet.current_packet.unset()

#print('"'+ConsumePacketSelect.compile().strip()+'"')

class ForwardPacketToInterface(PlannedAction):

    template="template/ConsumePacketSelectTest.j2"

    interface1 = Interface()
    interface2 = Select( interface1.adjacent_interface == Interface )
    packet = Packet() # any packet
    
    def selector(self):
        return self.packet.at_interface_output |EQ| self.interface1
        
    def effect(self):
        # TODO: we can auto-detect what to unset in property
        #       as property can only have one variable
        #       just select the variable first of the class that has the variable
        self.packet.at_interface_output.unset(self.interface1)
        # this also works but experimentally:
        # self.packet.at_interface_output.unset()
        # TODO: set() could automatically issue an unset()
        self.packet.at_interface_input.set(self.interface2)

#print(ForwardPacketToInterface.compile(None))
        
class ForwardPacketInSwitch(PlannedAction):

    switch = Host()
    
    #switch = Host |IN| Host.isSwitch
    interface_from = Interface |IN| switch.has_interface
    interface_to = Interface |IN| switch.has_interface

    packet = Packet()

    state = RequestState |IN| packet.protocol_state

    def selector(self):
        Select(self.interface_from == self.packet.at_interface_input \
        and self.interface_from != self.interface_to)

    def effect(self):
        self.packet.at_interface_input.unset(self.interface_from)

# print(ForwardPacketInSwitch.compile())

#    (:action forward-packet-in-switch
#        :parameters (?packet - packet ?switch - host ?interface-from - interface ?interface-to - interface ?state - state)
#        :precondition (and
#                          ;(current-packet ?packet) #KB - this predicate increases search time for 7001 case for 1 second
#                            (is-switch ?switch)
#                            (has-interface ?switch ?interface-from)
#                            (has-interface ?switch ?interface-to)
#                            (packet-protocol-state ?packet ?state)
#                            (at-interface-input ?packet ?interface-from)
#                            (not (= ?interface-from ?interface-to))
#        )
#        :effect (and
#                    (at-interface-output ?packet ?interface-to)
#                    (not(at-interface-input ?packet ?interface-from))
#                    (increase (total-cost) 1)
#        )
#    )

class ForwardPacketToRouteInTable(PlannedAction):
    host = Host()
    table = Select(Table in host.has_table) # Table is imaginary?
    packet = Select(Packet.at_table == table)
    route = Select(Route in table.has_route) # Route is also imaginary
    route_dot_network = Select(Network == route.network) # TODO: need just a dereference...
    # Need static function: net_match(packet.dst_ipaddr, route.network))
    print("VAR 1 ------------------------------------")
    interface_dest = Select(Interface.has_ipaddr == route.gw_ipaddr)
    #interface_dest = Select(Interface.has_ipaddr == route.gw_ipaddr)
    #packet         = Select(Packet.at_interface_input in host.has_interface)

    # TODO: not exists narrower...
    # net_narrower = Select(route_dot_network in Network.narrower_than)
    # route_narrower = Select(net_narrower == Route.network)
                # and NotExists(packet.dst_ipaddr in net_narrower.match_ip and 
                #                  route_narrower in table.routes )

    interface = Select(Interface == route.interface) # TODO: remove when dot-prop effect is supported
                        # https://trello.com/c/VhWF5MtJ/69-support-for-setting-of-dot-prop-in-effect
    

    def selector(self):
        return Select(\
                self.route.interface in self.interface_dest.adjacent_interface and \
                self.packet.dst_ipaddr in self.route_dot_network.match_ip) 
                                                # dst matches the net of this route
                # TODO: fill in all the static matches to match_ip
                # 

    def effect(self):
        # self.packet.at_table = None # TODO not supported yet
        self.packet.at_table.unset(self.table)
        # self.packet.at_interface_output = self.route.interface # TODO support this
        self.packet.at_interface_output = self.interface # TODO remove when above is supported
        self.packet.dst_macaddr = self.interface_dest

print(ForwardPacketToRouteInTable.compile(Problem()))

class TestImaginaryCreate(PlannedAction):
    host = Host()
    packet = Packet()
    interface = Select(Interface in host.has_interface)

    def selector(self):
        return Select(self.packet.at_interface_input in self.host.has_interface)

    def effect(self):
        table = Table()
        # to create object:
        # predicates:
        # generate new variables for new objects, store smwhr
        # (not (table-hashnum-exists ?num1 ?num2) ; hashnums
        #    add this to predicate templates
        # (hashnum ?num1)
        #    add to predicates templates
        #    generate this
        # (hashnum ?num2) ; for all created - need these!!
        # effects:
        # (table-hashnum-exists ?num1 ?num2)
        # (table-has-route ?num1 ?num2 ?num3 ?num4)
        route = Route()
        table.has_route.add(route)
        route.interface = self.interface
        self.problem.addObject(table)

print(TestImaginaryCreate.compile(Problem()))

class TestStaticObject(PlannedAction):
    host = Host()
    interface = Select(Interface in host.has_interface)
    packet = Select(Packet.at_interface_input == interface)

    def selector(self):
        return Select(self.packet.at_interface_input in self.host.has_interface \
        and self.packet.at_interface_input == self.problem.testif)

    def effect(self):
        self.packet.at_interface_input = self.problem.testif

class StaticObjectProblem(Problem):
    def actions(self):
        return [ TestStaticObject ]
    def problem(self):
        self.testif = self.addObject(Interface("test0"))
        self.ipaddr = IPAddr("192.168.1.1")
    def goal(self):
        return self.testif.has_ipaddr == self.ipaddr

p = StaticObjectProblem()
p.run()
print(p.compile_domain())
#p.compile_problem()
#p.compile_domain()


class HopToRoute(PlannedAction):
    "Relay the packet to route in the host"
    host = Host()
    packet = Select(Packet.at_interface_input in host.has_interface)
    # TODO HERE:
    # 1. make sure we return Packet object
    # 2. selector that we do is two-fold:
    #    2.1 
    # 3. class variable on returning object must be from Packet 
    print("PREDICATE1 ------------------------")
    table = Select(Table in host.has_table)
    print("PREDICATE2 ------------------------")
    route = Select(Route in table.has_route)
    route_dot_interface = Select(Interface == route.interface)

    def selector(self):
        return True

    def effect(self):
        self.packet.at_interface_input.unset()
        self.packet.at_interface_output = self.route_dot_interface
        
print(HopToRoute.compile(Problem()))
# raise AssertionError("TEST")

class CreateRoute(PlannedAction):
    host = Host()
    packet = Select(Packet.at_interface_input in host.has_interface)
    table = Select(Table in host.has_table)
    interface = Select(Interface in host.has_interface)

    def selector(self):
        return True

    def effect(self):
        r = Route()
        r.interface = self.interface
        self.table.has_route.add(r)
        self.problem.addObject(r)

class Cando():
    pass

class Model1(Cando):
    def __init__(self):
        self.actionModel = [
                Packet.at_interface_input == Host.has_interface,
                CreateRoute,
                HopToRoute,
                ForwardPacketToInterface,
                ConsumePacket
        ]


    
