# ? Skill Prep
# ? For next activation types


def SkillPrep(op, t):
    op.delta = 0
    t.addKey(time + op.stats['atkTime'], DoSkill)

# ? SP Recoveries


def spRec_Auto(op, t):
    if op.skill['active']:
        op.skill['off']()
        op.skill['active'] = False

    op.skill['delta'] += self.op.stats['spRec']
    op.CheckSP()


def spRec_Offensive(op, t):
    if op.skill['active']:
        op.skill['off']()
        op.skill['active'] = False
    op.skill['delta'] += 1
    op.CheckSP()


def spRec_Defensive(op, t):
    if op.skill['active']:
        op.skill['off']()
        op.skill['active'] = False
    op.skill['delta'] += 1
    op.CheckSP()

# ? Skill Activation types


def spFull_Next(op, t):
    t.addKey(time + self.op.stats['atkTime'], "SkillPrep")

def spFull_Instant(op, t):
    self.killAttack(time, self.op.stats['spRec'])
    t.addKey(time, self.op.stats['spRec'], "Skill", "Attack")
    duration = skill['duration']

# ? Skill Activate
# ? Turn off skill ASAP?

def Skill_NextAttack(op, t):
    if not op.skill['active']:
        op.skill['on']()
        op.skill['active'] = True

    t.addKey(time + op.stats['atkTime'], "SP")

def Skill_Instant(op, t):
    if not op.skill['active']:
        op.skill['on']()
        op.skill['active'] = True
    if op.skill['delta'] == 0:
        op.killAttack(time, 1)
        t.addKey(time + 1, "SP", "Attack")
    else:
        t.addKey(time + 1, "Skill")


def DoAttack(op, t):
    # ? Do their own attacks
    t[time]["Attack"] = self.op.DoAttack()

    n_time, _ = t.getNextCmd(time, "Attack")
    if n_time != time and n_time != 0:
        if n_time > time + self.op.stats['atkTime']:
            # ! Double check this
            t.moveKey(n_time, time)
    else:
        t.addKey(time + self.op.stats['atkTime'], "Attack")
