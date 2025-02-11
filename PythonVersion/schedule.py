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

    
    # Updates the schedule in a certain task, machine and job
    def updateSchedule(self, job, machine, taskPosition, problem):
        if self.endTask[job] == -1 and self.endMachine[machine] == -1: # If it is the first task to do in its job and machine
            self.startTimeTasks[taskPosition] = 0
        else:
            self.startTimeTasks[taskPosition] = max(self.endTask[job], self.endMachine[machine]) # It will start inmediately after the previous task is done and the machine is free
        # Update data of arrays
        self.endTimeTasks[taskPosition] = self.startTimeTasks[taskPosition] + problem.getData(machine, taskPosition)[0]
        #print(str(machine) + " " + str(taskPosition) + " " + str(problem.getData(machine, taskPosition)[0]))
        #print("EndTime " + str(taskPosition) + ": " + str(self.endTimeTasks[taskPosition]))
        self.endMachine[machine] = self.endTimeTasks[taskPosition]
        #print("EndMachine " + str(machine) + ": " + str(self.endMachine[machine]))
        self.endTask[job] = self.endTimeTasks[taskPosition]
        #print("EndTask " + str(job) + ": " + str(self.endTask[job]))
    