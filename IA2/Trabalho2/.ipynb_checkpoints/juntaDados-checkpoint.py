# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 09:58:28 2023

@author: sergi
"""

import pandas as pd
import matplotlib.pyplot as plt

# Read the first CSV file
df = pd.read_csv('train.csv')



# Create a scatter plot of v2a1 vs. target
df.plot(kind='scatter', x='Target', y='v2a1')
#df = df.dropna(subset=['v2a1'])

# Add axis labels and a title to the plot
plt.xlabel('Target')
plt.ylabel('v2a1')
plt.title('Scatter Plot of v2a1 vs. Target')

# Show the plot
plt.show()