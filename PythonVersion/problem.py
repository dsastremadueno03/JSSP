class Problem:    

    def __init__(self, nJobs, nTasks, nMachines, availableMachines, durations, energyPrices, dueDates, jobPresedence, energyConsumption):
        self.nJobs = nJobs
        self.nTasks = nTasks
        self.nMachines = nMachines
        self.availableMachines = availableMachines
        self.durations = durations
        self.energyPrices = energyPrices
        self.dueDates = dueDates
        self.jobPresedence = jobPresedence
        self.energyConsumption = energyConsumption
