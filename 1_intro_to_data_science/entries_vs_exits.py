# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 09:21:26 2015

@author: brianchase
"""

import numpy
from pandas import *
from ggplot import *

data = pandas.read_csv("turnstile_data_master_with_weather.csv")
entry = numpy.sum(data['ENTRIESn_hourly'])
print entry
exits = numpy.sum(data['EXITSn_hourly'])
print exits
print entry - exits