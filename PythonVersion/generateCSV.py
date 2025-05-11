import os # For the path of the instance files
import glob # For the path of the instance files
import csv # For the CSV file

# What data is needed to generate the CSV file?

# Columns:
# Instance,	N Jobs,	N Machines,	N Tasks, N Individuals,	N Iterations,	
# Mutation Prob., Threshold, Mode, Factor, Xover type, Mutation type,
# Factor, Iteration, Tardiness, Energy,	N Generations, Execution Time

# Updates the global data with the data of a file to be written in the CSV file
def getInstanceData(instance, data):
    newLine = [] # Stores a line of data (Only one iteration)
    infoLine = [] # Stores the parameters of the instance
    with open(instance, "r") as file:
        raw_data = file.read()
        infoLine.append(instance.split("_")[1].split(".txt")[0]) # Instance number
        # Get the numerical data from the instance file
        for line in raw_data.splitlines():
            # Get the parameters info (repeats in every row)
            if line.isdigit(): # Only happens once
                infoLine.append(line)
            elif line.startswith("{'"):# Only happens once
                infoLine.append(line.split("\'")[1])

            # Rest of info
            elif line.startswith("ITERATION "):
                for element in infoLine: # Adds the parameters of the instance to the new line
                    newLine.append(element)
                newLine.append(line.split(" ")[1])
            elif line.startswith("Tardiness"):
                newLine.append(line.split(" ")[1])
            elif line.startswith("Energy"):
                newLine.append(line.split(" ")[2])
            elif line.startswith("Number of generations:"):
                newLine.append(line.split(" ")[3])
            elif line.startswith("Calculation time"):
                newLine.append(line.split(" ")[6])
                data.append(newLine) # Adds a new line of data to the global data
                newLine = [] # Resets the newLine variable for the next iteration
                
    # Return the updated data
    return data

# Get all the instances in the folders
def getAllInstances():
    data = []
    mainFolder = fr"PythonVersion\results" # Path to the folder with the results
    instances = [] # List of all the instances
    # Get all the instance files in the folder and subfolders
    # Root is the path to the folder, dirs is the subfolders, files is the files in the folder
    for root, dirs, files in os.walk(mainFolder):
        for file in files:
            if file.endswith(".txt") and file.startswith("result_"):
                instances.append(os.path.join(root, file))

    print(instances)
    # Get the data from each instance file
    for instance in instances:
        # Update the global data with the data of each instance
        data = getInstanceData(instance, data)

    return data # Return the list of instances



# Once the global data is updated and complete, it is written in the CSV file
def generateCSV(data):
    # Get the column names
    column_names = [
        "Instance",
        "N Jobs",
        "N Machines",
        "N Tasks",
        "N Individuals",
        "N Iterations",
        "Mutation Prob.",
        "Threshold",
        "Mode",
        "Factor",
        "Xover type",
        "Mutation type",
        "Iteration",
        "Tardiness",
        "Energy",
        "N Generations",
        "Execution Time"
    ]

    # Create the CSV file
    with open("result.csv", mode = "w", newline = "") as file:
        writer = csv.writer(file)
        writer.writerow(column_names)
        print(data)
        for line in data:
            writer.writerow(line)
    print("CSV file generated successfully.")


# Call the function to generate the CSV file
generateCSV(getAllInstances()) 
            



