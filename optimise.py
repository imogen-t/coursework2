# %%
import csv

# %%
# Import data

# abnormal points
with open('lin-prog-inputs.csv', newline='') as f:
    reader = csv.reader(f)
    abnormal_curves = list(reader)

with open('user1-data.csv', newline='') as f:
    reader = csv.reader(f)
    user1 = list(reader)

with open('user2-data.csv', newline='') as f:
    reader = csv.reader(f)
    user2 = list(reader)

with open('user3-data.csv', newline='') as f:
    reader = csv.reader(f)
    user3 = list(reader)

with open('user4-data.csv', newline='') as f:
    reader = csv.reader(f)
    user4 = list(reader)

with open('user5-data.csv', newline='') as f:
    reader = csv.reader(f)
    user5 = list(reader)

users = [user1, user2, user3, user4, user5]

# %%
'''
For each pricing curve:
    For for each device:
        acceptable window = (earliest on, latest on)
        possible prices = trim price curve to this window
        h = number of hours device must be on for

        sort possible prices zipped with their indexes
        select first h elements of the sorted prices
        the zip pair values give the optimal times for that device
'''

# %%
# Sort times by increasing price with their indexes

pricesA = [(idx, item) for idx,item in enumerate(abnormal_curves[0])]
pricesB = [(idx, item) for idx,item in enumerate(abnormal_curves[1])]
pricesC = [(idx, item) for idx,item in enumerate(abnormal_curves[2])]

priceCurves = [pricesA, pricesB, pricesC]

# %%
# select lowest 

# note: only pass a copy of the actual price curve to this function!
# maxPerHour is always 1 for all users, so this is a constant and not read by the data
def findBestTimes(priceCurve, earliest, latest, demand):
    earliest = int(earliest)
    latest = int(latest)
    demand = int(demand)
    demand_total = 0
    optimalTimes = []
    # remove all values outside of acceptable region
    priceCurve = priceCurve[earliest:latest]
    # sort list by energy cost
    priceCurve = sorted(priceCurve, key= lambda x : x[1])

    # take best`demand` times to suit consumer needs
    optimalTimes = priceCurve[0:int(demand)]
    # return times with lowest cost, sorted by chronological hour

    return sorted([i[0] for i in optimalTimes])
# %%
# user 1, price curve a
def optimiseTimes_1curve(priceCurve, user):
    optimal = []
    for device in user:
        curve_copy = priceCurve.copy()
        opTimes = findBestTimes(curve_copy, device[0], device[1], device[3]) # max per hour is a constant
        optimal.append(opTimes)
    return optimal

def optimiseTimes_allCurves(curves, user, index):
    optimal = []
    for curve in curves:
        o = optimiseTimes_1curve(curve, user)
        optimal.append(o)
    filename = "user" + str(index) + "-optimalTimes.csv"
    write_csv(filename, optimal)
    return optimal

user1_optimised = optimiseTimes_allCurves(priceCurves, user1,1)
user2_optimised = optimiseTimes_allCurves(priceCurves, user2,2)
user3_optimised = optimiseTimes_allCurves(priceCurves, user3,3)
user4_optimised = optimiseTimes_allCurves(priceCurves, user4,4)
user5_optimised = optimiseTimes_allCurves(priceCurves, user5,5)
# %%
# write outputs to csv

def write_csv(filename, data):
    file = open(filename, 'w', newline ='') 
    with file:     
        write = csv.writer(file) 
        write.writerows(data) 


# %%
