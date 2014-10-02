'''
Created on Oct 1, 2014

@author: Jason
'''

import datetime
import matplotlib.pyplot
import pandas
import numpy
import math

import qstkutil.DataAccess as dataaccess
import qstkutil.qsdateutil as dateutil
import qstkutil.tsutil     as tsutil



def simulate(start_date, end_date, symb_list, allocations):
    if len(allocations) != len(symb_list):
        raise Exception("equities and allocations of unequeal length")
    
    
    timestamps = dateutil.getNYSEdays(start_date, end_date, datetime.timedelta(hours=16))  # specify time of day - 4:00pm (hour = 16) for close of market
    
    database = dataaccess.DataAccess('Yahoo', cachestalltime=0)
    database_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    data = dict(zip(database_keys,database.get_data(timestamps, symb_list, database_keys)))
    normalized_close = data['close'].values / data['close'].values[0,:]
    daily_close = numpy.dot(normalized_close,allocations)
    daily_ret   = tsutil.returnize0(daily_close.copy())  
    
    avg_daily_ret = numpy.average(daily_ret)
    stddev = numpy.std(daily_ret)
    cum_ret = numpy.cumprod(daily_ret + 1)
    
    return (stddev, avg_daily_ret, math.sqrt(len(daily_ret))*avg_daily_ret/stddev, cum_ret[len(cum_ret)-1])
        

