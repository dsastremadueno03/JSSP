from problem import Problem
import ast # Automatic conversion of data
import glob # For the path of the instance file

class InstanceReader:

    def __init__(self, pathIntances, pathPreparedJobs, pathTOUPrices, pathPassiveEnergy, pathMutationProb):
        self.problem = Problem([], 0, 0, 0, [], [], [], [], 0, 0, 0) # Initialize the problem
        self.pathIntances = pathIntances
        self.pathPreparedJobs = pathPreparedJobs
        self.pathTOUPrices = pathTOUPrices
        self.pathPassiveEnergy = pathPassiveEnergy
        self.pathMutationProb = pathMutationProb
        
    # Read the instance file and return the data
    # DATA RETRIEVED:
    # nJobs
    # nMachines
    # nTasks
    # jobTasks
    def readInstance(self):
        data = []
        f = open(glob.glob(self.pathIntances)[0], 'r')
        lines = [line.strip() for line in f.readlines()] # Read all lines and remove the \n
        f.close()
        for line in lines:
            data.append(line.split(" ")) # Get the values separated
        return data
    
    # Read the prepared jobs file and return the data
    # DATA RETRIEVED:
    # dueDates
    # tasksMachines
    def readPreparedJobs(self):
        f = open(self.pathPreparedJobs, 'r')
        data = ast.literal_eval(f.readline().strip()) # Read the array and automatically convert it 
        f.close()
        return data
    
    # Read the TOU prices file and return the data
    # DATA RETRIEVED:
    # energyPrices
    def readTOUPrices(self):
        f = open(self.pathTOUPrices, 'r')
        lines = [line.strip() for line in f.readlines()] # Read all lines and remove the \n
        f.close()
        return lines
    
    # Read the passive energy file and return the data
    # DATA RETRIEVED:
    # passiveEnergy
    def readPassiveEnergy(self):
        f = open(self.pathPassiveEnergy, 'r')
        data = ast.literal_eval(f.readline().strip()) # Read the array and automatically convert it
        f.close()
        return data
    
    # Read the mutation probability file and return the data
    # DATA RETRIEVED:
    # mutationProb
    # thresholdGenetic
    # nIndividuals
    def readMutationProb(self):
        f = open(self.pathMutationProb, 'r')
        data = []
        f.readline().strip() # Skip first line (only info)
        for i in range(6):
            data.append(int(f.readline().strip())) # Read the values and convert it to int to append it in data
        f.close()
        return data
    
    # Transform the instance data and assign it to the problem
    def transformInstanceData(self, data):
        self.problem.nJobs = int(data[0][0])
        self.problem.nMachines = int(data[0][1])
        # Initialize the taskMachine matrix
        for i in range(self.problem.nMachines):
            self.problem.tasksMachines.append([])
        
        # i starts at 1 because the first line is the number of jobs and machines
        for i in range(self.problem.nJobs):
            tasksInJob = int(data[i+1][0])
            self.problem.nTasks += tasksInJob # Sum the number of tasks for job i
            self.problem.jobTasks.append(tasksInJob) # Append the number of tasks for job i
            
            """
            # j starts at 1 because the first value is the number of tasks for job i
            j = 0
            while(j < len(data[i+1])-1):
                machinesInTask = int(data[i+1][j+1])
                setMachinesPossible = []
                # k starts at 1 because the first value is the number of machines for task j
                # Saves the duration in the matrix of tasksMachines for this task
                for k in range(0, machinesInTask*2, 2):
                    machine = int(data[i+1][j+1+k+1])
                    duration = int(data[i+1][j+1+k+2])
                    self.problem.tasksMachines[machine-1].append([duration, 0]) # Append the duration for the task for the specific machine
                    setMachinesPossible.append(machine-1) # Machine is possible for this task
                
                    
                # Fill the rest of the machines with -1
                if len(setMachinesPossible) < self.problem.nMachines:
                    for k in range(self.problem.nMachines):
                        if k not in setMachinesPossible:
                            self.problem.tasksMachines[k].append([-1, -1])
                # Increase j by the number of machines in the task
                j += machinesInTask * 2 + 1
                
        for i in range(self.problem.nMachines):
            print(self.problem.tasksMachines[i])
                    """
    
    # Transform the prepared jobs data and assign it to the problem   
    def transformPreparedJobsData(self, data):
        for job in data:
            self.problem.dueDates.append(job[0][0][4]) # Append the due date for the job
            for task in job:
                setPossibleMachines = []
                for machine in task:
                        machineId = machine[0]
                        if machineId not in setPossibleMachines: # There are multiple options in the input file (just take first one)
                            duration = machine[1]
                            energy = machine[2] / 100 # Values were converted to a higher scale in the input file
                            param = [duration, energy]
                            self.problem.tasksMachines[machineId].append(param)
                            setPossibleMachines.append(machineId)
                # Fill the rest of the machines with -1
                if len(setPossibleMachines) < self.problem.nMachines:
                    for k in range(self.problem.nMachines):
                        if k not in setPossibleMachines:
                            self.problem.tasksMachines[k].append([-1, -1])
                    
        
    # Transform the TOU prices data and assign it to the problem
    def transformTOUPricesData(self, data):
        actualData = data[196:220] # Fixed values from file format (TOU prices from hour 0 till 24)
        fixedData = []
        for value in actualData:
            fixedData.append(value.strip(','))
        finalData = []
        for i in range(len(fixedData)):
            for _ in range(60): # For each minute
                finalData.append(int(fixedData[i])/60/100.0) # Obtain decimal value (/60 for minutes, /100 for two-digit decimal value)
        self.problem.energyPrices = finalData
        
    # Transform the passive energy data and assign it to the problem
    def transformPassiveEnergyData(self, data):
        passiveEnergy = []
        for i in range(len(data)):
            passiveEnergy.append(data[i]/100) # Values were converted to a higher scale in the input file
        self.problem.passiveEnergy = passiveEnergy
        
    # Transform the mutation probability data and assign it to the problem
    def transformMutationProbData(self, data):
        self.problem.mutationProb = data[0]
        self.problem.thresholdGenetic = data[1]
        self.problem.nIndividual = data[2]
        return data[3], data[4], data[5] # Returns the number of iterations per instance to the main directly
    
print("TEST")
instanceReader = InstanceReader(r"instances_new/instances_new/flexible_jobshop_7_2jobs_3machines_flex_high_squared.data", r"preparedjobs_new/preparedjobs_new/flexible_jobshop_7_2jobs_3machines_flex_high_squared_JOBS.data", r"TOU prices/TOU prices/TOU_prices_v1", r"passive_energy/passive_energy_3machines.txt", r"mutation_prob.txt")

# Read and assign data retrieved to the problem
dataInstance = instanceReader.readInstance()
dataPreparedJobs = instanceReader.readPreparedJobs()
dataTOUPrices = instanceReader.readTOUPrices()
instanceReader.transformInstanceData(dataInstance)
instanceReader.transformPreparedJobsData(dataPreparedJobs)
instanceReader.transformTOUPricesData(dataTOUPrices)




        
    
