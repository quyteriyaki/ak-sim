
def PhysicalAttack(operator, enemy):
    # Physical Damage
    # hitNumber (atk - def) >= atk * 0.05
    # (atk - (def + flat_def_down) * (1 - scale_def_down)) * damage_amp
    val = round(
        (operator.stats['atk'] - 50)
    )
    return (val)

def ArtsAttack(operator, enemy):
    # Arts Damage
    # Arts Damage
    # hitNumber (Matk * (1 - Mres)) (Mres decimal)
    # atk * [1 - {(res + flat_res_down)(1 - scale_res_down) / 100] * damage_amp
    val = round(
        (operator.stats['atk'] * (10 / 100)) * operator.attack['times']
    )
    return(val)