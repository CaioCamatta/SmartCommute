import cityflow
import re
import numpy as np 
from scipy import optimize
import mlrose

from simulate import simulate

def main():

    # mlrose  

    fitness_cust = mlrose.CustomFitness(simulate)

    problem = mlrose.DiscreteOpt(fitness_fn=fitness_cust, maximize=False, length=2, max_val = 30)


    schedule = mlrose.ExpDecay()
    
    init_state = np.array([28,7])

    best_time_values, best_avg_time = mlrose.simulated_annealing(problem, schedule = schedule,
                                                      max_attempts = 10, max_iters = 100,
                                                      init_state = init_state, random_state = 1)

    print("Best time values:")
    print(best_time_values)

    print("Best avg time:")
    print(best_avg_time)

main()