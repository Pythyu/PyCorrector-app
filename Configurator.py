import yaml

class Config:
    STATIC = []
    FUNCTIONS = []
    EXPECTED_OUTPUTS = []
    SCORE_FUNCTIONS = []
    TIMEOUT_FUNCTIONS = []

class UserFunc:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return self.name+": "+str(self.value)

class DataSet:
    def __init__(self, data, stripped=False):
        self.dataset = data
        self.stripped = stripped

    def __str__(self):
        if self.stripped:
            tmp = str([e.forward() for e in self.dataset])
            tmp = tmp.replace("'","")
            return tmp
        return str([e.forward() for e in self.dataset])

class Arguments:
    def __init__(self, args, stripped=False):
        self.args = args
        self.stripped = stripped

    def forward(self):
        if self.stripped:
            return self.args[0].forward()
        return [e.forward() for e in self.args]

class Data:
    def __init__(self, data):
        self.data = data

    def forward(self):
        return self.data

def add_new_function(name,data):
    # Append to already existing one if possible
    tmp = [nm.name for nm in Config.FUNCTIONS]
    if name in tmp:
        add_args_to_function(tmp.index(name), data)
        return
    # Create a new one otherwise
    payload = Data(data)
    args = Arguments([payload])
    set = DataSet([args])
    Config.FUNCTIONS.append(UserFunc(name, set))

def add_args_to_function(id, data):
    payload = Data(data)
    args = Arguments([payload])
    Config.FUNCTIONS[id].value.dataset.append(args)

def add_data_to_args(name, argsID, data):
    tmp = [nm.name for nm in Config.FUNCTIONS]
    if name not in tmp:
        return

    id = tmp.index(name)
    payload = Data(data)
    Config.FUNCTIONS[id].value.dataset[argsID].args.append(payload)

def test_gen():
    payload = Data("Test1")
    args = Arguments([payload])
    set = DataSet([args])
    return UserFunc("Testfunction", set)
