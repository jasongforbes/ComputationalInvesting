'''
Created on Oct 5, 2014

@author: Jason
'''
import scs #needed to avoid memory error on shutdown
from Optimizer import Optimizer
import numpy
import cvxpy as cvx


class SharpeOptimizer(Optimizer):
    '''
    classdocs
    '''
    def __init__(self, portfolio):
        '''
        Constructor
        '''
        self.portfolio = portfolio
    
    def optimize(self):
        n = len(self.portfolio.get_symbols())
        x = cvx.Variable(n)
        t = cvx.Variable(1)
        
        Sigma = self.portfolio.get_covariance()
        R = numpy.average(self.portfolio.get_returns().values,axis=0)
        
        objective = cvx.Maximize(x.T * R)
        constraints = [cvx.quad_form(x,Sigma) <= 1,
                       cvx.sum_entries(x) == t,
                       x <= t,
                       x.T * R >= 0,
                       x >= 0,
                       t >= 0]
        problem = cvx.Problem(objective,constraints)               
        
        problem.solve(solver=cvx.CVXOPT)     
        if problem.status == cvx.OPTIMAL:
            allocation = numpy.squeeze(numpy.asarray(x.value/t.value))
            sharpe_ratio = self.portfolio.simulate(allocation)[2]
            return (allocation, sharpe_ratio)
        else:
            return (numpy.zeros(n), numpy.nan)