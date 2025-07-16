# JSSP

This is part of my final thesis project for the Computer Engineering bachelor's degree from the University of Oviedo. 

The code contains a genetic algorithm, using parameter files to set its behavior.

# How to execute the algorithm

Run the app.py using two parameters passed via console: app.py <instance_number> <parameter_file_number>

A result file will be generated, containing three files: 
- Graphics file stores the evolution plot for each execution.
- Pickle file has a .pkl that contains the best individual from each execution.
- Text file contains a .txt that has the information from the best individuals written.

# How to read pickle

Use the ReadPickle class to generate the evolution plot or the Gantt chart. *The file to be displayed must be moved to a file called results inside PythonVersion.*
