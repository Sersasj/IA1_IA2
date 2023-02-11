import csv
from natsort import natsort_keygen

import pandas as pd

"""
Sort Inicial
# Load the csv file into a Pandas DataFrame
df = pd.read_csv('dataset/brasileirao.csv')

# Sort the data by year and position
df.sort_values(by= 'position', key=natsort_keygen())

# Reset the index of the DataFrame
df.reset_index(drop=True, inplace=True)

# Save the sorted data back to a csv file
df.to_csv('file_sorted.csv', index=False)

"""
# Load data from csv file into a pandas dataframe
df = pd.read_csv("file_sorted.csv")

# Sort the data by year and position

# Add a new column to categorize each team as either top 4, bottom 4, or other
df["category"] = "other"
df.loc[df["position"] <= 4, "category"] = "top 4"
df.loc[df["position"] >= df.groupby("year")["position"].transform("count") - 3, "category"] = "bottom 4"

# Group the data by year and category and calculate the mean values for each group
mean_data = df.groupby(["year", "category"]).mean()
mean_data = mean_data.iloc[9:]

mean_data = df.groupby(["category" ]).mean()

mean_data.to_csv('mean_dataaaa_.csv', index=False)

