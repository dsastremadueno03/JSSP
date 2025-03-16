from problem import Problem

class InstanceReader:

    def __init__(self, pathIntances, pathPreparedJobs, pathDeadlines, pathTOUPrices):
        self.problem = Problem([], 0, 0, 0, [], [], [], [], 0) # Initialize the problem
        self.pathIntances = pathIntances
        self.pathPreparedJobs = pathPreparedJobs
        self.pathDeadlines = pathDeadlines
        self.pathTOUPrices = pathTOUPrices
        
    # Read the instance file and return the data
    def readInstance(self):
        data = []
        f = open(self.pathIntances, 'r')
        lines = [line.strip() for line in f.readlines()] # Read all lines and remove the \n
        f.close()
        for line in lines:
            data.append(line.split(" ")) # Get the values separated
        return data
    
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
                    
                
            
        
        
        
        
    
print("Test")
instanceReader = InstanceReader(r"instances_new\instances_new\flexible_jobshop_59_10jobs_10machines_flex_high_squared.data", "", "", "")
dataInstance = instanceReader.readInstance()
instanceReader.transformInstanceData(dataInstance)
        
    
