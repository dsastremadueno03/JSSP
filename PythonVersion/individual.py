from schedule import Schedule
from problem import Problem
import random

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
        return self.fitness == value.fitness
    
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
        
    
    # Generates a schedule based on the individual
    def genSchedule(self, problem):
        if len(self.tasksPermutation) != problem.nTasks or len(self.machinePermutation) != problem.nTasks: # If individual has no data
            return None
        # Create schedule
        self.schedule = Schedule(problem.nMachines, problem.nJobs, problem.nTasks)
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
                actEnergyPrice += problem.energyPrices[j] * consumption # Multiply hour price by the amount of energy consumed 
        
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
                pasEnergyPrice += problem.energyPrices[j] * problem.passiveEnergy[i]
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
        print("Mutates: ")
        print(child)
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
        
        print("mutated:")
        print(child)
            
    # Follows a job order crossover where self takes half or their jobs and the other half from the second parent
    def merge(self, individual2, problem):
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
        
        # Should it mutate?
        if random.randint(1, 100) <= problem.mutationProb:
            Individual.mutate(child)
            
        child.genSchedule(problem)
        child.evaluate(problem)
        return child