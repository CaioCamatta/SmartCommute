import cityflow
import re
import numpy as np 
from scipy import optimize
import mlrose


STEPS = 500

def trackTotal(dict, totals):
    for key in dict:
        if key not in totals:
            totals[key] = dict[key]
        else:
            totals[key] += dict[key]


def calculateAverages(totals, averages, count):
    for key in totals:
        averages[key] = totals[key] / count

def calculateTotalAverage(averages):
    c = 0
    t= 0 
    for key in averages:
        c += 1
        t += averages[key]

    return t / c


# -> go through the whole file, replace each instance of time with a value from our array
def create_file(time_values):

    # start

    # house keeping, ensure # of provided time values == the number of occurences of time in our list


    count = 0
    with open("./configs/roadnet.json", "rt") as fin:

        with open("./configs/edited_roadnet.json", "wt") as fout:
            for line in fin:
                if (re.search('"time": \d+', line)):
                    fout.write('"time": ' + str(time_values[count]) + ",")
                    count += 1
                else:
                    fout.write(line)



def simulate(time_values):
    count = 0
    totals = {}
    averages = {}

    # expecting time _values tp be 2 long
    time_values = time_values.tolist() * 20

    
    print("Simulating with:")
    print(time_values)
    
    create_file(time_values)
    

    eng = cityflow.Engine("./configs/config.json", thread_num=1)
    for x in range(STEPS):
        if (x % 100 == 0):
            print("step: " + str(x))

        eng.next_step()
        trackTotal(eng.get_lane_waiting_vehicle_count(), totals)
        count += 1

    calculateAverages(totals, averages, count)

    total_avg_time =  calculateTotalAverage(averages)
    print("calculated total avg time: " + str(total_avg_time))
    return total_avg_time


def main():
    # try mlrose shit 

    fitness_cust = mlrose.CustomFitness(simulate)

    problem = mlrose.DiscreteOpt(fitness_fn=fitness_cust, maximize=False, length=2, max_val = 50)


    schedule = mlrose.ExpDecay()
    
    init_state = np.array([28,7])

    best_time_values, best_avg_time = mlrose.simulated_annealing(problem, schedule = schedule,
                                                      max_attempts = 10, max_iters = 1000,
                                                      init_state = init_state, random_state = 1)


    print("Best time values:")
    print(best_time_values)

    print("Best avg time:")
    print(best_avg_time)


main()
