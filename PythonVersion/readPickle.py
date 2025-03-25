import pickle
import os
import glob

# Unpickle individual
individuals = []

path = glob.glob(os.path.join("results", "*.pkl"))
for file in path:
    with open(file, 'rb') as pickled:
        bestInd = pickle.load(pickled)
        print(bestInd)
        individuals.append(bestInd)