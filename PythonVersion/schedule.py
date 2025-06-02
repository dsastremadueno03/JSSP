class Schedule:

# Represents the schedule from a given individual
    def __init__(self, nMachines, nJobs, nTasks, dueDates):
        self.dueDates = dueDates
        self.nMachines = nMachines # Number of machines
        self.nJobs = nJobs
        self.nTasks = nTasks # Number of tasks
        self.startTimeTasks = [] # Array of start times for each task 
        self.endTimeTasks = [] # Array of end times for each task
        self.endMachine = [] # Array of end times of the last scheduled task for each machine (initially -1)
        self.endTask = [] # Array of end times for each job (initially -1)
        self.startMachine = [] # Array of initial time of a machine (for passive energy)

    # Initialize the arrays with -1
        for i in range(nTasks):
            self.startTimeTasks.append(-1)
            self.endTimeTasks.append(-1)
        for i in range(nMachines):
            self.endMachine.append(-1)
            self.startMachine.append(-1)
        for i in range(nJobs):
            self.endTask.append(-1)

    
    # Updates the schedule in a certain task, machine and job
    def updateSchedule(self, job, machine, taskPosition, problem, factor):
        # Update the start time of the task
        if self.endTask[job] == -1 and self.endMachine[machine] == -1: # If it is the first task to do in its job and machine
            self.startTimeTasks[taskPosition] = 0
        else:
            self.startTimeTasks[taskPosition] = max(self.endTask[job], self.endMachine[machine]) # It will start inmediately after the previous task is done and the machine is free
              
        # If looking for energy cost, read the most expensive prices and avoid using them 
        if factor == 1: 
            # Get prices per hour
            priceInHours = [] 
            isOnlyPrice = True # Check if there is only one same price for all the hours
            for i in range(24):
                newPrice = problem.energyPrices[i*60] # Get the price for the hour
                if len(priceInHours) > 0 and newPrice not in priceInHours:
                    isOnlyPrice = False
                priceInHours.append(newPrice)
            # Get the 4 most expensive prices
            mostExpensivePrices = sorted(priceInHours, reverse=True)[:12]
            # If the price of the start time is one of the most expensive, add 1 minute to the start time
            if not isOnlyPrice: # If there is only one price, need to avoid infinite loop
                while problem.energyPrices[self.startTimeTasks[taskPosition] % 1440] in mostExpensivePrices:
                    self.startTimeTasks[taskPosition] += 1

        # Update data of arrays
        self.endTimeTasks[taskPosition] = self.startTimeTasks[taskPosition] + problem.getData(machine, taskPosition)[0] # Time taken by the task
        if self.startMachine[machine] == -1: # If it is the first task to do in its machine
            self.startMachine[machine] = self.startTimeTasks[taskPosition] # Update the start time of the machine
        self.endMachine[machine] = self.endTimeTasks[taskPosition] # Update the end time of the machine
        self.endTask[job] = self.endTimeTasks[taskPosition] # Update the end time of the job
        

            
    