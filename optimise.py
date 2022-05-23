# %%
import csv
import matplotlib.pyplot as plt

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

def optimiseTimes_allCurvesAndUsers(curves, users):
    optimal = []
    for curve in curves:
        for user in users:
            o = optimiseTimes_1curve(curve, user)
            optimal.append(o)
    return optimal

allOptimised = optimiseTimes_allCurvesAndUsers(priceCurves, users)

# lists of users split by device times under each price curve
optimisedA = allOptimised[::3]
optimisedB = allOptimised[1::3]
optimisedC = allOptimised[2::3]
# %%
# get frequency counts for each time
concated = []
for elem in optimisedA:
    for e in elem:
        concated += e

counts = list({(x,concated.count(x)) for x in concated})

# fill in emptys
for i in range(24):
    if([item for item in counts if item[0] == i] == []):
        counts.append((i,0))

counts = sorted(counts, key= lambda x : x[0])

# %%
# plot bar chart for each time

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
times = list(zip(*counts))[0]
frequencies = list(zip(*counts))[1]
ax.bar(times, frequencies)
plt.title("Optimal Cumulative Energy Use by 5 Users with IoT Devices by Hour")
plt.xlabel("Time, in 24-hour format")
plt.ylabel("Number of IoT devices used in this hour")
plt.xticks(range(24))
plt.show()


# %%
