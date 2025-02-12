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
        #print("Schedule has been generated correctly!")
        
    def evaluate(self, problem):
        for i in range(problem.nJobs):
            late = self.schedule.endTask[i] - problem.dueDates[i] 
            if late < 0:
                self.tardiness.append(0)
            else:
                self.tardiness.append(late)
        self.fitness = max(self.schedule.endTimeTasks)
            