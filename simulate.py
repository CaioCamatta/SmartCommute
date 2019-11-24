import cityflow
import re
import numpy as np 
from scipy import optimize
import mlrose
import gc


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

    count = 0
    with open("./configs/roadnet.json", "rt") as fin:
        with open("./configs/edited_roadnet.json", "wt") as fout:
            for line in fin:
                if (re.search('"time": \d+', line)):
                    fout.write('"time": ' + str(time_values[count]) + ",")
                    count += 1
                else:
                    fout.write(line)



def simulate(time_values, shouldSave=False):
    count = 0
    totals = {}
    averages = {}

    #expecting time _values tp be 2 long
    print(time_values)
    time_values = time_values.tolist()

    print(time_values)  
    time_values = time_values* 20            

    
    print("Simulating with:")
    print(time_values)
    
    create_file(time_values)
    
    eng = None
    if (shouldSave):
         eng = cityflow.Engine("./configs/config.json", thread_num=1)
    else:
        eng = cityflow.Engine("./configs/config_no_save.json", thread_num=1)
   
    for x in range(STEPS):
        if (x % 100 == 0):
            print("step: " + str(x))

        eng.next_step()
        trackTotal(eng.get_lane_waiting_vehicle_count(), totals)
        count += 1

    calculateAverages(totals, averages, count)

    total_avg_time =  calculateTotalAverage(averages)
    print("calculated total avg time. " + str(total_avg_time))
    
    return total_avg_time