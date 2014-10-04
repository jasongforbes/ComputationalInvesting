'''
Created on Oct 4, 2014

@author: Jason
'''
import datetime
import unittest
from numpy import testing
from PortfolioSimulation import PortfolioSimulation
from BruteOptimizer import BruteOptimizer

class Test(unittest.TestCase):


    def testBruteOptimizer(self):
        portfolio = PortfolioSimulation(['AAPL', 'GLD', 'GOOG', 'XOM'],datetime.date(2011,1,1),datetime.date(2011,12,31))
        self.ValidateOptimization(BruteOptimizer(portfolio,0.1), [0.4, 0.4, 0.0, 0.2])
        portfolio = PortfolioSimulation(['AXP', 'HPQ', 'IBM', 'HNZ'], datetime.date(2010,1,1), datetime.date(2010,12,30))
        self.ValidateOptimization(BruteOptimizer(portfolio,0.1), [0.0, 0.0, 0.0, 1.0])        

        
    def ValidateOptimization(self, optimizer, exp_allocations):
        (allocations, sharpe_ratio) = optimizer.optimize()
        testing.assert_array_equal( allocations, exp_allocations, "Portfolio allocation weighting array is incorrect")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testBruteOptimizer']
    unittest.main()