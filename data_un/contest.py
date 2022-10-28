# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 13:56:52 2022

@author: SaGaRueda
"""


from datetime import datetime
import time
import pandas as pd
import numpy as np
data = pd.read_csv('contests.csv',delimiter = '\t')


#print(datetime.datetime.fromtimestamp(i))

x = 1607295300000
x2 = 1607295300
x3 = 1666130400
j = 1
for i in data['start_date']:
    ss= int(str(i)[0:-3])
    #print(ss)
    print(datetime.fromtimestamp(ss))
    j+=1