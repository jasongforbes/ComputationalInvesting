'''
Created on Oct 10, 2014

@author: Jason
'''
import datetime
import numpy
import pandas
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
        self.data['returns'] = pandas.DataFrame(0, index=self.timestamps, columns=self.symbols)
        
        
        for key in self.keys:
            self.data[key] = self.data[key].fillna(method = 'ffill')
            self.data[key] = self.data[key].fillna(method = 'bfill')
            self.data[key] = self.data[key].fillna(1.0)
            
        self.data['returns'].iloc[1::,:] =(self.data['close'][:][1::] / self.data['close'].values[0:-1]) -1
        
    def normalized_returns(self):
        normalized_close = self.normalized_close()
        normalized_returns = numpy.zeros(normalized_close.shape)
        normalized_returns[1::,:] = (normalized_close[1::,:] / normalized_close[0:-1,:]) -1
        return normalized_returns
    
    def get_startdate(self):
        return self.start_date
    
    def get_enddate(self):
        return self.end_date
    
    def get_symbols(self):
        return self.symbols
    
    def get_timestamps(self):
        return self.timestamps
    
    def get_returns(self):
        return self.data['returns']
    
    def get_close(self):
        return self.data['close']
    
    def get_actual_clos(self):
        return self.data['actual_close']
    
    def get_high(self):
        return self.data['high']
    
    def get_low(self):
        return self.data['low']
    
    def open(self):
        return self.data['open']
    
    def volume(self):
        return self.data['volume']
    
    def normalized_close(self):
        return self.data['close'].values / self.data['close'].values[0,:]
