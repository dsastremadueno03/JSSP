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
dueDates = [2, 3, 1] # Due dates for each job (in hours)

passiveEnergy = [30, 20, 25] # Passive energy consumption of each machine (from its initial use until the end of the program)

# Matrix of Machine x Task that contains tuples of (duration, active energy consumption) for each machine and task. 
# No possible operation: (-1,-1)
tasksMachines = [
    [[2,60], [1,40], [2,50], [-1,-1], [3,70], [1,60], [2,70]], #Machine 0
    [[3,30], [-1,-1], [2,40], [2,60], [-1,-1], [1,50], [1,40]], #Machine 1
    [[1,30], [-1,-1], [2,40], [1,50], [2,40], [2,30], [1,40]] #Machine 2
]

mutationProb = 10 # Probability in % to get a mutation in a child

# Creation of the problem
PROBLEM = Problem(jobTasks, nJobs, nTasks, nMachines, energyPrices, dueDates, passiveEnergy, tasksMachines, mutationProb) #FINAL

# FUNCTIONS
# Creation of the individual
def genIndividual(problem):
    jobs = []
    #Initialize to 0
    for i in range(nJobs):
        jobs.append(0)
    tasks = []
    machines = []
    ids = []
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
        taskId = totalJob + jobs[job]-1
        while problem.getData(machine, taskId) == [-1,-1]: # As long as that machine can do the task
            machine = random.randint(0, problem.nMachines-1)
        machines.append(machine)
        ids.append(taskId)
    individual = Individual(tasks, machines, ids)
    individual.genSchedule(PROBLEM)
    individual.evaluate(PROBLEM)
    return individual

# Returns the best two individuals in a family of 2 parents and 2 children
# MODES -> 0: Minimize; 1: Maximize
def getBestTwo(fam, mode):
    # Lambda funtion that sorts by the time attribute first, and then by the energy. 
    fam.sort(key = lambda x: (x.fitness[0], x.fitness[1]), reverse=mode)
    result = fam[:2] # Take the best two
    return result
    


##################
###    MAIN    ###
##################

N_INDIVIDUALS = 20
N_GENERATIONS = 20
currentGeneration = []
nextGeneration = []
fitnessTimePlot = []
fitnessEnergyPlot = []

# MODE -> 0: Minimize; 1: Maximize
mode = 0

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
        best = getBestTwo(family, 0) # Minimize
        

    # 3rd -> Add to new generation the best two per family

        nextGeneration.append(best[0])
        nextGeneration.append(best[1])
        
    # 4th -> Shuffle generation (different genes) and join in pairs again
    random.shuffle(nextGeneration)
    currentGeneration.clear()
    for i in range(0, N_INDIVIDUALS, 2):
        currentGeneration.append([nextGeneration[i], nextGeneration[i+1]])
    nextGeneration.clear()

# Show best individual obtained by tardiness and energy cost separately
    fitnessTime = []
    fitnessEnergy = []
    for family in currentGeneration:
        fitnessTime.append(int(family[0].fitness[0]))
        fitnessTime.append(int(family[1].fitness[0]))
        fitnessEnergy.append(float(family[0].fitness[1]))
        fitnessEnergy.append(float(family[1].fitness[1]))
    minTimeFitness = min(fitnessTime)
    minEnergyFitness = min(fitnessEnergy)
    fitnessTimePlot.append(minTimeFitness)
    fitnessEnergyPlot.append(minEnergyFitness)
    minTimeIndex = fitnessTime.index(minTimeFitness)
    minEnergyIndex = fitnessEnergy.index(minEnergyFitness)
    

    
# Plot of fitness evolution

axisValue = []
for i in range(N_GENERATIONS):
    axisValue.append(int(i+1))

fig, ax = plt.subplots(1, 2, figsize=(10, 5))
ax[0].plot(axisValue, fitnessTimePlot, 'o-', linewidth=2, color='b')
ax[0].set(xlim=(0, N_GENERATIONS+2), ylim=(0, max(fitnessTimePlot)+2))
ax[0].set_xlabel('Generation')
ax[0].set_ylabel('Tardiness (h)')
ax[0].set_title('Evolution of tardiness')

ax[1].plot(axisValue, fitnessEnergyPlot, 'o-', linewidth=2, color='r')
ax[1].set(xlim=(0, N_GENERATIONS+2), ylim=(0, max(fitnessEnergyPlot)+200))
ax[1].set_xlabel('Generation')
ax[1].set_ylabel('Energy Cost (€)')
ax[1].set_title('Evolution of energy cost')

plt.tight_layout()
plt.show()

# Best individual data    
lastGeneration = [] # Stores individuals out of the pairs
for pair in currentGeneration:
    for individual in pair:
        lastGeneration.append(individual)
lastGeneration.sort(key = lambda x: (x.fitness[0], x.fitness[1]), reverse=mode) # Sorting to obtain the best individual
best = lastGeneration[0]
print("BEST:")
print(best)
print(best.schedule.startTimeTasks)
print(best.schedule.endTimeTasks)
print("Tardiness: " + str(best.fitness[0]))
print("Energy Consumption: " + str(best.fitness[1]))
    



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

# TEST 1.4 -> Mutation problem

Setting mutation prob. to 100% with a moderate population (20 individuals/gen.)
Checking if schedule does not reduce time. (Adding -1 from matrix)
"""
        











