import pickle # Read pickled objects
import os # Access the path
import glob # Get the general files (*)
import matplotlib.pyplot as plt # Show the result plots

# Unpickle individuals
def unpickleInd():
    bestInd = [] # List of individuals
    i = 1
    # Stores the individuals in the folder "results"
    path = glob.glob(os.path.join(r"results/pickle", "*.pkl"))
    for file in path:
        with open(file, 'rb') as pickled:
            bestInd = pickle.load(pickled)
            for ind in bestInd:
                print("Individual", i)
                print(ind)
                i += 1
    return bestInd

# Unpickle plot a
def unpicklePlots(a, b):  
    path = os.path.join(r"results/graphic/", f"plot_{a}_result_{b}.pkl")
    with open(path, 'rb') as pickled:
        fig = pickle.load(pickled)
    plt.show()
        

unpicklePlots(10, 59) # Unpickle plot 1