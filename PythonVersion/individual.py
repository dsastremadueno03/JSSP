from schedule import Schedule
class Individual:

    def __init__(self, taskPermutation, machinePermutation):
        self.tasksPermutation = taskPermutation
        self.machinePermutation = machinePermutation
        self.tardiness = 0
        self.energyCost = 0
        self.fitness = 0
        self.schedule = None

    def __str__(self):
        return str(self.tasksPermutation) + "\n" + str(self.machinePermutation) + "\n" + str(self.tardiness) + "\n" + str(self.energyCost) + "\n" + str(self.fitness)
    
    def genSchedule(self):
        schedule = Schedule()