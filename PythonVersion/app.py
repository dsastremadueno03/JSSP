import random

# INITIAL DATA
# Times for each operation in each machine (m,o)
# -1 indicates that the operation is not possible in that machine
times = [
    [2, 3, -1, 7, 2, 3, 2],
    [-1, 2, 3, 5, 8, -1, 1],
]

# Operations to do (each operation belongs to a job)
operations = [[1, 2, 3], [4, 5], [6, 7]]

#FUNCTIONS
# Returns the number of operations in total
def numOp():
    i = 0
    for job in operations:
        for operation in job:
            i+=1
    return i

# Returns a randomly-generated parent
def generateParent():
    size = numOp()
    parent = []
    parentOperations = []
    for job in operations:
            parentOperations.append(job.copy())
    for i in range(size):
        # Select a random job
        job = random.randint(0, len(parentOperations)-1)
        while (job == None or len(parentOperations[job]) == 0):
            job = random.randint(0, len(parentOperations)-1)
        # Select a random operation and machine
        op = parentOperations[job][0]
        parentOperations[job].remove(op)
        machine = random.randint(0, len(times)-1)
        parent.append([machine, op])
    if checkSchedule(parent):
        return parent
    else:
        return generateParent()

# Calculates the time the shcedule takes [FOR NOW LINEAR]
# TO DO: IMPLEMENT PARALELL OPERATIONS
def calcTime(schedule):
    scheduleTime = 0
    for i in range(len(schedule)):
        machine = schedule[i][0]
        operation = schedule[i][1]
        scheduleTime += times[machine][operation-1]
    return scheduleTime

# Checks if the schedule is valid
def checkSchedule(schedule):
    done = []
    # Check if the schedule exists
    if schedule == None:
        return False
    # Check if the schedule has the correct number of operations
    if len(schedule) != numOp():
        return False
    # Check if the order of operations is possible
    for op in schedule:
        # Check if the operation is not repeated
        if op[1] in done:
            return False
        done.append(op[1])
        isInJob = []
        # If the operation is not possible in the machine
        if times[op[0]][op[1]-1] == -1:
            return False
        # If the job has previous operations that are not done
        for job in operations:
            if op[1] in job:
                isInJob = job
            for operation in isInJob:
                if operation not in done:
                    return False
                if operation == op[1]:
                    break
    return True

# Returns a child from two parents
def produceChild(parent1, parent2):
    size = numOp()
    child = []
    for i in range(size):
        if random.randint(0, 1) == 0:
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    if checkSchedule(child):
        return child
    else:
        return produceChild(parent1, parent2)
        

# MAIN

tree = []

parent1 = generateParent()
print("parent 1: ")
print(parent1)
print("time: ")
print(calcTime(parent1))
tree.append(parent1)
parent2 = generateParent()
print("parent 2: ")
print(parent2)
print("time: ")
print(calcTime(parent2))
tree.append(parent2)
child1 = produceChild(parent1, parent2)
print("child 1: ")
print(child1)
print("time: ")
print(calcTime(child1))
tree.append(child1)
child2 = produceChild(parent1, parent2)
while (child2 == child1):
    child2 = produceChild(parent1, parent2)
print("child 2: ")
print(child2)
print("time: ")
print(calcTime(child2))
tree.append(child2)

    
        
        
    










