import cityflow
import re
import numpy as np 
from scipy import optimize
import mlrose

from simulate import simulate


def main():
    time_values = np.array([2,0])

    avg = simulate(time_values, shouldSave=True)
    
    print("done! saved replays")


main()