'''
Created on Oct 10, 2014

@author: Jason
'''
import datetime
import numpy
from utils import transforms as tf

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
        self.symbols = tf.wrap(symb_list,list)
        self.timestamps =  timestamps = dateutil.getNYSEdays(start_date, end_date, datetime.timedelta(hours=16))
        self.data = dict(zip(self.keys,database.get_data(timestamps, self.symbols, self.keys)))
        
        for key in self.keys:
            self.data[key] = self.data[key].fillna(method = 'ffill')
            self.data[key] = self.data[key].fillna(method = 'bfill')
            self.data[key] = self.data[key].fillna(1.0)
        
    def normalized_returns(self):
        normalized_close = self.normalized_close()
        normalized_returns = numpy.zeros(normalized_close.shape)
        normalized_returns[1::,:] = (normalized_close[1::,:] / normalized_close[0:-1,:]) -1
        return normalized_returns
    
    def data_returns(self):
        close = self.data['close'].values
        returns = numpy.zeros(close.shape)
        returns[1::,:] = (close[1::,:] / close[0:-1,:]) -1
        return returns
    
    def normalized_close(self):
        return self.data['close'].values / self.data['close'].values[0,:]
