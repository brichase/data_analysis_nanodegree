# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 09:27:43 2015

@author: brianchase
"""

import numpy as np
import pandas
import statsmodels.api as sm

def linear_regression(features, values):
    features = sm.add_constant(features)
    model = sm.OLS(values, features)
    results = model.fit()
    intercept = results.params[0]
    params = results.params[1:]
    return intercept, params
    
def predictions(dataframe):
    features = dataframe[['rain', 'precipi', 'Hour', 'meantempi']]
    dummy_units = pandas.get_dummies(dataframe['UNIT'],prefix='unit')
    features = features.join(dummy_units)
    
    values = dataframe['ENTRIESn_hourly']
    
    intercept, params = linear_regression(features, values)
    
    predictions = intercept + np.dot(features,values)
    return predictions
    
data = pandas.read_csv("turnstile_data_master_with_weather.csv")
print predictions(data)
