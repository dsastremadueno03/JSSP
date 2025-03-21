from individual import Individual
from instanceReader import InstanceReader
from problem import Problem
from schedule import Schedule
import random

instanceReader = InstanceReader(r"instances_new\instances_new\flexible_jobshop_7_2jobs_3machines_flex_high_squared.data", r"preparedjobs_new\preparedjobs_new\flexible_jobshop_7_2jobs_3machines_flex_high_squared_JOBS.data", r"TOU prices\TOU prices\TOU_prices_v1", r"passive_energy\passive_energy_3machines.txt", r"mutation_prob_genetic_parameters.txt")

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
instanceReader.transformMutationProbData(dataMutationProb)

### FOR COMPARING RESULTS ONLY
instanceReader.problem.passiveEnergy = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Creation of the problem
PROBLEM = instanceReader.problem #FINAL

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

individual = genIndividual(PROBLEM)

individual.calcActiveEnergyPrice(PROBLEM)