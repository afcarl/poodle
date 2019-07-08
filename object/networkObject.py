from poodle.poodle import *
from object.commonObject import *

class RequestState(StaticObject):
    static_values = ["request", "reply"]

class Network(Object):
    is_default = StateFact()
    def gen_name(self, name):
        return super(Network, self).gen_name("NET-"+name)
Network.is_narrower_than = Relation(Network)
# TODO: define default behaviour with "default" net narrower-than

class IPAddr(Object): # -> ipaddr - object; ip-192.179.4.34 - ipaddr
    net_match = Relation(Network) # -> (net-match [self] ?net - network)
    
    def gen_name(self, name):
        return super(IPAddr, self).gen_name("IP-"+name)


class Table(Object):
    # TODO: PredefinedObject? - initialize objects statically?
    
    has_route_to = Relation(Network) # TODO : this is heuristic relation!!! 
    pass

class Port(Object):
    is_any_port = StateFact()
    
class Socket(Object):
    has_port = Property(Port)


class Interface(Object):
    has_ipaddr = Property(IPAddr)
    has_net = Property(Network)
    
    internet_connected = StateFact()

#    def __str__(self):
#        return str(self.value)
# Interface.adjacent_interface = BidirectionalRelation(Interface) # TODO: not with self?
Interface.adjacent_interface = Relation(Interface) # TODO: not with self?

class Host_P(Object): # TODO REMOVE!!!!!!
    pass

class Host(Host_P):
    has_table = Relation(Table) # -> (has-table [self] ?table - table) [x many] (table in Host.has_table) 
    has_interface = Relation(Interface)
    socket = Relation(Socket)
    isSwitch = StateFact()

    # heuristic relations!!
    # TODO: unique property constraint? -->>>
    # "this action should be unique (key) by this set of properties"
    #   -- note for every action there is different key
    has_host_rule_to = Property(IPAddr) # -> ()
    #            Property may be just a single object, or a collection of objects (positioned or named)
    has_host_rule_to_fwmark_sport = Property(ipto=IPAddr, sport=Port)
    has_host_rule_to_fwmark_dport = Property(ipto=IPAddr, dport=Port)
    has_host_rule_to_fwmark_sport_dport = Property(ipto=IPAddr, sport=Port, dport=Port)


# Imaginary objects are identified by the predicate itself, 
# or by combination of identified_by properties with any of its properties
class Route(Imaginary): # there is no "self" in imaginary route, currently it is "has_route" predicate
    # Identity
    # TODO: complex identification?? Number4Bit as identified_by
    identified_by = Property(host=Host, table=Table, number=Number)

    # Properties 
    network = Property(Network) # -> (route-id ?host ?table ?number )
    ipaddr = Property(IPAddr)
    target_ipaddr = Property(IPAddr)
    interface = Property(Interface)
    
    # Relations
Route.is_higher_metric_than = Relation(Route) # TODO: complex relation??
    

class RuleTo(Imaginary):
    identified_by = [Host, Number]
    
    rule_to = Property(IPAddr) # dst ipaddr..
    table = Relation(Table) # TODO: this must "drag" link to Host
    # TODO: host-has-rule-to # identified_by?? or exist_check??
    #       this is actually used as heuristic - to deny adding more same rules
    #       probably need to add this as a heuristic pattern, may be automatically
    
    # TODO: we moved relation higher-than to Number object!
    # TODO: check if there is a way to express higher-than for rules?

# TODO: express: every host has only one rule to destination X???
#       this should probably happen at action side! so that action can not fire
#       with this costraint in place!

class SPortRule(RuleTo):
    rule_to = Property(ipaddr=IPAddr, port=Port)
class DPortRule(RuleTo):
    rule_to = Property(ipaddr=IPAddr, port=Port)
class SPortDPortRule(RuleTo):
    rule_to = Property(ipaddr=IPAddr, src_port=Port, dst_port=Port)

class ProtectedProperty(Property):
    def _check(self):
        global _problem_compilation
        global _compilation
        assert _problem_compilation, "Property %s is protected!" % self
        assert not _compilation, "Property %s is protected!" % self
    def set(self, what):
        self._check()
        super().set(what)
    def unset(self, what):
        self._check()
        super().unset(what)

class Packet(Object):
    
    is_consumed = StateFact()
    protocol_state = Relation(RequestState)
    
    current_packet = StateFact()

    
    packet_has_dst_ip = StateFact() # Do not know why we need this
    packet_has_src_ip = StateFact()
    
    dst_ipaddr = Property(IPAddr)
    src_ipaddr = Property(IPAddr)
    has_src_port = Property(Port)
    has_dst_port = Property(Port)
    
    socket_from = ProtectedProperty(Socket)
    socket_to = ProtectedProperty(Socket)
    
    # validation_packet_recv = RelationRecv(Packet) # checking relation receipt
    
    seen_at = Relation(host=Host, state=RequestState)
    seen_at_eth = Relation(iface=Interface, state=RequestState)
    
    origin = ProtectedProperty(Host)
    
    at_table = StateRelation(Table)
    at_host = StateRelation(Host) # TODO: this should be derived predicate!
    at_interface_input = StateProperty(Interface)
    at_interface_output = StateProperty(Interface)
    # can also be manually derived (as it is now manually written in PDDL)
    related_to = Relation(Interface) # TODO: REMOVE!!
Packet.next = Property(Packet) # next packet in chain
Packet.validation_packet = Property(Packet)



class ConntrackState(Imaginary):
    #                        src     dst     src   dst
    # identified_by = [ Host, IPAddr, IPAddr, Port, Port, Interface ]
    # strings mean properties from the list below
    identified_by = [ "host", "src", "dst", "src_port", "dst_port", "interface" ] 
    identified_by = Property(host=Host, src=IPAddr, dst=IPAddr, src_port=Port, dst_port=Port, intnerface=Interface)
    # host = Property(Host)
    # src = Property(IPAddr)
    # dst = Property(IPAddr)
    # src_port = Property(Port)
    # dst_port = Property(Port)
    # interface = Property(Interface)
    