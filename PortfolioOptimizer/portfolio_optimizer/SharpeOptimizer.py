'''
Created on Oct 5, 2014

@author: Jason
'''
from Optimizer             import Optimizer
from PortfolioSimulation   import PortfolioSimulation
import scipy.optimize as opt
import numpy
from numpy import inf, nan

class SharpeOptimizer(Optimizer):
    '''
    classdocs
    '''
    def __init__(self, PortfolioSimulation):
        '''
        Constructor
        '''
        self.portfolio = PortfolioSimulation
    
    def optimize(self):
        initial_guess = numpy.zeros(len(self.portfolio.symbols))
        initial_guess[0] = 1
        allocation_bounds = numpy.array([[0,1]]*len(self.portfolio.symbols),dtype=float)
        results = opt.minimize(self.portfolio.opt_objective, initial_guess,
                                        bounds=allocation_bounds,
                                        method="SLSQP",
                                        constraints=[{'type':'eq',   'fun': self.portfolio.opt_legal_input_constraint}])
        if results.success:
            (vol, daily_ret, sharpe_ratio, cum_ret) = self.portfolio.simulate(results.x)
            return (results.x, sharpe_ratio)
        else:
            return (results.x, nan)