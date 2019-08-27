import unittest
import pytest

from poodle import *

from object.networkObject import *
from object.commonObject import *
from poodle.problem import Problem

# class ConsumePacketSelect(PlannedAction):
#     cost = 1
    
#     interface1 = Interface()
#     current_host = Select( interface1 in Host.has_interface )
#     packet = Select( Packet.at_interface_input == current_host.has_interface )
#             #   or current_host.has_interface in Packet.at_interface_output
#             # TODO: protect against using 'or' operator by checking _selector for emptiness
#             # alternatively, we can detect all ORs this way: returning False
#             # and checking if there was previous result.
#             # we can then stack up all OR'ed and generate separate actions
#     interface_any = Select( Interface in current_host.has_interface )
#     packet_next = Select( packet.next == Packet )
    
#     def selector(self):
#         # TODO: when implementing and/or protection - compilation mode should switch to return True
#         return Select(self.packet.dst_ipaddr == self.interface_any.has_ipaddr \
#                 and self.interface1.has_ipaddr == self.packet.dst_ipaddr)
    
#     def effect(self):
#         self.packet_next.current_packet.set() # = True
#         # self.packet.next.current_packet.set() # = True # TODO: support for dot-dot
#         # (Packet-current_packet )
#         self.packet.is_consumed.set() # = False
#         self.packet.current_packet.unset()

# class StumbProblem(Problem):
#     def actions(self):
#         return [ ConsumePacketSelect]
#     def problem(self):
#         self.o1 = Object()
#         self.o2 = Object()
#         pass
#     def goal(self):
#         return self.o1 == self.o2


@pytest.mark.skip(reason="incompatible with poodle3")
class TestEffectGenPredicate(unittest.TestCase):
    #bug #35 https://trello.com/c/cTbR2PEe/35-effect-dont-declare-predicates-for-declaration-collection
    def test_effectGenPredicate(self):
        p = StumbProblem()
        p.compile_problem()
        p.compile_domain()
        lines = p.get_predicates()
        #Packet-is_consumed ?var1 - Packet
        self.assertTrue(lines.find('(Packet-is_consumed ?var1 - Packet)') != -1)

@pytest.mark.skip(reason="incompatible with poodle3")
def test_booleffect():
    class Stub(Object):
        pass

    stobj = Stub()

    class Scheduler(Object):
        queueLength = Property(Stub)
        active = Bool(False)
    
    class T(Problem):
        @planned
        def ScheduleQueueProcessed(self,
                scheduler1: Scheduler):
            assert  scheduler1.queueLength == stobj
            scheduler1.active = True
        def problem(self):
            self.o1 = Object()
            self.o2 = Object()
            pass
        def goal(self):
            return self.o1 == self.o2
    t=T()
    # print(t.compile_domain())
    t.compile_problem()
    assert "(Scheduler-active " in \
         t.compile_domain().split("ScheduleQueueProcessed")[1]

    
@pytest.mark.skip(reason="incompatible with poodle3")
def test_full_schedule():
    class Stub(Object):
        pass

    stobj = Stub()

    class Scheduler(Object):
        queueLength = Property(Stub)
        active = Bool(False)
    
    tsched = Scheduler()
    tsched.queueLength = stobj

    @planned
    def ScheduleQueueProcessed(
            scheduler1: Scheduler):
        assert  scheduler1.queueLength == stobj
        scheduler1.active = True