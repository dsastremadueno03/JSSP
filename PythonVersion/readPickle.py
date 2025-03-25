import pickle # Read pickled objects
import os # Access the path
import glob # Get the general files (*)
import matplotlib.pyplot as plt # Show the result plots

# Unpickle individuals
def unpickleInd():
    individuals = []
    i = 1
    # Stores the individuals in the folder "results"
    path = glob.glob(os.path.join(r"results\pickle", "*.pkl"))
    for file in path:
        with open(file, 'rb') as pickled:
            bestInd = pickle.load(pickled)
            print("Individual", i)
            print(bestInd)
            i += 1
            individuals.append(bestInd)

# Unpickle plots
def unpicklePlots(a):  
    path = glob.glob(os.path.join(r"results\graphic", f"plot_result_{a}.pkl"))
    for file in path:
        with open(file, 'rb') as pickled:
            fig = pickle.load(pickled)
    plt.show()
        
unpicklePlots(10)