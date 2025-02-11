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
            #print("job " + str(job))
            #print("jobTasks[job] " + str(jobTasks[job]-1))
            # Calculate the postition of the task in the array
            totalJob = 0
            for i in range(job):
                totalJob += problem.jobTasks[i] # Add the previous tasks to get to the initial pos for the job in the array
            taskPosition = totalJob + jobTasks[job] - 1
            #print("taskPosition " + str(taskPosition))
            self.schedule.updateSchedule(job, machine, taskPosition, problem)
        print("Schedule has been generated correctly!")
            
    def showSchedule(self, problem):
        s = "  \t"
        for i in range(50):
            s += str(i) + " "
        s += "\n"
        for i in range(problem.nMachines):
            s += "M" + str(i+1) + "\t"
            for j in range(problem.nTasks):
                if self.machinePermutation[j] == i:
                    for k in range(self.schedule.startTimeTasks[j]-1):
                        s += "  "
                    for k in range(self.schedule.endTimeTasks[j] - self.schedule.startTimeTasks[j]):
                        s += "- "
                    s += "+ "    
            s += "\n"
        print(s)