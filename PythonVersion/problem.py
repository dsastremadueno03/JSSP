class Problem:    

# Constructor for the problem with jobs, number of machines, energy prices and due dates
    def __init__(self, jobTasks, nJobs, nTasks, nMachines, energyPrices, dueDates, tasksMachines):
        self.jobTasks = jobTasks # Array of jobs
        self.nJobs = nJobs # Number of jobs
        self.nTasks = nTasks # Number of tasks
        self.nMachines = nMachines # Number of machines
        self.energyPrices = energyPrices # Array of energy prices for each hour
        self.dueDates = dueDates # Array of due dates for each job

        # Matrix of Machine x Task that contains tuples of (duration, energy consumption) for each machine and task. 
        # No possible operation: (-1,-1)
        self.tasksMachines = tasksMachines 

    


