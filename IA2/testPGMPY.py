# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 12:25:59 2023

@author: sergi
"""

import pandas as pd
from pgmpy.models import BayesianModel
from pgmpy.estimators import MaximumLikelihoodEstimator

# Load the data into a pandas dataframe
df = pd.read_csv("mean_data.csv")

# Create a Bayesian model
model = BayesianModel([("points", "category"),
                       ("victories", "category"),
                       ("draws", "category"),
                       ("losses", "category"),
                       ("goals_scored", "category"),
                       ("goals_against", "category"),
                       ("goals_difference", "category"),
                       ("amount_trophy", "category"),
                       ("victories_20g", "category"),
                       ("goals_diff_20g", "category")])

# Train the model using maximum likelihood estimation
model.fit(df, estimator=MaximumLikelihoodEstimator)

# Predict the category for a new team
new_team = {"points": 60, "victories": 15, "draws": 10, "losses": 15, 
            "goals_scored": 55, "goals_against": 65, "goals_difference": -10, 
            "amount_trophy": 0, "victories_20g": 0, "goals_diff_20g": 0}

print(model.predict(new_team))