'''
Created on Oct 2, 2014

@author: Jason
'''
import unittest
import datetime
from portfolio import HistoricalPortfolio as ps

class HistoricalPortfolioTest(unittest.TestCase):


    def testPortfolioSimulation(self):       
        self.ValidatePortfolioSimulation(ps.HistoricalPortfolio(['AAPL', 'GLD', 'GOOG', 'XOM'], datetime.date(2011,1,1), datetime.date(2011,12,31)), 
                                         [0.4, 0.4, 0.0, 0.2], 0.0101467068, 0.0006572611, 1.0282840310 , 1.1648726196, True)
        self.ValidatePortfolioSimulation(ps.HistoricalPortfolio(['AXP', 'HPQ', 'IBM', 'HNZ'], datetime.date(2010,1,1), datetime.date(2010,12,30)), 
                                         [0.0, 0.0, 0.0, 1.0], 0.00924299255937, 0.000756285585593, 1.2989003411, 1.1960583568, True) 


    def ValidatePortfolioSimulation(self, portfolio, allocations, exp_std_dev, exp_avg_daily_ret, exp_sharpe_ratio, exp_cum_ret, bool_plot):
        (std_dev, daily_ret, sharpe, cum_ret) = portfolio.simulate(allocations)
        self.assertAlmostEqual(std_dev,   exp_std_dev,        4, "Std. deviation %.10f != %.10f "     % (std_dev, exp_std_dev))
        self.assertAlmostEqual(daily_ret, exp_avg_daily_ret,  4, "Daily return %.10f != %.10f "       % (daily_ret, exp_avg_daily_ret))
        self.assertAlmostEqual(sharpe,    exp_sharpe_ratio,   4, "Sharpe ratio %.10f != %.10f "       % (sharpe, exp_sharpe_ratio))
        self.assertAlmostEqual(cum_ret,   exp_cum_ret,        4, "Cumulative return %.10f != %.10f "  % (cum_ret, exp_cum_ret))
        if bool_plot:
            portfolio.plot_daily_returns(allocations, ['SPY'])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'HistoricalPortfolioTest.testOptimize']
    unittest.main()