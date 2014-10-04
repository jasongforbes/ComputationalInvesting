'''
Created on Oct 3, 2014

@author: Jason
'''
import datetime
import numpy
import math

import qstkutil.DataAccess as dataaccess
import qstkutil.qsdateutil as dateutil

class PortfolioSimulation:
    '''
    classdocs
    '''
    keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    def __init__(self, symb_list, start_date, end_date):
        '''
        Constructor
        '''
        database = dataaccess.DataAccess('Yahoo', cachestalltime=0)
        
        self.symbols = symb_list 
        self.timestamps =  timestamps = dateutil.getNYSEdays(start_date, end_date, datetime.timedelta(hours=16))
        self.unnormalized_data = dict(zip(self.keys,database.get_data(timestamps, self.symbols, self.keys)))
        self.normalized_close = self.unnormalized_data['close'].values / self.unnormalized_data['close'].values[0,:]
    
    def simulate(self,allocations):
        if len(self.symbols) != len(allocations):
            raise Exception("Length of symb_list and allocations must be equal") 
        earnings = numpy.dot(self.normalized_close,allocations)
        daily_ret = numpy.zeros(numpy.size(earnings))
        daily_ret[1::] = (earnings[1::] / earnings[0:-1]) -1  
        
        avg_daily_ret = numpy.average(daily_ret)
        stddev = numpy.std(daily_ret)
        cum_ret = numpy.cumprod(daily_ret + 1)
        sharpe_ratio = math.sqrt(len(daily_ret)) * avg_daily_ret / stddev
        return(stddev, avg_daily_ret, sharpe_ratio, cum_ret[len(cum_ret)-1])
        
        
        