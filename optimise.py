# %%
from scipy.optimize import linprog
import csv

# %%
# Import data

with open('lin-prog-inputs.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

# %%
# Define bounds on function

## there are 24 explanatory variables
x0_bounds = (0, None)
