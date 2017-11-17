# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 15:11:25 2015

@author: brianchase
"""
import numpy
from pandas import *
from ggplot import *

def plot_weather_data(turnstile_weather):
    '''
    You are passed in a dataframe called turnstile_weather. 
    Use turnstile_weather along with ggplot to make a data visualization
    focused on the MTA and weather data we used in assignment #3.  
    You should feel free to implement something that we discussed in class 
    (e.g., scatterplots, line plots, or histograms) or attempt to implement
    something more advanced if you'd like.  

    Here are some suggestions for things to investigate and illustrate:
     * Ridership by time of day or day of week
     * How ridership varies based on Subway station (UNIT)
     * Which stations have more exits or entries at different times of day
       (You can use UNIT as a proxy for subway station.)

    If you'd like to learn more about ggplot and its capabilities, take
    a look at the documentation at:
    https://pypi.python.org/pypi/ggplot/
     
    You can check out:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
     
    To see all the columns and data points included in the turnstile_weather 
    dataframe. 
     
    However, due to the limitation of our Amazon EC2 server, we are giving you a random
    subset, about 1/3 of the actual data in the turnstile_weather dataframe.
    '''
    mean_entries_hour = [0]*25
    
    for i in range(0,23):        
        mean_entries_hour[i] = numpy.mean(turnstile_weather['ENTRIESn_hourly'][turnstile_weather['Hour'] == i])
    
    average_dict = {'Hour': Series(range(0,25)),
                    'avg_entries_hourly': Series(mean_entries_hour)}
    data = DataFrame(average_dict)
    
    plot = ggplot(data, aes('Hour', 'avg_entries_hourly')) + geom_point() + geom_line() + ggtitle("Average ENTRIESn_hourly vs Hour") + xlab("Hour") + ylab("Average ENTRIESn_hourly") + xlim(0,24) + ylim(0,3000)
    return plot
