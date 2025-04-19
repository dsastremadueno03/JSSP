from schedule import Schedule
from problem import Problem
import random
import numpy as np # Epsilon


class Individual:

    def __init__(self, taskPermutation, machinePermutation, idPermutation):
        self.tasksPermutation = taskPermutation # Stores the tasks (as jobs) in the order they are done
        self.machinePermutation = machinePermutation # Stores the machine in which the task is done
        self.idPermutation = idPermutation # Stores the id of the tasks in the whole problem
        self.tardiness = []
        self.energyCost = 0
        self.fitness = []
        self.schedule = None

    def __str__(self):
        return str(self.tasksPermutation) + "\n" + str(self.machinePermutation)
    
    # Equal operator
    def __eq__(self, value):
        EPSILON = np.finfo(float).eps
        return (abs(self.fitness[0] - value.fitness[0]) < EPSILON) and (abs(self.fitness[1] - value.fitness[1]) < EPSILON)
    
    
    """
    
    # Less than operator
    # 1. Tardiness
    # 2. Energy cost (If tardiness is the same)
    def __lt__(self, value):
        if self.fitness[0] < value.fitness[0]:
            return True
        elif self.fitness[0] == value.fitness[0]:
            return self.fitness[1] < value.fitness[1]
        return False
    
    # Greater than operator
    # 1. Tardiness
    # 2. Energy cost (If tardiness is the same)
    def __gt__(self, value):
        if self.fitness[0] > value.fitness[0]:
            return True
        elif self.fitness[0] == value.fitness[0]:
            return self.fitness[1] > value.fitness[1]
        return False
    """
    
    # Checks if the individual is better than another one
    # mode = 0 -> Minimize
    # mode = 1 -> Maximize
    # factor = 0 -> Tardiness
    # factor = 1 -> Energy cost
    def isBetter(self, other, mode, factor):
        EPSILON = np.finfo(float).eps
        if mode == 0:
            # Minimize
            if factor == 0:
                # Minimize tardiness
                if abs(self.fitness[0] - other.fitness[0]) < EPSILON:
                    return self.fitness[1] < other.fitness[1]
                elif self.fitness[0] < other.fitness[0]: 
                    return True
                return False
            else:
                # Minimize energy cost
                if abs(self.fitness[1] - other.fitness[1]) < EPSILON:
                    return self.fitness[0] < other.fitness[0]
                elif self.fitness[1] < other.fitness[1]:
                    return True
                return False
        if mode == 1:
            # Maximize
            if factor == 0:
                # Maximize tardiness
                if abs(self.fitness[0] - other.fitness[0]) < EPSILON:
                    return self.fitness[1] > other.fitness[1]
                elif self.fitness[0] > other.fitness[0]:
                    return True
                return False
            else:
                # Maximize energy cost
                if abs(self.fitness[1] - other.fitness[1]) < EPSILON:
                    return self.fitness[0] > other.fitness[0]
                elif self.fitness[1] > other.fitness[1]:
                    return True
                return False
                
        
        
    
    # Generates a schedule based on the individual
    def genSchedule(self, problem):
        if len(self.tasksPermutation) != problem.nTasks or len(self.machinePermutation) != problem.nTasks: # If individual has no data
            return None
        # Create schedule
        self.schedule = Schedule(problem.nMachines, problem.nJobs, problem.nTasks, problem.dueDates)
        # Go through the task permutation and the machine permutation
        for i in range(problem.nTasks):
            job = self.tasksPermutation[i]
            machine = self.machinePermutation[i]
            task = self.idPermutation[i]
            self.schedule.updateSchedule(job, machine, task, problem)
        #print("Schedule has been generated correctly!")
        
    # Calculates the tardiness array of the individual
    # Returns the total tardiness (sum of all tardiness)
    def updateTardiness(self, problem):
        totalTardiness = 0
        for i in range(problem.nJobs):
            late = self.schedule.endTask[i] - problem.dueDates[i] 
            if late < 0:
                self.tardiness.append(0) # Tardiness cannot be negative
            else:
                self.tardiness.append(late)
                totalTardiness += late
        return totalTardiness

    # Calculates the cost of the active energy of the individual
    def calcActiveEnergyPrice(self, problem):
        actEnergyPrice = 0
        for i in range(problem.nTasks):
            machine = self.machinePermutation[i]
            task = self.idPermutation[i]
            # Energy consumed
            consumption = problem.getData(machine, task)[1] # Access to energy cost of doing the task in a specific machine
            # Time of use
            startTime = self.schedule.startTimeTasks[i] 
            endTime = self.schedule.endTimeTasks[i] 
            # Calculates with the range of time in the schedule the price of the active energy consumed
            for j in range(startTime, endTime): 
                actEnergyPrice += problem.energyPrices[j%(60*24)] * consumption # Multiply minute price by the amount of energy consumed 
        # Returns the price of the active energy of the individual
        return actEnergyPrice
        
        # ASUMING: 
        # - Passive energy starts when first use of machine. 
        # - Passive energy ends when machine finishes.
        # - Passive energy is independent of active energy.
        
        # Calculates the cost of passive energy of the individual
    def calcPassiveEnergyPrice(self, problem):
        pasEnergyPrice = 0
        # For every machine, get its functional time to get the prices 
        # and multiply it by the machine passive energy consumption
        for i in range(problem.nMachines):
            for j in range(self.schedule.startMachine[i], self.schedule.endMachine[i]):
                pasEnergyPrice += problem.energyPrices[j%(60*24)] * problem.passiveEnergy[i]
        return pasEnergyPrice
         
    # Calculates the energy consumption     
    def updateTotalEnergyConsumptionPrice(self, problem):
        actEnergyPrice = self.calcActiveEnergyPrice(problem)
        pasEnergyPrice = self.calcPassiveEnergyPrice(problem)
        self.energyCost = actEnergyPrice + pasEnergyPrice
        return self.energyCost
        
    # Evaluates the tardiness, energy consumption and fitness of the individual
    def evaluate(self, problem):
        # Evaluates the tardiness of jobs
        totalTardiness = self.updateTardiness(problem)
        # Evaluates the total energy consumption
        totalEnergyCost = self.updateTotalEnergyConsumptionPrice(problem)
        # Calculates fitness (using comparison function)
        self.fitness = [totalTardiness, totalEnergyCost] # Fitness is composed of the tardiness and the energy cost (Multiobjective)
        
    # Makes the child mutate (move one gene out of order)
    def mutate(child):
        #print("Mutates: ")
        #print(child)
        gene = random.randint(0, len(child.tasksPermutation)-1)
        # Check that it is in range (does not alter the order of priority)
        job = child.tasksPermutation[gene]
        # Limit of changing positions
        limitMin = 0
        limitMax = gene
        for i in range(gene+1):
            if child.tasksPermutation[i] == job:
                limitMin = i
        for i in range(gene+1):
            if (i+gene < len(child.tasksPermutation)) and (child.tasksPermutation[i+gene] == job):
                limitMax = i+gene
                break
            
            
        moveTo = random.randint(limitMin, limitMax)
        child.tasksPermutation.insert(moveTo, child.tasksPermutation.pop(gene))
        child.machinePermutation.insert(moveTo, child.machinePermutation.pop(gene))
        child.idPermutation.insert(moveTo, child.idPermutation.pop(gene))
        
        #print("mutated:")
        #print(child)
            
    # Follows a job order crossover where self takes half or their jobs and the other half 
    # from the second parent 
    def JOXCrossover(self, individual2, problem):
        # Prepare matrices to save data
        newTasks = []
        newMachines = []
        newIds = []
        for i in range(problem.nTasks):
            newTasks.append(-1)
            newMachines.append(-1)
            newIds.append(-1)
        
            
        # Select which jobs to take from self
        jobsForSelf = [] # Stores the jobs that should be copied from self
        jobsForSecond = [] # Stores the indexes of the jobs taken from individual2
        for i in range(problem.nJobs//2): # Half of the jobs from self
            # Select a random job from self
            job = random.randint(0, problem.nJobs-1)
            # Check that it is not already in the list of jobs for self
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
                newIds[i] = self.idPermutation[i]
        # Next, we complete the array with those from the second parent
        j = 0 # index for second parent
        for i in range(problem.nTasks):
            if newTasks[i] == -1:
                newTasks[i] = individual2.tasksPermutation[jobsForSecond[j]]
                newMachines[i] = individual2.machinePermutation[jobsForSecond[j]]
                newIds[i] = individual2.idPermutation[jobsForSecond[j]]
                j += 1
            
        child = Individual(newTasks, newMachines, newIds)
            
        return child
    
    # Follows a Precedent Preservative Crossover, which uses a mask to select which jobs 
    # to take from each parent and which to take from the other parent
    # The mask is a binary matrix that indicates which jobs to take from each parent
    def PPXCrossover(self, individual2, problem, oldMask):
        # Prepare data structures
        mask = []
        # Copy the parent1 and parent2
        parent1 = Individual(self.tasksPermutation.copy(), self.machinePermutation.copy(), self.idPermutation.copy()) # Copy of the parent1
        parent2 = Individual(individual2.tasksPermutation.copy(), individual2.machinePermutation.copy(), individual2.idPermutation.copy()) # Copy of the parent2
        # Create the child data structures
        newTasks = []
        newMachines = []
        newIds = []
        
        #print("inicio")
        #print(len(parent1.tasksPermutation))
        #print(len(parent1.machinePermutation))
        #print(len(parent1.idPermutation))
        #print(len(parent2.tasksPermutation))
        #print(len(parent2.machinePermutation))
        #print(len(parent2.idPermutation))
        
        
        # Create a mask of size nTasks
        if oldMask == None:
            for i in range(problem.nTasks):
                mask.append(random.randint(0, 1))
        else:
            mask = oldMask
                
        # Create the children
        for i in range(problem.nTasks):
            # If the mask is 0, we take the job from parent1
            if mask[i] == 0:
                id = parent1.idPermutation.pop(0) # Take the job from parent1
                newIds.append(id) # Add the job to the child
                newTasks.append(parent1.tasksPermutation.pop(0)) # Take the job from parent1
                newMachines.append(parent1.machinePermutation.pop(0)) # Take the job from parent1
                index = parent2.idPermutation.index(id) # Get the index of the task in parent2
                # Cross out (delete) the gen from parent2
                parent2.tasksPermutation.pop(index)
                parent2.machinePermutation.pop(index)
                parent2.idPermutation.pop(index)
            
            # If the mask is 1, we take the job from parent2
            elif mask[i] == 1:
                id = parent2.idPermutation.pop(0) # Take the job from parent2
                newIds.append(id) # Add the job to the child
                newTasks.append(parent2.tasksPermutation.pop(0)) # Take the job from parent2
                newMachines.append(parent2.machinePermutation.pop(0)) # Take the job from parent2
                index = parent1.idPermutation.index(id) # Get the index of the task in parent1
                # Cross out (delete) the gen from parent1
                parent1.tasksPermutation.pop(index)
                parent1.machinePermutation.pop(index)
                parent1.idPermutation.pop(index)
                
            #print("Parent1:")
            #print(len(parent1.tasksPermutation))
            #print(len(parent1.machinePermutation))
            #print(len(parent1.idPermutation))
            #print("Parent2:")
            #print(len(parent2.tasksPermutation))
            #print(len(parent2.machinePermutation))
            #print(len(parent2.idPermutation))
        
        child = Individual(newTasks, newMachines, newIds) # Create the child
        return child, mask # Return the child and the mask to do the crossover again
        
    # Defines the merge function, which merges two individuals into one
    # Creates two children from two parents
    # It defines the type of crossover to be used
    # If PPX is selected, it uses the mask to select which jobs to take from each parent
    # Type 0 -> JOX crossover (job order crossover)
    # Type 1 -> PPX crossover (precedent preservative crossover)
    def merge(self, individual2, problem, type):
        
        child1 = None
        child2 = None
        
        # Select the crossover type
        if type == 0: # JOX crossover
            child1 = self.JOXCrossover(individual2, problem)
            child2 = individual2.JOXCrossover(self, problem)
    
        elif type == 1: # PPX crossover
            child1, mask = self.PPXCrossover(individual2, problem, None)
            #print(len(self.tasksPermutation))
            #print(len(individual2.tasksPermutation))
            child2, mask = individual2.PPXCrossover(self, problem, mask)
        
        # Should it mutate?
        if random.randint(1, 100) <= problem.mutationProb:
            Individual.mutate(child1)
        child1.genSchedule(problem)
        child1.evaluate(problem)
        
        # Should it mutate?
        if random.randint(1, 100) <= problem.mutationProb:
            Individual.mutate(child2)
        child2.genSchedule(problem)
        child2.evaluate(problem)
        
        return child1, child2
        