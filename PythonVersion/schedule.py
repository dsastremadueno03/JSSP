class Schedule:

# Represents the schedule from a given individual
    def __init__(self, nMachines, nJobs, nTasks):
        self.startTimeTasks = [] # Array of start times for each task 
        self.endTimeTasks = [] # Array of end times for each task
        self.endMachine = [] # Array of end times of the last scheduled task for each machine (initially -1)
        self.endTask = [] # Array of end times for each job (initially -1)

    # Initialize the arrays with -1
        for i in range(nTasks):
            self.startTimeTasks.append(-1)
            self.endTimeTasks.append(-1)
        for i in range(nMachines):
            self.endMachine.append(-1)
        for i in range(nJobs):
            self.endTask.append(-1)

    