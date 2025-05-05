from individual import Individual
from instanceReader import InstanceReader
from problem import Problem
from schedule import Schedule
import random # Randomize creation of individuals and other decisions
import pandas as pd # Export data as csv
import pickle # Serialize the best individuals
import os # Access paths
import time # Check time of the runtime
import glob # Access files in the folder with *
import sys # Access command line arguments
from pathlib import Path # Access paths through different OS

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
    individual.genSchedule(problem)
    individual.evaluate(problem)
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



# Parameter to know which file to read
iLabel = sys.argv[1] # Get the label of the instance from the command line argument
print("Instance " + str(iLabel) + " in progress...")
print(glob.glob(fr"instances_new/instances_new/flexible_jobshop_{iLabel}_*"))
# RETRIEVE DATA FROM FILES

# Create the instance reader, but do not read the prepared jobs nor the passive energy yet 
# (They contain variables in the name)
instanceReader = InstanceReader(glob.glob(fr"instances_new/instances_new/flexible_jobshop_{iLabel}_*")[0], "", r"TOU prices/TOU prices/TOU_prices_v1", "", r"mutation_prob_genetic_parameters.txt")

# Read and assign data retrieved to the problem
dataInstance = instanceReader.readInstance()
instanceReader.transformInstanceData(dataInstance)

# Now we know machine number and job number, we can read the rest of the files
iJob = instanceReader.problem.nJobs # Number of jobs
iMachine = instanceReader.problem.nMachines # Number of machines
instanceReader.pathPreparedJobs = glob.glob(fr"preparedjobs_new/preparedjobs_new/flexible_jobshop_{iLabel}_{iJob}jobs_{iMachine}machines_*")[0]
instanceReader.pathPassiveEnergy = fr"passive_energy/passive_energy_{iMachine}machines.txt"

dataPreparedJobs = instanceReader.readPreparedJobs()
dataTOUPrices = instanceReader.readTOUPrices()
dataPassiveEnergy = instanceReader.readPassiveEnergy()
dataMutationProb = instanceReader.readMutationProb()

instanceReader.transformPreparedJobsData(dataPreparedJobs)
instanceReader.transformTOUPricesData(dataTOUPrices)
instanceReader.transformPassiveEnergyData(dataPassiveEnergy)
# Store the number of iterations per instance (repetitions of the algorithm)
# MODE -> 0: Minimize; 1: Maximize
# FACTOR -> 0: Tardiness; 1: Energy Cost
nIterations, mode, factor, xover, mutType = instanceReader.transformMutationProbData(dataMutationProb)

### FOR COMPARING RESULTS ONLY
#instanceReader.problem.passiveEnergy = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Creation of the problem
PROBLEM = instanceReader.problem #FINAL

# Establish the number of iterations and the number of individuals
N_INDIVIDUALS = PROBLEM.nIndividual
bests = [] # Store the best individual from each iteration to then pickle the list
totalExecutionTime = 0.0

# Restart folder to store the results 
# ORDER: Min/Max -> Tardiness/EnergyCost -> JOX/PPX/GPMX/GOX -> INS/SWAP/INV
mode_str = "Min" if mode == 0 else "Max"
factor_str = "Tardiness" if factor == 0 else "EnergyCost"
xover_str = "JOX" if xover == 0 else "PPX" if xover == 1 else "GPMX" if xover == 2 else "GOX"
mutType_str = "INS" if mutType == 0 else "SWAP" if mutType == 1 else "INV"

folder = rf"results/{mode_str}/{factor_str}/{xover_str}/{mutType_str}"

os.makedirs(folder, exist_ok=True)
os.makedirs(folder+r"/pickle", exist_ok=True)
os.makedirs(folder+r"/text", exist_ok=True)
os.makedirs(folder+r"/graphic", exist_ok=True) 
# Delete the files if they exist to overwrite them
if os.path.exists(folder+rf"/text/result_{iLabel}.txt"):
    os.remove(folder+rf"/text/result_{iLabel}.txt")
if os.path.exists(folder+rf"/pickle/result_{iLabel}.pkl"):
    os.remove(folder+rf"/pickle/result_{iLabel}.pkl")
if glob.glob(folder+rf"/graphic/*_result_{iLabel}.pkl") != []: 
    for each in glob.glob(folder+rf"/graphic/*_result_{iLabel}.pkl"):
        os.remove(each)
        
path = os.path.join(folder+r"/text", f"result_{iLabel}.txt")
with open(path, 'a') as file: 
    print(f"Number of Jobs:", file=file)
    print(PROBLEM.nJobs, file=file)
    print(f"Number of Machines:", file=file)
    print(PROBLEM.nMachines, file=file)
    print(f"Number of Tasks:", file=file)
    print(PROBLEM.nTasks, file=file)
    print(f"Number of Individuals:", file=file)
    print(N_INDIVIDUALS, file=file)
    print(f"Number of Iterations:", file=file)
    print(nIterations, file=file)
    print(f"Mutation Probability:", file=file)
    print(PROBLEM.mutationProb, file=file)
    print(f"Threshold Generations:", file=file)
    print(PROBLEM.thresholdGenetic, file=file)
    print(f"CrossOver Type:", file=file)
    print({"JOX" if xover == 0 else "PPX" if xover == 1 else "GPMX" if xover == 2 else "GOX"}, file=file)
    print(f"Mutation Type:", file=file)
    print({"INS" if mutType == 0 else "SWAP" if mutType == 1 else "INV"}, file=file)
    print(f"Mode:", file=file)
    print(mode, file=file)
    print(f"Factor:", file=file)
    print(factor, file=file)



###################
###  ALGORITHM  ###
###################

# This is the best individual among the best individuals from each iteration
bestOfTheBests = None

for a in range(nIterations):
    currentGeneration = [] # Store the current generation of individuals
    nextGeneration = [] # Store the next generation of individuals
    fitnessEvolPlot = [] # Store the fitness evolution of the best individual in the generation
    
    # Starts clock on this iteration
    initIter = time.time()

    # 1st -> Create initial pairs of individuals

    for i in range(N_INDIVIDUALS//2):
        
        family = [genIndividual(PROBLEM), genIndividual(PROBLEM)]
        bestInGen = family[0]
        currentGeneration.append(family)

    # Counter for the threshold for the algorithm to stop
    nGenWithoutImprovement = 0
    gen = 0 # Generation counter
    
    # Start genetic algorithm and stop when there is no improvement in whatever the mutation_prob file states generations
    while(nGenWithoutImprovement < PROBLEM.thresholdGenetic):
        print("Generation " + str(gen) + " in progress...")
        lastBest = bestInGen
        # 2nd -> Create children and evaluate
        for family in currentGeneration:
            child1, child2 = family[0].merge(family[1], PROBLEM, xover, mutType) # Merge the two parents to create two children
            family.append(child1)
            family.append(child2)
            best = getBestTwo(family, mode, factor, bestInGen) # Minimize by tardiness
            
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

    # Save best individual obtained by tardiness and energy cost from this generation
        fitnessEvolPlot.append(bestInGen.fitness)
        
    # Stops the clock for this iteration
    endIter = time.time()
    totalExecutionTime += (endIter - initIter) # Add to the total time
    # Save total number of generations
    N_GENERATIONS = gen
    
    # Save the list of fitness evolution of the best individual in each generation

    path = os.path.join(folder+r"/graphic", f"plot_{a}_result_{iLabel}.pkl")
    with open(path, 'wb') as file:
        pickle.dump(fitnessEvolPlot, file)

    # Best individual data    
    best = bestInGen
    
    # If the best of this generation is better than the best registered for this instance 
    # or the latter is None, update
    if bestOfTheBests is None or best.isBetter(bestOfTheBests, mode, factor):
        bestOfTheBests = best

    # Add the best candidate to the rest of best 
    # candidates of other iterations to serialize them all together later
    bests.append(best)
    
    # Recording of information regarding this iteration, saved in the "result" folder
    path = os.path.join(folder+r"/text", f"result_{iLabel}.txt")
    with open(path, 'a') as file: 
        print(f"\nITERATION {a+1}\n", file=file)
        print("BEST:", file=file)
        print(best, file=file)
        print(best.schedule.startTimeTasks, file=file)
        print(best.schedule.endTimeTasks, file=file)
        print("Tardiness: " + str(best.fitness[0]), file=file)
        print("Energy Consumption: " + str(best.fitness[1]), file=file)
        print("Number of generations: " + str(N_GENERATIONS), file=file)
        print("Calculation time of this iteration (s): " + str(endIter - initIter), file=file)
        print("\n\n", file=file)
        
best = bestOfTheBests
# Register the best out of the best individuals for each of the iterations
path = os.path.join(folder+r"/text", f"result_{iLabel}.txt")
with open(path, 'a') as file: 
    print(f"\nSUMMARY\n\n", file=file)
    print("GLOBAL BEST:", file=file)        
    print(best, file=file)
    print(best.schedule.startTimeTasks, file=file)
    print(best.schedule.endTimeTasks, file=file)
    print("Tardiness: " + str(best.fitness[0]), file=file)
    print("Energy Consumption: " + str(best.fitness[1]), file=file)
    print("\n\nTotal execution time (s)", file=file)
    print(totalExecutionTime, file=file)

bests.append(best) # Add the best individual to the list of best individuals
# Save the best individuals in a pickle file
path = os.path.join(folder+r"/pickle", f"result_{iLabel}.pkl")
with open(path, 'wb') as file: 
    pickle.dump(bests, file)

print("Execution time (s)")
print(totalExecutionTime)

"""
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

child1 = parent1.JOXCrossover(parent2, PROBLEM)
print("\nChild 1")
print(child1)
print("Fitness: " + str(child1.fitness))
print("DueDates: " + str(child1.tardiness))
print("Energy Consumption: " + str(child1.energyCost))
child2 = parent2.JOXCrossover(parent1, PROBLEM)
while child2.tasksPermutation == child1.tasksPermutation:
    child2 = parent2.JOXCrossover(parent1, PROBLEM)
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
        











