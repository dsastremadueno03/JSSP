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
    # compType = 0 -> Lexico-graphical comparison
    # compType = 1 -> Mono comparison
    def isBetter(self, other, mode, factor, compType):
        EPSILON = np.finfo(float).eps
        # Lexico-graphical comparison
        if compType == 0:
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
                
        # Mono-objective comparison
        elif compType == 1:
            if mode == 0:
                # Minimize
                if factor == 0:
                    # Minimize tardiness
                    return self.fitness[0] < other.fitness[0]
                else:
                    # Minimize energy cost
                    return self.fitness[1] < other.fitness[1]
            if mode == 1:
                # Maximize
                if factor == 0:
                    # Maximize tardiness
                    return self.fitness[0] > other.fitness[0]
                else:
                    # Maximize energy cost
                    return self.fitness[1] > other.fitness[1]
    

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
            startTime = self.schedule.startTimeTasks[task] 
            endTime = self.schedule.endTimeTasks[task] 
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

    """
    # Check if the individual is valid
    # If the individual is not valid, repair it
    # It goes through the tasks in order of task and job, and swaps the tasks that are not in the right order
    def repair(self, problem):
        counter = 0
        for j in range(problem.nJobs): # Go through the jobs
            error = -1 # Error location
            i = 0 # Index for the tasks in the individual
            while i < problem.nTasks: # Go through the tasks in the individual
                #print("j: ", j)
                #print("i: ", i)
                #print("counter: ", counter)
                #print("error: ", error)
                if self.tasksPermutation[i] == j: # If we find the job we are in
                    if counter == self.idPermutation[i]: # If the task is in the right order
                        if error != -1: # If there was an error, swap the tasks
                            # Swap the tasks
                            tempTask = self.tasksPermutation[i]
                            tempMachine = self.machinePermutation[i]
                            tempId = self.idPermutation[i]
                            self.tasksPermutation[i] = self.tasksPermutation[error]
                            self.machinePermutation[i] = self.machinePermutation[error]
                            self.idPermutation[i] = self.idPermutation[error]
                            self.tasksPermutation[error] = tempTask
                            self.machinePermutation[error] = tempMachine
                            self.idPermutation[error] = tempId

                            i = error # Set the index to the error location
                            error = -1 # Reset the error
                            counter += 1 # Move to the next task
                        else:
                            counter += 1 # Look for the next task
                    else: 
                        if error == -1:
                            error = i
                i += 1 # Move to the next
                    
    """
    # Generate the idPermutation and machinePermutation based on the tasksPermutation
    def generateIDMachine(self, problem):
        # idPermutation
        newIds = []
        jobs = [] # Count task in real time for each job
        #Initialize to 0
        for i in range(problem.nJobs):
            jobs.append(0)
        # Create the permutation
        for job in self.tasksPermutation:
            totalJob = 0 # Id calculation
            jobs[job] += 1 # Count the number of tasks in the job in real time
            for i in range(job): # Add the number of tasks in the previous jobs
                totalJob += problem.jobTasks[i]
            totalJob += jobs[job] - 1 # Add the number of tasks in the job that are already done
            newIds.append(totalJob) # Add the id of the task in the job
        

        # machinePermutation
        newMachines = []
        for i in range(problem.nTasks):
            id = newIds[i] # Get the task index from the new idPermutation
            index = self.idPermutation.index(id) # Get the index of the task in the original idPermutation
            newMachines.append(self.machinePermutation[index]) # Get the machine of the task in the original machinePermutation
            

        # Updade the permutations
        self.idPermutation = newIds # Set the idPermutation
        self.machinePermutation = newMachines # Set the machinePermutation

        
            
        

    # Makes the child mutate (move one gene out of order)
    def mutateInsert(child):
        #print("Mutates: ")
        #print(child)
        gene = random.randint(0, len(child.tasksPermutation)-1)

        """
        # Check that it is in range (does not alter the order of priority)
        job = child.tasksPermutation[gene]
        # Limit of changing positions
        limitMin = 0
        limitMax = len(child.tasksPermutation)-1
        for i in range(gene): # Check the previous task from the same job to mark as minimum limit
            if child.tasksPermutation[i] == job:
                limitMin = i + 1

        for i in range(gene+1, len(child.tasksPermutation)): # Check the next task from the same job to mark as maximum limit
            if child.tasksPermutation[i] == job:
                limitMax = i - 1
                break
        """
        
        moveTo = random.randint(0, len(child.tasksPermutation)-1)
        while moveTo == gene: # Check that the moveTo is not the same as the gene
            moveTo = random.randint(0, len(child.tasksPermutation)-1)
        child.tasksPermutation.insert(moveTo, child.tasksPermutation.pop(gene))
        
        
    # Makes the child mutate (swaps two genes in range)
    def mutateSwap(child):
        #print("Mutates: ")
        #print(child)
        gene = random.randint(0, len(child.tasksPermutation)-1)

        """
        # Check that it is in range (does not alter the order of priority)
        job = child.tasksPermutation[gene]

        # Array to store found jobs
        foundJobs = []
        foundJobs.append(job)

        # Limit of changing positions
        limitMin = 0
        limitMax = len(child.tasksPermutation)-1

        # Minimum limit
        for i in range(gene): # Check from the start if gene is in the found jobs.
            if child.tasksPermutation[i] in foundJobs: # If already in, update minimum limit
                limitMin = i + 1
            else: # Else, append it to the found jobs
                foundJobs.append(child.tasksPermutation[i])

        # Maximum limit
        for i in range(gene+1, len(child.tasksPermutation)): # Check the next task from the same job to mark as maximum limit
            if child.tasksPermutation[i] in foundJobs: # If already in, update maximum limit and stop, since it cannot go further
                limitMax = i - 1
                break

        # Check that there is a range to swap
        if limitMin < limitMax:     
        
        """
        moveTo = random.randint(0, len(child.tasksPermutation)-1)
        while moveTo == gene: # Check that the moveTo is not the same as the gene
            moveTo = random.randint(0, len(child.tasksPermutation)-1)
            
        # Swap the genes
        taskToMove = child.tasksPermutation[moveTo]
        child.tasksPermutation[moveTo] = child.tasksPermutation[gene]
        child.tasksPermutation[gene] = taskToMove

    
    # Makes the child mutate (inverts the order of the genes in a range)
    def mutateInvert(child):
        gene = random.randint(0, len(child.tasksPermutation)-1)

        """
        # Check that it is in range (does not alter the order of priority)
        job = child.tasksPermutation[gene]

        # Array to store found jobs
        foundJobs = []
        foundJobs.append(job)

        # Limit of changing positions
        limitMin = 0
        limitMax = len(child.tasksPermutation)-1

        # Minimum limit
        for i in range(gene): # Check from the start if gene is in the found jobs.
            if child.tasksPermutation[i] in foundJobs: # If already in, update minimum limit
                limitMin = i + 1
            else: # Else, append it to the found jobs
                foundJobs.append(child.tasksPermutation[i])

        # Maximum limit
        for i in range(gene+1, len(child.tasksPermutation)): # Check the next task from the same job to mark as maximum limit
            if child.tasksPermutation[i] in foundJobs: # If already in, update maximum limit and stop, since it cannot go further
                limitMax = i - 1
                break

        # Check that there is a range to invert
        if limitMin < limitMax:
        """

        moveTo = random.randint(0, len(child.tasksPermutation)-1)
        while moveTo == gene: # Check that the moveTo is not the same as the gene
            moveTo = random.randint(0, len(child.tasksPermutation)-1)
            
        # Get the biggest and smallest of the two genes
        maxValue = max(gene, moveTo)
        minValue = min(gene, moveTo)
                
        # Invert the genes
        for i in range(abs(maxValue-minValue)//2+1):
            if minValue + i == maxValue - i: # If the two genes are the same, break
                break
            # Swap the genes
            taskToMove = child.tasksPermutation[minValue+i]
            child.tasksPermutation[minValue+i] = child.tasksPermutation[maxValue-i]
            child.tasksPermutation[maxValue-i] = taskToMove


    def mutate(child, type):
        if type == 0:
            return Individual.mutateInsert(child)
        elif type == 1:
            return Individual.mutateSwap(child)
        elif type == 2:
            return Individual.mutateInvert(child)
            
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
        
        child = Individual(newTasks, newMachines, newIds) # Create the child
        return child, mask # Return the child and the mask to do the crossover again
    
    # Follows a Generalized Partially Mapped Crossover, creating a child that inherits first
    # the genes from a specified range of the first parent and then the rest from the second parent
    # begin and end are the indexes of the range of the first parent
    def GPMXCrossover(self, individual2, problem, oldBegin, oldEnd):
        
        # Create the child data structures
        newTasks = []
        newMachines = []
        newIds = []
        
        for i in range(problem.nTasks):
            newTasks.append(-1)
            newMachines.append(-1)
            newIds.append(-1)
        
        # Range of the crossover for parent1
        begin = 0
        end = 0
        
        # Obtain the range of the crossover
        if oldBegin == None:
            begin = random.randint(0, problem.nTasks-1)
            end = random.randint(begin, problem.nTasks-1)
        else:
            begin = oldBegin
            end = oldEnd
        
        # Get the list ranged
        for i in range(begin, end+1):
            newTasks[i] = self.tasksPermutation[i]
            newMachines[i] = self.machinePermutation[i]
            newIds[i] = self.idPermutation[i]
        
        # Get the tasks from parent2 that are not in the range of parent1
        counter = 0 # Counter for the tasks in parent2
        for i in range(problem.nTasks): # Go through the permutations
            if newIds[i] == -1: # If there is no task yet in that position
                # Check that gen does not come from parent1
                if individual2.idPermutation[counter] not in newIds:
                    newTasks[i] = individual2.tasksPermutation[counter]
                    newMachines[i] = individual2.machinePermutation[counter]
                    newIds[i] = individual2.idPermutation[counter]
                    counter += 1 # Move to the next gen of parent2
                    
                # If the task is already in the child, then ignore it and move to next task
                else:
                    while individual2.idPermutation[counter] in newIds:
                        counter += 1
                    newTasks[i] = individual2.tasksPermutation[counter]
                    newMachines[i] = individual2.machinePermutation[counter]
                    newIds[i] = individual2.idPermutation[counter]
                    counter += 1
                    
        return Individual(newTasks, newMachines, newIds), begin, end # Return the child and the range of the crossover
    
    # Follows a Generalized Order Crossover, creating a child that inherits first
    # the genes from parent2 and then the rest from parent1 that are in the range
    # begin and end are the indexes of the range of the first parent
    def GOXCrossover(self, individual2, problem, oldBegin, oldEnd):
    # Create the child data structures
        rangeXover = []
        newTasks = []
        newMachines = []
        newIds = []
        
        # Range of the crossover for parent1
        begin = 0
        end = 0
        
        # Obtain the range of the crossover
        if oldBegin == None:
            begin = random.randint(0, problem.nTasks-1)
            end = random.randint(begin, problem.nTasks-1)
        else:
            begin = oldBegin
            end = oldEnd
        
        # Get the list ranged
        for i in range(begin, end+1):
            rangeXover.append(self.idPermutation[i])
        
        # While the first element of the range is not found in parent2, keep adding 
        # genes to the child that are not in the range
        counter = 0 # Counter for the tasks in parent2
        # Copy the genes from parent2 until the first gen of the range is found
        while individual2.idPermutation[counter] != rangeXover[0]: 
            if individual2.idPermutation[counter] not in rangeXover:
                newTasks.append(individual2.tasksPermutation[counter])
                newMachines.append(individual2.machinePermutation[counter])
                newIds.append(individual2.idPermutation[counter])
            counter += 1
        
        # Copy the genes from parent1 that are in the range
        for i in range(begin, end+1):
            newTasks.append(self.tasksPermutation[i])
            newMachines.append(self.machinePermutation[i])
            newIds.append(self.idPermutation[i])
        
        # Keep copying the genes from parent2 until the end of the permutation
        for i in range(counter, problem.nTasks):
            if individual2.idPermutation[i] not in rangeXover:
                newTasks.append(individual2.tasksPermutation[i])
                newMachines.append(individual2.machinePermutation[i])
                newIds.append(individual2.idPermutation[i])
        
        return Individual(newTasks, newMachines, newIds), begin, end # Return the child and the range of the crossover
    
    # Defines the merge function, which merges two individuals into one
    # Creates two children from two parents
    # It defines the type of crossover to be used
    # If PPX is selected, it uses the mask to select which jobs to take from each parent
    # Type 0 -> JOX crossover (job order crossover)
    # Type 1 -> PPX crossover (precedent preservative crossover)
    def merge(self, individual2, problem, type, mutType):
        
        child1 = None
        child2 = None
        
        # Select the crossover type
        if type == 0: # JOX crossover
            child1 = self.JOXCrossover(individual2, problem)
            child2 = individual2.JOXCrossover(self, problem)
    
        elif type == 1: # PPX crossover
            child1, mask = self.PPXCrossover(individual2, problem, None)
            child2, mask = individual2.PPXCrossover(self, problem, mask)
        
        elif type == 2: # GPMX crossover
            child1, begin, end = self.GPMXCrossover(individual2, problem, None, None)
            child2, begin, end = individual2.GPMXCrossover(self, problem, begin, end)
            
        elif type == 3: # GOX crossover
            child1, begin, end = self.GOXCrossover(individual2, problem, None, None)
            child2, begin, end = individual2.GOXCrossover(self, problem, begin, end)
        
        # Should it mutate?
        if random.randint(1, 100) <= problem.mutationProb:
            Individual.mutate(child1, mutType)
        child1.generateIDMachine(problem)
        child1.genSchedule(problem)
        child1.evaluate(problem)
        
        # Should it mutate?
        if random.randint(1, 100) <= problem.mutationProb:
            Individual.mutate(child2, mutType)
        child2.generateIDMachine(problem)
        child2.genSchedule(problem)
        child2.evaluate(problem)
        
        return child1, child2
        