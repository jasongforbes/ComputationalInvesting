'''
Created on Oct 18, 2014

@author: Jason
'''
from portfolio.HistoricalData import HistoricalData

import pandas as pd
import numpy as np

class PortfolioSimulation(HistoricalData):
    '''
    classdocs
    '''

    def __init__(self, MarketOrders, starting_cash):
        '''
        Constructor
        '''
        super(PortfolioSimulation,self).__init__(MarketOrders.symbols(), MarketOrders.start_date(), MarketOrders.end_date())
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
        self.data['Value'] = pd.DataFrame(np.sum(self.data['Holdings'][self.symbols].values * self.data['close'][self.symbols].values,axis=1)+self.data['Holdings']['_CASH'].values,index=dates, columns=['Value'])
        self.data['Value']['Year']  = [date.year for date in dates]
        self.data['Value']['Month'] = [date.month for date in dates]
        self.data['Value']['Day']   = [date.day for date in dates]

    def to_csv(self,path):
        self.data['Value'].to_csv(path_or_buf=path, columns=['Year','Month','Day','Value'],index_label='Date')