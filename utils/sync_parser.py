class Resource:
    def __init__(self, name, count):
        self.name = name
        self.count = int(count)
        self.available = int(count)

    def __repr__(self):
        return f"{self.name}(available={self.available})"

class Action:
    def __init__(self, pid, action_type, resource_name, cycle):
        self.pid = pid
        self.action_type = action_type.upper()  # 'READ' o 'WRITE'
        self.resource_name = resource_name
        self.cycle = int(cycle)

    def __repr__(self):
        return f"{self.pid} {self.action_type} {self.resource_name} @ {self.cycle}"

def parse_resources(file_path):
    resources = {}
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip():
                name, count = line.strip().split(',')
                resources[name.strip()] = Resource(name.strip(), count.strip())
    return resources

def parse_actions(file_path):
    actions = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip():
                pid, action_type, resource, cycle = line.strip().split(',')
                actions.append(Action(pid.strip(), action_type.strip(), resource.strip(), cycle.strip()))
    return actions
