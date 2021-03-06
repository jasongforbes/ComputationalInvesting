'''
Created on Oct 4, 2014

@author: Jason
'''
from Optimizer import Optimizer as optimizer_base
from sklearn.utils.extmath import cartesian
import numpy


class BruteOptimizer(optimizer_base):
    '''
    classdocs
    '''


    def __init__(self, portfolio, allocation_step_size):
        '''
        Constructor
        '''
        if allocation_step_size < 0 or allocation_step_size > 1:
            raise Exception("allocation_step_size must be between 0 and 1")
        self.portfolio = portfolio
        self.stepsize = allocation_step_size
    
    def optimize(self):
        best_sharpe_ratio = 0
        best_allocation = []
        num_symbols = len(self.portfolio.get_symbols())
        steps = numpy.linspace(0, 1, 1/self.stepsize + 1)
        allocations = cartesian([steps]*num_symbols)
        legal_allocations = allocations[numpy.where(allocations.sum(1)==1)]
        for allocation in legal_allocations:
            sharpe = self.portfolio.simulate(allocation)[2]
            if sharpe > best_sharpe_ratio:
                best_sharpe_ratio = sharpe
                best_allocation = allocation
        return (best_allocation, best_sharpe_ratio)
        