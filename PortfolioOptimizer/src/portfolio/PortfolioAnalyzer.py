'''
Created on Oct 19, 2014

@author: Jason
'''
import HistoricalPortfolio as hp

class PortfolioAnalyzer(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def analyze(self,portfolio,benchmark,name="",):
        bench = hp.HistoricalPortfolio(benchmark,portfolio.get_startdate(), portfolio.get_enddate())
        bench.simulate()
        column_width=18
        print name
        print "                       {0:>{2}}    {1:>{2}}".format("Portfolio",                          "Benchmark",                  column_width)
        print "Average Returns    -   {0:>{2}}    {1:>{2}}".format(portfolio.average_returns(),          bench.average_returns(),      column_width)
        print "Volatility         -   {0:>{2}}    {1:>{2}}".format(portfolio.standard_deviation(),       bench.standard_deviation(),   column_width)
        print "Sharpe Ratio       -   {0:>{2}}    {1:>{2}}".format(portfolio.sharpe_ratio(),             bench.sharpe_ratio(),         column_width)
        print "Cumulative Returns -   {0:>{2}}    {1:>{2}}".format(portfolio.cumulative_return()[-1][0], bench.cumulative_return()[-1],column_width)
        