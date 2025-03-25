from individual import Individual
from instanceReader import InstanceReader
from problem import Problem
from schedule import Schedule
import matplotlib.pyplot as plt
import random
import pandas as pd
import pickle
import os
import shutil

random.seed(4) # Fix the randomness

"""
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

"""

# RETRIEVE DATA FROM FILES
instanceReader = InstanceReader(r"instances_new\instances_new\flexible_jobshop_59_10jobs_10machines_flex_high_squared.data", r"preparedjobs_new\preparedjobs_new\flexible_jobshop_59_10jobs_10machines_flex_high_squared_JOBS.data", r"TOU prices\TOU prices\TOU_prices_v1", r"passive_energy\passive_energy_10machines.txt", r"mutation_prob_genetic_parameters.txt")

# Read and assign data retrieved to the problem
dataInstance = instanceReader.readInstance()
dataPreparedJobs = instanceReader.readPreparedJobs()
dataTOUPrices = instanceReader.readTOUPrices()
dataPassiveEnergy = instanceReader.readPassiveEnergy()
dataMutationProb = instanceReader.readMutationProb()
instanceReader.transformInstanceData(dataInstance)
instanceReader.transformPreparedJobsData(dataPreparedJobs)
instanceReader.transformTOUPricesData(dataTOUPrices)
instanceReader.transformPassiveEnergyData(dataPassiveEnergy)
# Store the number of iterations per instance (repetitions of the algorithm)
nIterations = instanceReader.transformMutationProbData(dataMutationProb)

### FOR COMPARING RESULTS ONLY
instanceReader.problem.passiveEnergy = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Creation of the problem
PROBLEM = instanceReader.problem #FINAL

# FUNCTIONS
# Creation of the individual
def genIndividual(problem):
    jobs = []
    #Initialize to 0
    for i in range(problem.nJobs):
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
# FACTORS -> 0: Tardiness; 1: Energy Consumption
# bestInGen -> Best individual in the generation
def getBestTwo(fam, mode, factor, bestInGen):
    best = bestInGen
    # Lambda funtion that sorts by the priority attribute first, and then by the secondary. 
    if factor == 0:
        fam.sort(key = lambda x: (x.fitness[0], x.fitness[1]), reverse=(mode == 1))
    else:
        fam.sort(key = lambda x: (x.fitness[1], x.fitness[0]), reverse=(mode == 1))
    result = fam[:2] # Take the best two
    # Check if the best of the generation is better than the best two of the current family
    if result[0].isBetter(best, mode, factor):
        best = result[0]
    if result[1].isBetter(best, mode, factor):
        best = result[1]
    result.append(best) # Add the best individual of the generation
    return result
    


##################
###    MAIN    ###
##################

N_INDIVIDUALS = PROBLEM.nIndividual

# MODE -> 0: Minimize; 1: Maximize
mode = 0

plt.style.use('_mpl-gallery')

# Restart folder to store the results
folder = "results"
if os.path.exists(folder):
    shutil.rmtree(folder)
os.makedirs(folder, exist_ok=True)

for a in range(nIterations):
    currentGeneration = []
    nextGeneration = []
    fitnessTimePlot = []
    fitnessEnergyPlot = []
    

    # 1st -> Create initial pairs of individuals

    for i in range(N_INDIVIDUALS//2):
        
        family = [genIndividual(PROBLEM), genIndividual(PROBLEM)]
        bestInGen = family[0]
        currentGeneration.append(family)

    # Threshold for the algorithm to stop
    nGenWithoutImprovement = 0
    gen = 0 # Generation counter
    # Start genetic algorithm and stop when there is no improvement in whatever the mutation_prob file states generations
    while(nGenWithoutImprovement < PROBLEM.thresholdGenetic):
        print("Generation " + str(gen) + " in progress...")
        lastBest = bestInGen
        # 2nd -> Create children and evaluate
        for family in currentGeneration:
            family.append(family[0].merge(family[1], PROBLEM))
            family.append(family[1].merge(family[0], PROBLEM))
            best = getBestTwo(family, 0, 0, bestInGen) # Minimize by tardiness
            
        # Check if it is the best of the generation
            bestInGen = best[2] # Updates the best individual in the current generation
            
        # 3rd -> Add to new generation the best two per family

            nextGeneration.append(best[0])
            nextGeneration.append(best[1])
            
        # See if there was improvement
        if bestInGen == lastBest:
            nGenWithoutImprovement += 1
        else:
            nGenWithoutImprovement = 0
            
        # 4th -> Shuffle generation (different genes) and join in pairs again  
        random.shuffle(nextGeneration)
        currentGeneration.clear()
        for i in range(0, N_INDIVIDUALS, 2):
            currentGeneration.append([nextGeneration[i], nextGeneration[i+1]])
        nextGeneration.clear()
        gen += 1

    # Show best individual obtained by tardiness and energy cost separately
        fitnessTimePlot.append(bestInGen.fitness[0])
        fitnessEnergyPlot.append(bestInGen.fitness[1])

    # Save total number of generations
    N_GENERATIONS = gen

    # Best individual data    
    best = bestInGen
    print("BEST:")
    print(best)
    print(best.schedule.startTimeTasks)
    print(best.schedule.endTimeTasks)
    print("Tardiness: " + str(best.fitness[0]))
    print("Energy Consumption: " + str(best.fitness[1]))

    # Serialize best candidate with pickle and save it in a "result" folder
    path = os.path.join(folder, f"result_{a+1}.pkl")
    with open(path, 'wb') as file: 
        pickle.dump(best, file)
    

# Plot of fitness evolution

axisValue = []
for i in range(N_GENERATIONS):
    axisValue.append(int(i+1))

fig, ax = plt.subplots(1, 3, figsize=(10, 6))
colors = plt.get_cmap("tab10", PROBLEM.nMachines)
ax[0].plot(axisValue, fitnessTimePlot, 'o-', linewidth=2, color='b')
ax[0].set(xlim=(0, N_GENERATIONS+2), ylim=(0, max(fitnessTimePlot)+2))
ax[0].set_xlabel('Generation')
ax[0].set_ylabel('Tardiness (min)')
ax[0].set_title('Evolution of tardiness')

ax[1].plot(axisValue, fitnessEnergyPlot, 'o-', linewidth=2, color='r')
ax[1].set(xlim=(0, N_GENERATIONS+2), ylim=(0, max(fitnessEnergyPlot)+200))
ax[1].set_xlabel('Generation')
ax[1].set_ylabel('Energy Cost (€)')
ax[1].set_title('Evolution of energy cost')

# Plot of schedule

y_pos = []
durations = []
machine_labels = []
tasks = []
start_times = []

for i in range(PROBLEM.nMachines):
    y_pos.append(i)

for task in range(PROBLEM.nTasks):
    if best.schedule.startTimeTasks[task] != -1:
        start = best.schedule.startTimeTasks[task]
        end = best.schedule.endTimeTasks[task]
        duration = end - start

        start_times.append(start)
        durations.append(duration)
        tasks.append(f"T{task}")  # Task tag
        indexMachine = best.idPermutation.index(task)
        machine_labels.append(best.machinePermutation[indexMachine])  # Assigned machine

for i in range(PROBLEM.nTasks):
    ax[2].barh(machine_labels[i], durations[i], left=start_times[i], 
                color=colors(machine_labels[i] % PROBLEM.nMachines), edgecolor="black")
    
    # Label each task in the middle of the bar
    ax[2].text(start_times[i] + durations[i] / 2, machine_labels[i], tasks[i], 
               va="center", ha="center", color="white")

# Setting plot info
ax[2].set_xlabel("Time (h)")
ax[2].set_ylabel("Machines")

# Ensure only the 3 machines appear on the y-axis
ax[2].set_yticks(range(PROBLEM.nMachines))  
ax[2].set_yticklabels([f"M{i}" for i in range(PROBLEM.nMachines)])

ax[2].set_title("Best Found Schedule")
ax[2].grid(axis="x", linestyle="--", alpha=0.7)

plt.tight_layout()
plt.show()

"""
# GENERATE CSV

headers = [
    "Task",
    "Job",
    "Machine",
    "Start Time",
    "End Time"
]

df1 = pd.DataFrame(headers)

data = [
    best.idPermutation,
    best.tasksPermutation,
    best.machinePermutation,
    best.schedule.startTimeTasks,
    best.schedule.endTimeTasks
]

df2 = pd.DataFrame(data).T # Transpose the data to the headers

df1.to_csv("result.csv", index=False, header=False)
df2.to_csv("result.csv", mode='a', index=False, header=False)

print("Results were saved correctly!")

"""

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
        











