from ak_base.Timeline import Timeline
from ak_base.calculation import *
from ak_base.operator import Operator

class simulation ():
    def __init__(self, op, conf):
        self.op = op
        self.conf = conf
        self.timeline = Timeline()

    # Kill Attack should be used if an attack is scheduled AFTER skill activation.
    # This will remove the last scheduled attack command, it will be replaced during skill activation
    # Commonly used in: Auto Attack, batteries, 
    def killAttack(self, old_time, kill_range):
        key, _ = self.timeline.getNextCmd(old_time, "Attack")
        
        # If next isn't self
        if key != old_time and key != 0:
            if key >= old_time + kill_range:
                self.timeline.removeCmd(key, "Attack")

    def run(self):

        t = self.timeline = Timeline()
        t.addKey(0, "Init")
        time, events = t.tail

        # ? is shorthanding good?
        skill = self.op.skill

        while time <= self.conf['period']:
            self.op.DoSP()

            for e in events:
                e(op, t)
            
            time, events = t.getNextKey(time)
        return self.timeline