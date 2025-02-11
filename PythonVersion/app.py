from individual import Individual
from problem import Problem
from schedule import Schedule
import random


# EXAMPLE DATA
nJobs = 3 # Total number of jobs
nTasks = 7 # Total number of tasks
nMachines = 3 # Total number of machines

jobTasks = [2, 3, 2] # Number of tasks for each job

energyPrices = {3, 2, 1, 1, 1, 2, 3, 4, 5, 5, 6, 6, 7, 8, 8, 7, 6, 5, 4, 6, 7, 7, 6, 4} # Energy prices for each hour
dueDates = {10, 12, 11} # Due dates for each job (in hours)

# Matrix of Machine x Task that contains tuples of (duration, energy consumption) for each machine and task. 
# No possible operation: (-1,-1)
tasksMachines = [
    [[2,1], [1,1], [2,3], [-1,-1], [3,3], [1,2], [2,3]], #Machine 0
    [[3,3], [-1,-1], [2,1], [2,2], [-1,-1], [1,1], [1,1]], #Machine 1
    [[1,3], [-1,-1], [2,2], [1,3], [2,4], [2,3], [1,2]] #Machine 2
]


# Creation of the problem
PROBLEM = Problem(jobTasks, nJobs, nTasks, nMachines, energyPrices, dueDates, tasksMachines) #FINAL

# FUNCTIONS
# Creation of the individual
def genIndividual(problem):
    jobs = []
    #Initialize to 0
    for i in range(nJobs):
        jobs.append(0)
    tasks = []
    machines = []
    for i in range(problem.nTasks):
        # Choose job to do task from
        job = random.randint(0, problem.nJobs-1)
        while problem.jobTasks[job] == jobs[job]: # As long as the job is not complete
            job = random.randint(0, problem.nJobs-1)
        tasks.append(job)
        jobs[job] += 1
        # Choose machine to do task in
        machine = random.randint(0, problem.nMachines-1)
        while tasksMachines[machine][job+jobs[job]-1] == [-1,-1]: # As long as that machine can do the task
            machine = random.randint(0, problem.nMachines-1)
        machines.append(machine)
    return Individual(tasks, machines)


    


###    MAIN    ###

parent1 = genIndividual(PROBLEM)
print(parent1)



            

    
        
        
    










