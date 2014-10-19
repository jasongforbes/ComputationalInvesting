'''
Created on Oct 19, 2014

@author: Jason
'''

import numpy as np

class Portfolio(object):
    '''
    classdocs
    '''

    __returns = None
    
    def __init__(self, startdate, enddate):
        '''
        Constructor
        '''
        self._startdate = startdate
        self._enddate = enddate
    
    def get_startdate(self):
        return self._startdate
        
    def get_enddate(self):
        return self._enddate
    
    def set_returns(self, returns):
        self.__returns = returns
        
    def get_returns(self):
        return self.__returns
    
    def average_returns(self):
        return np.average(self.__returns.values)
        
    def standard_deviation(self):
        return np.std(self.__returns.values)
    
    def sharpe_ratio(self):
        return np.sqrt(252) * self.average_returns()/self.standard_deviation()
   
    def cumulative_return(self):
        return np.cumprod(self.__returns.values + 1, axis=0)
                