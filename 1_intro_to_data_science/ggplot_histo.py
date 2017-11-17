# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 08:41:24 2015

@author: brianchase
"""

from pandas import *
import datetime

turnstile_weather = pandas.read_csv("turnstile_data_master_with_weather.csv")


def reformat_subway_dates(date):
    '''
    The dates in our subway data are formatted in the format month-day-year.
    The dates in our weather underground data are formatted year-month-day.
    
    In order to join these two data sets together, we'll want the dates formatted
    the same way.  Write a function that takes as its input a date in the MTA Subway
    data format, and returns a date in the weather underground format.
    
    Hint: 
    There are a couple of useful functions in the datetime library that will
    help on this assignment, called strptime and strftime. 
    More info can be seen here and further in the documentation section:
    http://docs.python.org/2/library/datetime.html#datetime.datetime.strptime
    '''
    #print date.dtype()
    dt = datetime.datetime.strptime(date, "%m-%d-%y")
    date_formatted = dt.strftime("%w")
    #print date_formatted
    return date_formatted

date_col = turnstile_weather['DATEn']
print reformat_subway_dates(date_col)