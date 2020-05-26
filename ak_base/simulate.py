from tools.Timeline import Timeline
from ak_base.calculation import *
class simulation ():
    def __init__(self, op, conf):
        self.op = op
        self.conf = conf
        self.t = Timeline()

    # Kill Attack should be used if an attack is scheduled AFTER skill activation.
    # This will remove the last scheduled attack command, it will be replaced during skill activation
    # Commonly used in: Auto Attack, batteries, 
    def killAttack(self, old_time, kill_range):
        i = self.t.getNextCmd(old_time, "Attack")
        # If next isn't self and exists
        if i != self.t.latest and i != 0:
            if i[0] > old_time + kill_range:
                self.t.rmCmd(i[0], "Attack")

    def run(self):
        self.t = Timeline()
        self.t.addKey(0, "Init")
        ref = self.t.latest

        skill = self.op.skill
        currentSp = skill['spData']['initSp']
        isSkill = False
        duration = 0

        while ref[0] < self.conf['period']:
            if "SkillPrep" in ref[1]:
                currentSp = 0
                self.t.addKey(ref[0] + self.op.stats['atkTime'], "Skill")

            if "Skill" in ref[1]:
                if isSkill == False:
                    skill['skill_on']()
                    isSkill = True
                if self.conf['trigger_type'] == "Next":
                    self.t.addKey(ref[0] + self.op.stats['atkTime'], "SP")
                elif self.conf['trigger_type'] == "Instant":
                    duration -= 1
                    if duration == 0:
                        self.killAttack(ref[0], 1)
                        self.t.addKey(ref[0] + 1, "SP", "Attack")
                        currentSp = 0
                    else:
                        self.t.addKey(ref[0] + 1, "Skill")
            # SP updates
            # If Auto recovery, use timer ticker
            if "SP" in ref[1] or "Init" in ref[1]:
                if isSkill == True:
                    skill['skill_off']()
                    isSkill = False
                if skill['spData']['spType'] == 1:
                    currentSp += self.op.stats['spRec']  # Usually will be 1
                    if self.conf['trigger_type'] == "Next":
                        # Next attack
                        if currentSp == skill['spData']['spCost']:
                            self.t.addKey(ref[0] + self.op.stats['atkTime'], "SkillPrep")
                        else:
                            self.t.addKey(ref[0] + self.op.stats['atkTime'], "SP")
                    elif self.conf['trigger_type'] == "Instant":
                        if currentSp == skill['spData']['spCost']:
                            self.killAttack(ref[0], self.op.stats['spRec'])
                            self.t.addKey(ref[0] + self.op.stats['spRec'], "Skill", "Attack")
                            duration = skill['duration']
                        else:
                            self.t.addKey(ref[0] + self.op.stats['spRec'], "SP")
                # If Offensive recovery, use atk speed
                elif skill['spData']['spType'] == 2:
                    # For next attack trigger
                    currentSp += 1
                    if self.conf['trigger_type'] == "Next":
                        if currentSp == skill['spData']['spCost']:
                            self.t.addKey(ref[0] + self.op.stats['atkTime'], "SkillPrep")
                        else:
                            self.t.addKey(ref[0] + self.op.stats['atkTime'], "SP")
                    elif self.conf['trigger_type'] == "Instant":
                        if currentSp == skill['spData']['spCost']:
                            self.killAttack(ref[0], self.op.stats['spRec'])
                            self.t.addKey(ref[0] + self.op.stats['spRec'], "Skill", "Attack")
                            duration = skill['duration']
                        else:
                            self.t.addKey(ref[0] + 1, "SP")
                # If Defensive recovery, use enemy atk speed
                elif skill['spData']['spType'] == 4:
                    currentSp += 1
                    # Ha ha yes no defensive + next
                    if self.conf['trigger_type'] == "Instant":
                        if currentSp == skill['spData']['spCost']:
                            self.killAttack(ref[0], self.op.stats['spRec'])
                            self.t.addKey(ref[0] + self.op.stats['spRec'], "Skill", "Attack")
                            duration = skill['duration']
                # If passive, do nothting because skill state will be active
            if "Attack" in ref[1] or "Init" in ref[1]:
                if self.conf["atk_type"] == "Physical":
                    self.t.addData(ref[0], PhysicalAttack(self.op, ""))
                elif self.conf["atk_type"] == "Arts":
                    self.t.addData(ref[0], ArtsAttack(self.op, ""))
                # Check if there's another attack scheduled
                i = self.t.getNextCmd(ref[0], "Attack")
                if i != 0 and i != ref:
                    # If it's scheduled ahead of time
                    if i[0] > ref[0] + self.op.stats['atkTime']:
                        self.t.moveKey(i[0], ref[0])
                else:
                    # If there's no other scheduled attack, make one
                    self.t.addKey(ref[0] + self.op.stats['atkTime'], "Attack")
            
            ref = self.t.getNext(ref[0])
        return self.t