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
        return str(self.tasksPermutation) + "\n" + str(self.machinePermutation)
    
    # Generates a schedule based on the individual
    def genSchedule(self, problem):
        if len(self.tasksPermutation) != problem.nTasks or len(self.machinePermutation) != problem.nTasks: # If individual has no data
            return None
        # Create schedule
        self.schedule = Schedule(problem.nMachines, problem.nJobs, problem.nTasks)
        jobTasks = [] # Keep track of how many times a job's task has been made
        for i in range(problem.nJobs):
            jobTasks.append(0)
        # Go through the task permutation and the machine permutation
        for i in range(problem.nTasks):
            job = self.tasksPermutation[i]
            jobTasks[job] += 1
            machine = self.machinePermutation[i]
            # Calculate the postition of the task in the array
            totalJob = 0
            for i in range(job):
                totalJob += problem.jobTasks[i] # Add the previous tasks to get to the initial pos for the job in the array
            taskPosition = totalJob + jobTasks[job] - 1
            self.schedule.updateSchedule(job, machine, taskPosition, problem)
        print("Schedule has been generated correctly!")
            
    def showSchedule(self, problem):
        s = "  \t"
        for i in range(50):
            s += str(i) + " "
        s += "\n"
        for i in range(problem.nMachines):
            s += "M" + str(i+1) + "\t"
            startTime = []
            for j in range(problem.nTasks):
                startTime.append(self.schedule.startTimeTasks[j])
            stop = max(startTime) + 1
            endTime = 0
            while min(startTime) < stop:
                index = startTime.index(min(startTime))
                startTime[index] = max(startTime) + 1
                if self.machinePermutation[index] == i:
                    for k in range(self.schedule.startTimeTasks[index] - endTime):
                        s += "  "
                    if endTime == 0:
                        s += "- "
                    for k in range(self.schedule.endTimeTasks[index] - self.schedule.startTimeTasks[index] - 1 ):
                        s += "- "
                    s += "+ "
                    endTime = self.schedule.endTimeTasks[index]     
            s += "\n"
        print(s)