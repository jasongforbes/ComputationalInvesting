'''
Created on Oct 4, 2014

@author: Jason
'''
import datetime
import time
import unittest
from numpy               import testing
from PortfolioSimulation import PortfolioSimulation
from BruteOptimizer      import BruteOptimizer
from SharpeOptimizer     import SharpeOptimizer

class Test(unittest.TestCase):

    def setUp(self):
        self.portfolios = [PortfolioSimulation(['AAPL', 'GLD', 'GOOG', 'XOM'],datetime.date(2011,1,1),datetime.date(2011,12,31)),
                           PortfolioSimulation(['AXP', 'HPQ', 'IBM', 'HNZ'], datetime.date(2010,1,1), datetime.date(2010,12,30))]
        self.brute_results = [[0.4, 0.4, 0.0, 0.2],
                              [0.0, 0.0, 0.0, 1.0]]
        self.sharpe_results = [[0.46, 0.37, 0.0, 0.17],
                               [0.0, 0.0, 0.0, 1.0]]

    def testBruteOptimizer(self):
        print "Brute Optimization Test"
        print "----------------------"
        for index in range(0,len(self.portfolios)):
            self.ValidateOptimization(BruteOptimizer(self.portfolios[index],0.1), self.brute_results[index], self.portfolios[index])
        
    def testSharpeOptimizer(self):
        print "Sharpe Optimization Test"
        print "----------------------"
        for index in range(0,len(self.portfolios)):
            self.ValidateOptimization(SharpeOptimizer(self.portfolios[index]), self.sharpe_results[index], self.portfolios[index])       

        
    def ValidateOptimization(self, optimizer, exp_allocations, portfolio):
        start_time = time.time()
        (allocations, sharpe_ratio) = optimizer.optimize()
        end_time = time.time()
        print "Portfolio            %s" % (portfolio.symbols)
        print "Allocations          {0}".format(portfolio.symbols)  
        print "Sharpe Ratio         {0}".format(sharpe_ratio)  
        print "Time Elapsed (ms)    {0}\n".format(1000*(end_time-start_time)) 
        testing.assert_array_almost_equal( allocations, exp_allocations, 2, "Portfolio allocation weighting array is incorrect")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testOptimizer']
    unittest.main()