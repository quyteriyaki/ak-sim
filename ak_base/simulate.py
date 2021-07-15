from ak_base.Timeline import Timeline
from ak_base.calculation import *

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
        time, cmds = t.tail

        skill = self.op.skill
        currentSp = skill['spData']['initSp']
        isSkill = False
        duration = 0

        while time <= self.conf['period']:
            if "SkillPrep" in cmds:
                currentSp = 0
                t.addKey(time + self.op.stats['atkTime'], 'Skill')
            
            if "Skill" in cmds:
                if not isSkill:
                    skill['on']()
                    isSkill = True
                if self.conf['trigger_type'] == "Next":
                    t.addKey(time + self.op.stats['atkTime'], "SP")
                elif self.conf['trigger_type'] == "Instant":
                    duration -= 1
                    if duration == 0:
                        self.killAttack(time, 1)
                        t.addKey(time + 1, "SP", "Attack")
                        currentSp = 0
                    else:
                        t.addKey(time + 1, "Skill")
            # SP updates
            if "SP" in cmds or "Init" in cmds:
                if isSkill:
                    skill['off']()
                    isSkill = False
                # If Auto recovery, use timer ticker
                if skill['spData']['spType'] == 1:
                    if currentSp == skill['spData']['spCost']:
                        if self.conf['trigger_type'] == "Next":
                            t.addKey(time + self.op.stats['atkTime'], "SkillPrep")
                        elif self.conf['trigger_type'] == "Instant":
                            self.killAttack(time, self.op.stats['spRec'])
                            t.addKey(time, self.op.stats['spRec'], "Skill", "Attack")
                            duration = skill['duration']
                    else:
                        t.addKey(time + self.op.stats['spRec'], "SP")
                    currentSp += self.op.stats['spRec']
                # If Offensive recovery, use atk speed
                elif skill['spData']['spType'] == 2:
                    # For next attack trigger
                    currentSp += 1
                    if currentSp == skill['spData']['spCost']:
                        if self.conf['trigger_type'] == "Next":
                            t.addKey(time + self.op.stats['atkTime'], "SkillPrep")
                        elif self.conf['trigger_type'] == "Instant":
                            self.killAttack(time, self.op.stats['spRec'])
                            t.addKey(time, self.op.stats['spRec'], "Skill", "Attack")
                            duration = skill['duration']
                    else:
                        t.addKey(time + self.op.stats['atkTime'], "SP")
            
            if "Attack" in cmds or "Init" in cmds:
                if self.conf["atk_type"] == "Physical":
                    t[time]["Attack"] = PhysicalAttack(self.op, "")
                elif self.conf["atk_type"] == "Arts":
                    t[time]["Attack"] = ArtsAttack(self.op, "")
                
                n_time, _ = t.getNextCmd(time, "Attack")
                if n_time != time and n_time != 0:
                    if n_time > time + self.op.stats['atkTime']:
                        # ! Double check this
                        t.moveKey(n_time, time)
                else:
                    t.addKey(time + self.op.stats['atkTime'], "Attack")
            
            time, cmds = t.getNextKey(time)
        return self.timeline