'''
Created on Oct 3, 2014

@author: Jason
'''
import numpy
import math
import matplotlib.pyplot as plot

from portfolio import HistoricalData as hs
from portfolio import Portfolio as pf

class HistoricalPortfolio(hs.HistoricalData, pf.Portfolio ):
    '''
    classdocs
    '''
    def __init__(self, symb_list, start_date, end_date):
        '''
        Constructor
        '''
        hs.HistoricalData.__init__(self, symb_list, start_date, end_date)
        pf.Portfolio.__init__(self, start_date, end_date)
        self.avg_returns = numpy.average(self.data_returns(),  axis=0)
        self.covariance  = numpy.cov(self.data_returns(), rowvar=0)   
        
    def simulate(self,allocations):
        self.allocations = numpy.array(allocations)
        return(self.standard_deviation(), self.average_returns(), self.sharpe_ratio(), self.cumulative_return()[-1])
    
    def get_daily_earnings(self,allocations):
        if len(self.symbols) != len(allocations):
            raise Exception("Length of symb_list and allocations must be equal") 
        earnings = self.normalized_close().dot(allocations)
        return earnings
    
    def average_returns(self):
        return self.avg_returns.dot(self.allocations)
        
    def standard_deviation(self):
        return numpy.sqrt(self.allocations.T.dot(self.covariance.dot(self.allocations)))
    
    def cumulative_return(self):
        return numpy.cumprod(self.data_returns() + 1, axis=0).dot(self.allocations)
    
    def plot_daily_returns(self,allocations,benchmarks):
        daily_earnings = self.get_daily_earnings(allocations)
        benchmark = HistoricalPortfolio(benchmarks, self.start_date, self.end_date)
        plot.clf()
        plot.plot(numpy.append(benchmark.normalized_close(), daily_earnings.reshape(len(benchmark.normalized_close()),1) ,axis=1))
        plot.legend((benchmark.symbols,"Portfolio"))
        plot.ylabel('Adjusted Close')
        plot.xlabel('Date')
        plot.draw()
        plot.show()
        