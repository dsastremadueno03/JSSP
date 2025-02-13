from schedule import Schedule
from problem import Problem
import matplotlib.pyplot as plt
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
            