'''
Created on Oct 10, 2014

@author: Jason
'''
import datetime
import numpy

import qstkutil.DataAccess as dataaccess
import qstkutil.qsdateutil as dateutil

class HistoricalData(object):
    '''
    classdocs
    '''


    def __init__(self, symb_list, start_date, end_date):
        '''
        Constructor
        '''
        database = dataaccess.DataAccess('Yahoo', cachestalltime=0)
        self.start_date = start_date
        self.end_date = end_date
        self.symbols = symb_list
        self.timestamps =  timestamps = dateutil.getNYSEdays(start_date, end_date, datetime.timedelta(hours=16))
        self.unnormalized_data = dict(zip(self.keys,database.get_data(timestamps, self.symbols, self.keys)))
        self.normalized_close = self.unnormalized_data['close'].values / self.unnormalized_data['close'].values[0,:]
        self.normalized_returns = numpy.zeros(self.normalized_close.shape)
        self.normalized_returns[1::,:] = (self.normalized_close[1::,:] / self.normalized_close[0:-1,:]) -1
        self.avg_returns = numpy.average(self.normalized_returns,  axis=0)
        self.covariance = numpy.cov(self.normalized_returns, rowvar=0)       