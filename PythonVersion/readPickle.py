import pickle # Read pickled objects
import os # Access the path
import glob # Get the general files (*)

# Unpickle individuals
individuals = []
i = 1

# Stores the individuals in the folder "results"
path = glob.glob(os.path.join("results", "*.pkl"))
for file in path:
    with open(file, 'rb') as pickled:
        bestInd = pickle.load(pickled)
        print("Individual", i)
        print(bestInd)
        i += 1
        individuals.append(bestInd)