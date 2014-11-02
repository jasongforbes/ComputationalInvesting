'''
Created on Nov 2, 2014

@author: Jason
'''
import pandas as pd
import matplotlib.pyplot as plt

class BollingerBands(object):
    '''
    classdocs
    '''


    def __init__(self, HistoricalData, period):
        '''
        Constructor
        '''
        self.portfolio = HistoricalData
        self.period = period
        assert (self.portfolio.end_date - self.portfolio.start_date).days > period,  "period is longer than portfolio"
        self.portfolio.data['bollinger'] = (self.portfolio.data['close'] - pd.rolling_mean(self.portfolio.data['close'], period)) / pd.rolling_std(self.portfolio.data['close'], period)

    def get_bollinger_values(self):
        return self.portfolio.data['bollinger']
    
    def plot(self, symbol, title="", path="",b_save=False):
        assert symbol in self.portfolio.data['close'], "symbol {0} does not exist in historical data".format(symbol)
        mean = pd.rolling_mean(self.portfolio.data['close'], self.period)
        std_dev = 2*pd.rolling_std(self.portfolio.data['close'], self.period)
        upper_band = mean + std_dev
        lower_band = mean - std_dev
        plt.clf()
        portfolio_plt, = plt.plot(self.portfolio.data['close'][symbol],  color='b')
        mean_plt,      = plt.plot(mean[symbol],                          color='r')
        upper_plt,     = plt.plot(upper_band[symbol],                    color='g')
        lower_plt,     = plt.plot(lower_band[symbol],                    color='g')
        plt.title(title)
        plt.xlabel('Days')
        plt.ylabel('Close')
        if b_save:
            plt.savefig(path, format='pdf')
        else:
            plt.show()  
