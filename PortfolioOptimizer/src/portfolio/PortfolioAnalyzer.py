'''
Created on Oct 19, 2014

@author: Jason
'''
import HistoricalPortfolio as hp
import matplotlib.pyplot as plt
import datetime as dt

class PortfolioAnalyzer(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def analyze(self,portfolio,benchmark,name="",path="",b_save=False):
        bench = hp.HistoricalPortfolio(benchmark,portfolio.get_startdate(), portfolio.get_enddate())
        bench.simulate()
        
        numdays = (portfolio.get_enddate() -  portfolio.get_startdate()).days + 1
        daterange = sorted([portfolio.get_startdate() - dt.timedelta(days=x) for x in range(0, numdays)])
        
        plt.clf()
        portfolio_plt, = plt.plot(portfolio.cumulative_return(), color='b')
        bench_plt,     = plt.plot(bench.cumulative_return(),     color='g')
        plt.legend([portfolio_plt, bench_plt],[str(name),str(benchmark)])
        plt.title('Returns of ' + name + " and " + benchmark)
        plt.xlabel('Days')
        plt.ylabel('Returns')
        if b_save:
            plt.savefig(path, format='pdf')
        else:
            plt.show()  
        column_width=18
        print "\n{3:<{2}}     {0:>{2}}    {1:>{2}}"          .format("Portfolio",                          "Benchmark",                  column_width, name)
        print "Average Returns    -   {0:>{2}}    {1:>{2}}".format(portfolio.average_returns(),          bench.average_returns(),      column_width)
        print "Volatility         -   {0:>{2}}    {1:>{2}}".format(portfolio.standard_deviation(),       bench.standard_deviation(),   column_width)
        print "Sharpe Ratio       -   {0:>{2}}    {1:>{2}}".format(portfolio.sharpe_ratio(),             bench.sharpe_ratio(),         column_width)
        print "Cumulative Returns -   {0:>{2}}    {1:>{2}}".format(portfolio.cumulative_return()[-1][0], bench.cumulative_return()[-1],column_width)
        