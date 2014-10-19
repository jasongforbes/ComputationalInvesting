'''
Created on Oct 19, 2014

@author: Jason
'''

import numpy as np

class Portfolio(object):
    '''
    classdocs
    '''

    __returns = np.array(0)
    
    def __init__(self, params):
        '''
        Constructor
        '''
    
    def average_returns(self):
        return np.average(self.__returns)
        
    def standard_deviation(self):
        return np.std(self.__returns)
    
    def sharpe_ratio(self):
        return np.sqrt(252) * self.average_returns()/self.standard_deviation()
   
    def cumulative_return(self):
        return np.cumprod(self.__returns + 1, axis=0)
                