# Import the necessary libraries
import matplotlib.pyplot as plt
import pandas as pd
# we need to tell the lib to use an alternative GTK, thisis the hacky way to do so,
# non-hacky way to do so is:
#   export MPLBACKEND=TkAgg
import matplotlib as mpl
mpl.use("TkAgg")

# Initialize Figure and Axes object
fig, ax = plt.subplots()

# Load in data
tips = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv")

# Create violinplot
ax.violinplot(tips["total_bill"], vert=False)

# Show the plot
plt.show()