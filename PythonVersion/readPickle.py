import pickle # Read pickled objects
import os # Access the path
import glob # Get the general files (*)
import matplotlib.pyplot as plt # Show the result plots
from individual import Individual # Individual class
from schedule import Schedule # Schedule class



# Unpickle individuals
def unpickleInd():
    bestInd = [] # List of individuals
    i = 1
    # Stores the individuals in the folder "results"
    path = glob.glob(os.path.join(r"PythonVersion/results", "*.pkl"))
    for file in path:
        with open(file, 'rb') as pickled:
            bestInd = pickle.load(pickled)
            for ind in bestInd:
                print("Individual", i)
                print(ind)
                i += 1
    return bestInd

    
# Unpickles, as a plot, the evolution of a specific iteration
def plotEvol():
    path = glob.glob(os.path.join(r"PythonVersion/results", "*.pkl"))
    data = []
    with open(path[0], 'rb') as pickled:
        data = pickle.load(pickled)

    N_GENERATIONS = len(data) # Number of generations
    axisValue = []
    for i in range(N_GENERATIONS):
        axisValue.append(int(i+1)) # Generation number
        
    fitnessTimePlot = [] # Tardiness
    fitnessEnergyPlot = [] # Energy cost
    for i in range(N_GENERATIONS):
        fitnessTimePlot.append(data[i][0]) # Tardiness
        fitnessEnergyPlot.append(data[i][1]) # Energy cost

    fig, ax = plt.subplots(1, 2, figsize=(10, 6))
    ax[0].grid(axis='y', linestyle='--', alpha=0.7)
    ax[0].plot(axisValue, fitnessTimePlot, 'o-', linewidth=2, color='b')
    ax[0].set(xlim=(0, N_GENERATIONS+2), ylim=(0, max(fitnessTimePlot)+2))
    ax[0].set_xlabel('Generation')
    ax[0].set_ylabel('Tardiness (min)')
    ax[0].set_title('Evolution of tardiness')

    ax[1].grid(axis='y', linestyle='--', alpha=0.7)
    ax[1].plot(axisValue, fitnessEnergyPlot, 'o-', linewidth=2, color='r')
    ax[1].set(xlim=(0, N_GENERATIONS+2), ylim=(0, max(fitnessEnergyPlot)+200))
    ax[1].set_xlabel('Generation')
    ax[1].set_ylabel('Energy Cost (€)')
    ax[1].set_title('Evolution of energy cost')
    
    plt.show()

# Creates a permutation list that groups the tasks by job (keeps same index to know which job it is)
# EXAMPLE:
# taskPermutation -> [0, 1, 0, 2, 1, 2, 2]
# Result -> [0, 0, 1, 0, 1, 1, 2] (id of the tasks per job)
def groupByJob(ind):
    result = [] # Result of the grouping
    counterJobs = [] # Id of the task for each job
    for i in range(ind.schedule.nJobs):
        counterJobs.append(0)
    for i in range(ind.schedule.nTasks):
        result.append(counterJobs[ind.tasksPermutation[i]]) # Append the id of the task for each job
        counterJobs[ind.tasksPermutation[i]] += 1 # Increase the id of the task for each job
    
    return result # Return the result of the grouping

# Plot of the best individual schedule
# a -> Instance number
# b -> Iteration number  
def plotSchedule(ind):
    # Get schedule data
    data = None
    path = glob.glob(os.path.join(r"PythonVersion/results", "*.pkl"))
    with open(path[0], 'rb') as pickled:
        data = pickle.load(pickled) # data is a list of individuals  
        
    # Get individual data
    best = data[ind]
        
    # Get initial data from the top of the file (fixed positions)
    nJobs = best.schedule.nJobs # Number of jobs
    nMachines = best.schedule.nMachines # Number of machines
    nTasks = best.schedule.nTasks # Number of tasks
    
    y_pos = []
    durations = []
    machine_labels = []
    tasks = []
    start_times = []
    
    # Create plot
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    colors = plt.get_cmap("tab10", nJobs)
    # Group the tasks per job
    tasksByJob = groupByJob(best)


    for i in range(nMachines):
        y_pos.append(i)

    for task in range(nTasks): # Schedule lists are already ordered
        if best.schedule.startTimeTasks[task] != -1:                
            start = best.schedule.startTimeTasks[task]
            end = best.schedule.endTimeTasks[task]
            duration = end - start

            start_times.append(start)
            durations.append(duration)
            indexMachine = best.idPermutation.index(task) # Index for the permutations
            tasks.append(f"J{best.tasksPermutation[indexMachine]}-T{tasksByJob[indexMachine]}")  # Task tag
            machine_labels.append(best.machinePermutation[indexMachine])  # Assigned machine

    for i in range(nTasks):  
        index = best.idPermutation.index(i)  
        ax.barh(machine_labels[i], durations[i], left=start_times[i], 
                    color=colors(best.tasksPermutation[index]), edgecolor="black")
            
        # Label each task in the middle of the bar
        ax.text(start_times[i] + durations[i] / 2, machine_labels[i], tasks[i], 
                va="center", ha="center", color="white", fontsize=5, fontweight="bold")
        
    # Add deadlines fro each job to plot
    for i in range(nJobs):
        ax.axvline(x=best.schedule.dueDates[i], color=colors(i), linestyle="--")
        ax.text(best.schedule.dueDates[i], 10, f"D{i}", va="bottom", ha="center", color=colors(i))

    # Setting plot info 
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Machines")

    # Ensure only the 3 machines appear on the y-axis
    ax.set_yticks(range(nMachines))  
    ax.set_yticklabels([f"M{i}" for i in range(nMachines)])

    ax.set_title("Best Found Schedule", pad=20)
    ax.grid(axis="x", linestyle="--", alpha=0.7)

    plt.show()

plotSchedule(5) # Plot the schedule generated by the best individual from the iteration indicated
#plotEvol() # Plot the evolution of the tardiness and energy cost
#unpickleInd() # Unpickle the individuals and print them
