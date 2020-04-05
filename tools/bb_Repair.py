def toDict(blackboard):
    output = dict()
    for entry in blackboard:
        output[entry['key']] = entry['value']
    return output