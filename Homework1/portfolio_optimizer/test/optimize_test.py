'''
Created on Oct 2, 2014

@author: Jason
'''
import unittest
import datetime
import optimize

class Test(unittest.TestCase):


    def testOptimize(self):
        start_date = datetime.date(2011,1,1)
        end_date   = datetime.date(2011,12,31)
        symbols    = ['AAPL', 'GLD', 'GOOG', 'XOM']
        allocations= [0.4, 0.4, 0.0, 0.2]
        vol, daily_ret, sharpe, cum_ret = optimize.simulate(start_date, end_date, symbols, allocations)
        self.assertAlmostEqual(sharpe,       1.02828403099,     7, "Sharpe ratio %f != %f "   % (sharpe, 1.02828403099))
        self.assertAlmostEqual(vol,          0.0101467067654,   7, "Std. deviation %f != %f " % (vol, 0.0101467067654))
        self.assertAlmostEqual(daily_ret,    0.000657261102001, 7, "Daily return %f != %f "   % (daily_ret, 0.000657261102001))
        self.assertAlmostEqual(cum_ret,      1.16487261965,     7, "Cum return %f != %f "     % (cum_ret, 1.16487261965))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testOptimize']
    unittest.main()