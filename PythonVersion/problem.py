class Problem:    

# Constructor for the problem with jobs, number of machines, energy prices and due dates
    def __init__(self, jobTasks, nJobs, nTasks, nMachines, energyPrices, dueDates, passiveEnergy, tasksMachines, mutationProb, thresholdGenetic, nIndividual, xoverProb, compType):
        self.jobTasks = jobTasks # Array of jobs
        self.nJobs = nJobs # Number of jobs
        self.nTasks = nTasks # Number of tasks
        self.nMachines = nMachines # Number of machines
        self.energyPrices = energyPrices # Array of energy prices for each minute
        self.passiveEnergy = passiveEnergy # Array of the passive energy consumption of each machine
        self.dueDates = dueDates # Array of due dates for each job
        self.thresholdGenetic = thresholdGenetic # Number of generations without improvement to stop the genetic algorithm
        self.nIndividual = nIndividual # Number of individuals per generation
        self.xoverProb = xoverProb # Probability of crossover
        self.compType = compType # Lexico-graphical or mono-objective comparison type

        # Matrix of Machine x Task that contains tuples of (duration in minutes, energy consumption) for each machine and task. 
        # No possible operation: (-1,-1)
        self.tasksMachines = tasksMachines 
        
        self.mutationProb = mutationProb # Probability of mutation

# Retrieve data from tasksMachines matrix
    def getData(self, machine, task):
        return self.tasksMachines[machine][task]
        
    


