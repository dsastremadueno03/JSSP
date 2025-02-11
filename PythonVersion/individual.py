class Individual:

    def __init__(self, taskArray, machineArray):
        self.taskArray = taskArray
        self.machineArray = machineArray
        self.tasksPermutation = []
        self.machinePermutation = []
        self.tardiness = 0
        self.energyCost = 0
        self.fitness = 0
        self.Schedule = None

    