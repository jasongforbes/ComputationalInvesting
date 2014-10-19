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
        self.data['Trades'] = pd.DataFrame(0,index=dates,columns=symbs)
        self.data['Trades']['_CASH'][self.start_date]=starting_cash
        for order_index, trade in enumerate(zip(MarketOrders.orders.loc[:,'Date'],MarketOrders.orders.loc[:,'Symbol'])):
            buy_modifier = MarketOrders.orders['Buy'][order_index]                #-1 for sell, 1 for buy
            num_shares   = MarketOrders.orders['Number'][order_index]             #number of shares to buy/sell
            row_index = self.data['Trades'].index.get_loc(trade[0])
            cost_per_share = self.data['close'][trade[1]][row_index]       #cost of transaction
            self.data['Trades'].loc[trade]=buy_modifier*num_shares
            self.data['Trades']['_CASH'][row_index] = self.data['Trades']['_CASH'][row_index] - buy_modifier*num_shares*cost_per_share
        self.data['Holdings'] = pd.DataFrame(np.cumsum(self.data['Trades'][:].values,axis=0),index=dates,columns=symbs) 
        self.data['Holdings']['Value'] = np.sum(self.data['Holdings'][self.symbols].values * self.data['close'][self.symbols].values,axis=1)+self.data['Holdings']['_CASH'].values
        self.data['Holdings']['Year']  = [date.year for date in dates]
        self.data['Holdings']['Month'] = [date.month for date in dates]
        self.data['Holdings']['Day']   = [date.day for date in dates]
        returns = np.zeros(self.data['Holdings']['Value'].values.size)
        returns[1::] = self.data['Holdings']['Value'].values[1::]/self.data['Holdings']['Value'].values[0:-1] - 1
        self.set_returns( pd.DataFrame(returns, index=self.timestamps))

    def to_csv(self,path):
        self.data['Holdings'].to_csv(path_or_buf=path, cols=['Year','Month','Day','Value'],index_label='Date')