'''
Created on Oct 18, 2014

@author: Jason
'''
from portfolio.HistoricalData import HistoricalData
from portfolio.Portfolio import Portfolio

import pandas as pd
import numpy as np

class PortfolioSimulation(HistoricalData, Portfolio):
    '''
    classdocs
    '''

    def __init__(self, MarketOrders, starting_cash):
        '''
        Constructor
        '''
        HistoricalData.__init__(self,MarketOrders.symbols(), MarketOrders.start_date(), MarketOrders.end_date())
        Portfolio.__init__(self,MarketOrders.start_date(), MarketOrders.end_date())
        symbs = self.symbols + ['_CASH']
        dates = list(sorted(set([timestamp.date() for timestamp in self.timestamps])))
        # set-up trade matrix
        trade_matrix =  pd.DataFrame(0,index=dates,columns=symbs).values
        row_index = [np.where(self.data['close'].index.date          == date)[0][0] for date in MarketOrders.orders['Date']]
        col_index = [np.where(self.data['close'].columns.values == symb)[0][0] for symb in MarketOrders.orders['Symbol']]
        cost_per_share = self.data['close'].values[row_index,col_index]
        trade_matrix[0,-1] = starting_cash
        for index,(row,col) in enumerate(zip(row_index,col_index)):
            trade_matrix[row,col]+=MarketOrders.orders['Buy'].values[index]*MarketOrders.orders['Number'].values[index]
            trade_matrix[row,-1] -=MarketOrders.orders['Buy'].values[index] * MarketOrders.orders['Number'].values[index] * cost_per_share[index]
        self.data['Trades'] = pd.DataFrame(trade_matrix,index=dates,columns=symbs)
        # generate holdings matrix
        self.data['Holdings'] = pd.DataFrame(np.cumsum(self.data['Trades'][:].values,axis=0),index=dates,columns=symbs) 
        self.data['Holdings']['Value'] = np.sum(self.data['Holdings'][self.symbols].values * self.data['close'][self.symbols].values,axis=1)+self.data['Holdings']['_CASH'].values
        self.data['Holdings']['Year']  = [date.year for date in dates]
        self.data['Holdings']['Month'] = [date.month for date in dates]
        self.data['Holdings']['Day']   = [date.day for date in dates]
        # determine portfolio returns
        returns = np.zeros(self.data['Holdings']['Value'].values.size)
        returns[1::] = self.data['Holdings']['Value'].values[1::]/self.data['Holdings']['Value'].values[0:-1] - 1
        self.set_returns( pd.DataFrame(returns, index=self.timestamps))

    def to_csv(self,path):
        self.data['Holdings'].to_csv(path_or_buf=path, cols=['Year','Month','Day','Value'],index_label='Date')