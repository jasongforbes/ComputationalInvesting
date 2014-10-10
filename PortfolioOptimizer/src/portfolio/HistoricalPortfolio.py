'''
Created on Oct 3, 2014

@author: Jason
'''
import numpy
import math
import matplotlib.pyplot as plot

from portfolio import HistoricalData as hs

class HistoricalPortfolio(hs.HistoricalData):
    '''
    classdocs
    '''
    keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    
    def __init__(self, symb_list, start_date, end_date):
        '''
        Constructor
        '''
        super(HistoricalPortfolio,self).__init__(symb_list, start_date, end_date)
        
    def simulate(self,allocations):
        n = self.normalized_returns.shape[0]
        allocations = numpy.array(allocations)
        avg_daily_ret = numpy.dot(self.avg_returns,allocations) 
        stddev = numpy.sqrt(allocations.T.dot(self.covariance.dot(allocations)))
        cum_ret = numpy.cumprod(self.normalized_returns + 1, axis=0).dot(allocations)
        sharpe_ratio  = math.sqrt(n) *avg_daily_ret / stddev
        return(stddev, avg_daily_ret, sharpe_ratio, cum_ret[len(cum_ret)-1])
    
    def get_daily_earnings(self,allocations):
        if len(self.symbols) != len(allocations):
            raise Exception("Length of symb_list and allocations must be equal") 
        earnings = self.normalized_close.dot(allocations)
        return earnings
    
    def plot_daily_returns(self,allocations,benchmarks):
        daily_earnings = self.get_daily_earnings(allocations)
        benchmark = HistoricalPortfolio(benchmarks, self.start_date, self.end_date)
        plot.clf()
        plot.plot(numpy.append(benchmark.normalized_close, daily_earnings.reshape(len(benchmark.normalized_close),1) ,axis=1))
        plot.legend((benchmark.symbols,"Portfolio"))
        plot.ylabel('Adjusted Close')
        plot.xlabel('Date')
        plot.draw()
        plot.show()
        