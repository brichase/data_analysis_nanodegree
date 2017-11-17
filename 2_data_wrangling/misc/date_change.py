# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 23:21:41 2015

@author: brianchase
"""

import numpy
from pandas import *
from ggplot import *
import datetime

def reformat_subway_dates(date):    
    dt = datetime.datetime.strptime(date, "%Y-%m-%d")
    date_formatted = dt.strftime("%w")
    #print date_formatted
    return date_formatted

data = pandas.read_csv("turnstile_data_master_with_weather.csv")

mean_entries_day = [0]*7
data[['DATEn']] = data[['DATEn']].applymap(reformat_subway_dates)

for i in range(0,7):        
        mean_entries_day[i] = numpy.mean(data['ENTRIESn_hourly'][data['DATEn'].astype(int) == i])
 
average_dict = {'DATEn': Series(range(0,7)),
                'avg_entries_day': Series(mean_entries_day)}
data = DataFrame(average_dict)
    
plot = ggplot(data, aes('DATEn', 'avg_entries_day')) + geom_point() + geom_line() + ggtitle("Mean ENTRIESn_hourly by day of the Week") + xlab("Day (0=Sunday, 6=Saturday)") + ylab("Average ENTRIESn_hourly") + xlim(0,6) 
print plot
#print date_col
#print reformat_subway_dates(date_col)