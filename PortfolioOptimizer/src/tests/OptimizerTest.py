'''
Created on Oct 4, 2014

@author: Jason
'''
import datetime
import time
import unittest
from numpy     import testing
from portfolio import HistoricalPortfolio as ps
from optimizer import BruteOptimizer as brute
from optimizer import SharpeOptimizer as sharpe

class Test(unittest.TestCase):

    def setUp(self):
        self.portfolios = [ps.HistoricalPortfolio(['AAPL', 'GLD', 'GOOG', 'XOM'],datetime.date(2011,1,1),datetime.date(2011,12,31)),
                           ps.HistoricalPortfolio(['AXP', 'HPQ', 'IBM', 'HNZ'], datetime.date(2010,1,1), datetime.date(2010,12,30))]
        self.brute_results  = [[0.4, 0.4, 0.0, 0.2],
                               [0.0, 0.0, 0.1, 0.9]]
        self.sharpe_results = [[0.42, 0.40, 0.0, 0.18],
                               [0.0, 0.0, 0.07, 0.93]]
        
        
    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testBruteOptimizer(self):
        print "Brute Optimization Test"
        print "----------------------"
        for index in range(0,len(self.portfolios)):
            self.ValidateOptimization(brute.BruteOptimizer(self.portfolios[index],0.1), self.brute_results[index], self.portfolios[index])
        
    def testSharpeOptimizer(self):
        print "Sharpe Optimization Test"
        print "----------------------"
        for index in range(0,len(self.portfolios)):
            self.ValidateOptimization(sharpe.SharpeOptimizer(self.portfolios[index]), self.sharpe_results[index], self.portfolios[index])       

        
    def ValidateOptimization(self, optimizer, exp_allocations, portfolio):
        start_time = time.time()
        (allocations, sharpe_ratio) = optimizer.optimize()
        end_time = time.time()
        print "Portfolio            %s" % (portfolio.symbols)
        print "Allocations          {0}".format(allocations)  
        print "Sharpe Ratio         {0}".format(sharpe_ratio)  
        print "Time Elapsed (ms)    {0}\n".format(1000*(end_time-start_time)) 
        testing.assert_array_almost_equal( allocations, exp_allocations, 2, "Portfolio allocation weighting array is incorrect")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testOptimizer']
    unittest.main()