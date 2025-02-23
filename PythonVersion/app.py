from individual import Individual
from problem import Problem
from schedule import Schedule
import matplotlib.pyplot as plt
import random



# EXAMPLE DATA
nJobs = 3 # Total number of jobs
nTasks = 7 # Total number of tasks
nMachines = 3 # Total number of machines

jobTasks = [2, 3, 2] # Number of tasks for each job

energyPrices = [3, 2, 1, 1, 1, 2, 3, 4, 5, 5, 6, 6, 7, 8, 8, 7, 6, 5, 4, 6, 7, 7, 6, 4] # Energy prices for each hour
dueDates = [6, 5, 6] # Due dates for each job (in hours)

# Matrix of Machine x Task that contains tuples of (duration, energy consumption) for each machine and task. 
# No possible operation: (-1,-1)
tasksMachines = [
    [[2,1], [1,1], [2,3], [-1,-1], [3,3], [1,2], [2,3]], #Machine 0
    [[3,3], [-1,-1], [2,1], [2,2], [-1,-1], [1,1], [1,1]], #Machine 1
    [[1,3], [-1,-1], [2,2], [1,3], [2,4], [2,3], [1,2]] #Machine 2
]

mutationProb = 5 # Probability in % to get a mutation in a child

# Creation of the problem
PROBLEM = Problem(jobTasks, nJobs, nTasks, nMachines, energyPrices, dueDates, tasksMachines, mutationProb) #FINAL

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
        totalJob = 0
        for j in range(job):
            totalJob += problem.jobTasks[j]
        while problem.getData(machine, totalJob + jobs[job]-1) == [-1,-1]: # As long as that machine can do the task
            machine = random.randint(0, problem.nMachines-1)
        machines.append(machine)
    individual = Individual(tasks, machines)
    individual.genSchedule(PROBLEM)
    individual.evaluate(PROBLEM)
    return individual

# Returns the best two individuals in a family of 2 parents and 2 children
def getBestTwo(fam):
    result = [] # Stores the best two individuals
    fitness = [] # Stores the fitness of the individuals
    fitness.append(fam[0].fitness)
    fitness.append(fam[1].fitness)
    fitness.append(fam[2].fitness)
    fitness.append(fam[3].fitness)
    for i in range(2):
        index = fitness.index(min(fitness)) # Depends whether the fitness is better as a high or as a low value
        result.append(fam.pop(index))
        fitness.pop(index)
    return result
    
    

    

##################
###    MAIN    ###
##################

N_INDIVIDUALS = 80
N_GENERATIONS = 20
currentGeneration = []
nextGeneration = []
fitnessPlot = []

plt.style.use('_mpl-gallery')

# 1st -> Create initial pairs of individuals

for i in range(N_INDIVIDUALS//2):
    
    family = [genIndividual(PROBLEM), genIndividual(PROBLEM)]
    currentGeneration.append(family)


# Start genetic algorithm
for i in range(N_GENERATIONS):
    print("Generation " + str(i) + " in progress...")
    # 2nd -> Create children and evaluate
    for family in currentGeneration:
        family.append(family[0].merge(family[1], PROBLEM))
        family.append(family[1].merge(family[0], PROBLEM))
        best = getBestTwo(family)
        

    # 3rd -> Add to new generation the best two per family

        nextGeneration.append(best[0])
        nextGeneration.append(best[1])
        
    # 4th -> Shuffle generation (different genes) and join in pairs again
    random.shuffle(nextGeneration)
    currentGeneration.clear()
    for i in range(0, N_INDIVIDUALS, 2):
        currentGeneration.append([nextGeneration[i], nextGeneration[i+1]])
    nextGeneration.clear()

# Show best individual obtained
    fitness = []
    for family in currentGeneration:
        fitness.append(family[0].fitness)
        fitness.append(family[1].fitness)
    minFitness = min(fitness)
    print("Seleccionado: " + str(minFitness))
    fitnessPlot.append(minFitness)
    minIndex = fitness.index(minFitness)
    
# Plot of fitness evolution

axisValue = []
for i in range(N_GENERATIONS):
    axisValue.append(int(i+1))

fig, ax = plt.subplots()
ax.plot(axisValue, fitnessPlot, 'o-', linewidth=2)
ax.set(xlim=(0, N_GENERATIONS+2), ylim=(0, max(fitnessPlot)+2))
plt.show()

# Best individual data    
best = currentGeneration[minIndex//2][minIndex%2] # Accessing from individuals array to paired array
print(best)
print(best.schedule.startTimeTasks)
print(best.schedule.endTimeTasks)
print("Fitness: " + str(best.fitness))
print("Energy Consumption: " + str(best.energyCost))
    



"""

# TEST 1.1 -> Generate two individuals
parent1 = genIndividual(PROBLEM)
print("\nParent 1")
print(parent1)
print(parent1.schedule.startTimeTasks)
print(parent1.schedule.endTimeTasks)
#print(parent1.schedule.endTask)
#print(parent1.schedule.endMachine)
print("Fitness: " + str(parent1.fitness))
print("DueDates: " + str(parent1.tardiness))
print("Energy Consumption: " + str(parent1.energyCost))


parent2 = genIndividual(PROBLEM)
print("\nParent 2")
print(parent2)
print(parent2.schedule.startTimeTasks)
print(parent2.schedule.endTimeTasks)
#print(parent2.schedule.endTask)
#print(parent2.schedule.endMachine)
print("Fitness: " + str(parent2.fitness))
print("DueDates: " + str(parent2.tardiness))
print("Energy Consumption: " + str(parent2.energyCost))
            

# TEST 1.2 -> Generate two children 

child1 = parent1.merge(parent2, PROBLEM)
print("\nChild 1")
print(child1)
print("Fitness: " + str(child1.fitness))
print("DueDates: " + str(child1.tardiness))
print("Energy Consumption: " + str(child1.energyCost))
child2 = parent2.merge(parent1, PROBLEM)
while child2.tasksPermutation == child1.tasksPermutation:
    child2 = parent2.merge(parent1, PROBLEM)
print("\nChild 2")
print(child2) 
print("Fitness: " + str(child2.fitness))
print("DueDates: " + str(child2.tardiness))
print("Energy Consumption: " + str(child2.energyCost))

# TEST 1.3 -> Get the best two out of the four individuals

bestTwo = getBestTwo(parent1, parent2, child1, child2)
print("\n\nBest 1: ")
print(bestTwo[0])
print(bestTwo[0].fitness)
print("\n\nBest 2: ")
print(bestTwo[1])
print(bestTwo[1].fitness) 

"""
        











