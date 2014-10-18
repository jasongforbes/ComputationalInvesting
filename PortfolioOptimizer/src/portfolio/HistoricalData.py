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
    keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    def __init__(self, symb_list, start_date, end_date):
        '''
        Constructor
        '''
        database = dataaccess.DataAccess('Yahoo')
        self.start_date = start_date
        self.end_date = end_date
        self.symbols = symb_list
        self.timestamps =  timestamps = dateutil.getNYSEdays(start_date, end_date, datetime.timedelta(hours=16))
        self.data = dict(zip(self.keys,database.get_data(timestamps, self.symbols, self.keys)))
        
        for key in self.keys:
            self.data[key] = self.data[key].fillna(method = 'ffill')
            self.data[key] = self.data[key].fillna(method = 'bfill')
            self.data[key] = self.data[key].fillna(1.0)
        
        self.avg_returns = numpy.average(self.normalized_returns(),  axis=0)
        self.covariance = numpy.cov(self.normalized_returns(), rowvar=0)   
        
    def normalized_returns(self):
        normalized_close = self.normalized_close()
        normalized_returns = numpy.zeros(normalized_close.shape)
        normalized_returns[1::,:] = (normalized_close[1::,:] / normalized_close[0:-1,:]) -1
        return normalized_returns
    
    def returns(self):
        close = self.data['close'].values
        normalized_returns = numpy.zeros(close.shape)
        normalized_returns[1::,:] = (close[1::,:] / close[0:-1,:]) -1
        return normalized_returns
    
    def normalized_close(self):
        return self.data['close'].values / self.data['close'].values[0,:]
