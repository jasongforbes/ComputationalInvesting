'''
Created on Oct 3, 2014

@author: Jason
'''
import numpy
import pandas
import math
from utils import transforms as tf
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
        self.avg_returns = numpy.average(self.get_returns(),  axis=0)
        self.covariance  = numpy.cov(self.get_returns(), rowvar=0)   
        
    def simulate(self,allocations=1):
        self.allocations = numpy.array(tf.wrap(allocations,list))
        self.data['cumret'] = numpy.cumprod(self.get_returns()+1,axis=0)
        self.data['value'] = self.data['cumret'].dot(self.allocations.T)
        returns = numpy.zeros(self.data['value'].values.size)
        returns[1::] = self.data['value'].values[1::].T/self.data['value'].values[0:-1].T - 1
        self.set_returns( pandas.DataFrame(returns, index=self.get_timestamps()))
        return(self.standard_deviation(), self.average_returns(), self.sharpe_ratio(), self.cumulative_return()[-1])
    
    def get_daily_earnings(self,allocations):
        if len(self.symbols) != len(allocations):
            raise Exception("Length of symb_list and allocations must be equal") 
        earnings = self.normalized_close().dot(allocations)
        return earnings
    
    def get_portfolio_value(self):
        return self.data['value']
    
    def get_cumulative_returns(self):
        return self.data['cumret']
    
    def get_covariance(self):
        return self.covariance

    def plot_daily_returns(self,allocations,benchmarks):
        daily_earnings = self.get_daily_earnings(allocations)
        benchmark = HistoricalPortfolio(benchmarks, self.get_startdate(), self.get_enddate())
        plot.clf()
        plot.plot(numpy.append(benchmark.normalized_close(), daily_earnings.reshape(len(benchmark.normalized_close()),1) ,axis=1))
        plot.legend((benchmark.symbols,"Portfolio"))
        plot.ylabel('Adjusted Close')
        plot.xlabel('Date')
        plot.draw()
        plot.show()
        