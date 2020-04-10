from tools.Timeline import Timeline

class simulate ():
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

        duration = 0

        while ref[0] < self.conf['period']:
            if "Attack" in ref[1] or "Init" in ref[1]:
                # Check if there's another attack scheduled
                i = self.t.getNextCmd(ref[0], "Attack")
                if i != 0:
                    if i != ref:
                        # If it's scheduled ahead of time
                        if i[0] > ref[0] + self.op.stats['atkTime']:
                            self.t.movekey(i[0], ref[0])
                else:
                    # If there's no other scheduled attack, make one
                    self.t.addKey(ref[0] + self.op.stats['atkTime'], "Attack")
            
            if "SkillPrep" in ref[1]:
                currentSp = 0
                self.t.addKey(ref[0] + self.op.stats['atkTime'], "Skill")
                # Activate skill here ------------------------------------------------------
                skill['skill_on']()

            if "Skill" in ref[1]:
                if self.conf['trigger_type'] == "Next":
                    self.t.addKey(ref[0] + self.op.stats['atkTime'], "SP")
                    # Deactivate skill here ------------------------------------------------
                    skill['skill_off']()
                elif self.conf['trigger_type'] == "Instant":
                    duration -= 1
                    if duration == 0:
                        self.killAttack(ref[0], 1)
                        self.t.addKey(ref[0] + 1, "SP", "Attack")
                        currentSp = 0
                        # Deactivate skill here --------------------------------------------
                        skill['skill_off']()
                    else:
                        self.t.addKey(ref[0] + 1, "Skill")
            # SP updates
            # If Auto recovery, use timer ticker
            if "SP" in ref[1] or "Init" in ref[1]:
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
                            # Activate skill here------------------------------------------
                            skill['skill_on']()
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
                            # Activate skill here ------------------------------------------
                            skill['skill_on']()
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
                            state = "Skill"
                # If passive, do nothting because skill state will be active
            ref = self.t.getNext(ref[0])
        return self.t.keys