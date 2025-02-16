from schedule import Schedule
from problem import Problem
import random

class Individual:

    def __init__(self, taskPermutation, machinePermutation):
        self.tasksPermutation = taskPermutation
        self.machinePermutation = machinePermutation
        self.tardiness = []
        self.energyCost = 0
        self.fitness = 0
        self.schedule = None

    def __str__(self):
        return str(self.tasksPermutation) + "\n" + str(self.machinePermutation)
    
    # Gets the task id (inferred by how many times the job appears)
    # job -> job id
    # jobTasks -> array with number of appearences of each job
    def getTask(self, problem, job, jobTasks):
        totalJob = 0
        for i in range(job):
            totalJob += problem.jobTasks[i] # Add the previous tasks to get to the initial pos for the job in the array
        taskPosition = totalJob + jobTasks[job]
        jobTasks[job] += 1
        return taskPosition
    
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
            machine = self.machinePermutation[i]
            # Calculate the postition of the task in the array
            task = self.getTask(problem, job, jobTasks)
            self.schedule.updateSchedule(job, machine, task, problem)
        #print("Schedule has been generated correctly!")
        
    # Evaluates the tardiness, energy consumption and fitness of the individual
    def evaluate(self, problem):
        # Evaluates the tardiness of jobs
        for i in range(problem.nJobs):
            late = self.schedule.endTask[i] - problem.dueDates[i] 
            if late < 0:
                self.tardiness.append(0)
            else:
                self.tardiness.append(late)
        # Evaluates the total energy consumption
        jobTasks = []
        for i in range(problem.nJobs):
            jobTasks.append(0)
        for i in range(problem.nTasks):
            job = self.tasksPermutation[i]
            machine = self.machinePermutation[i]
            task = self.getTask(problem, job, jobTasks)
            self.energyCost += problem.getData(machine, task)[1] # Access to energy cost of specific case
        #TODO: ADD ENERGY CONSUMPTION TO IT
        self.fitness = max(self.schedule.endTimeTasks) # Calculate fitness 
        
    # Makes the child mutate (move one gene out of order)
    def mutate(child):
        gene = random.randint(0, len(child.tasksPermutation)-1)
        # Check that it is in range (does not alter the order of priority)
        job = child.tasksPermutation[gene]
        # Limit of changing positions
        limitMin = 0
        limitMax = gene
        for i in range(gene):
            if child.tasksPermutation[i] == job:
                limitMin = i
            if (i+gene < len(child.tasksPermutation)) and (child.tasksPermutation[i+gene] == job):
                limitMax = i+gene
            
            
        moveTo = random.randint(limitMin, limitMax)
        while gene == moveTo:
            moveTo = random.randint(0, len(child.tasksPermutation)-1)
        child.tasksPermutation.insert(moveTo, child.tasksPermutation.pop(gene))
        child.machinePermutation.insert(moveTo, child.machinePermutation.pop(gene))
            
    # Follows a job order crossover where self takes half or their jobs and the other half from the second parent
    def merge(self, individual2, problem):
        # Prepare matrices to save data
        newTasks = []
        newMachines = []
        for i in range(problem.nTasks):
            newTasks.append(-1)
            newMachines.append(-1)
        
            
        # Select which jobs to take from self
        jobsForSelf = [] # Stores the jobs that should be copied from self
        jobsForSecond = [] # Stores the indexes of the jobs taken from individual2
        for i in range(problem.nJobs//2):
            job = random.randint(0, problem.nJobs-1)
            while job in jobsForSelf:
                job = random.randint(0, problem.nJobs-1) 
            jobsForSelf.append(job)   
        
        # Get indexes of the rest of the jobs from the second parent
        for i in range(problem.nTasks):
            if individual2.tasksPermutation[i] not in jobsForSelf:
                jobsForSecond.append(i)

        
        # Copy the jobs from self in their position inside the child's arrays
        # First, we copy the tasks in self
        for i in range(problem.nTasks):
            if self.tasksPermutation[i] in jobsForSelf:
                newTasks[i] = self.tasksPermutation[i]  
                newMachines[i] = self.machinePermutation[i]
        # Next, we complete the array with those from the second parent
        j = 0 # index for second parent
        for i in range(problem.nTasks):
            if newTasks[i] == -1:
                newTasks[i] = individual2.tasksPermutation[jobsForSecond[j]]
                newMachines[i] = individual2.machinePermutation[jobsForSecond[j]]
                j += 1
            
        child = Individual(newTasks, newMachines)
        
        # Should it mutate?
        if random.randint(1, 100) <= problem.mutationProb:
            print("Mutation detected!")
            Individual.mutate(child)
            
        child.genSchedule(problem)
        child.evaluate(problem)
        return child