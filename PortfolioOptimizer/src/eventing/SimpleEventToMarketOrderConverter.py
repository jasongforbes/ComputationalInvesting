'''
Created on Oct 25, 2014

@author: Jason
'''
import numpy as np
import sklearn.utils.extmath as mth
import pandas as pd
from portfolio.MarketOrders import MarketOrders

class SimpleEventToMarketOrderConverter(object):
    '''
    classdocs
    '''

    def __init__(self, eventStudy, order_amount, hold_time):
        '''
        Constructor
        '''
        self.event_matrix = eventStudy.event_matrix
        self.order_amont  = order_amount
        self.hold_time    = hold_time
        (buy_orders,buy_timestamps) = self._initialize_event_orders(eventStudy.histdata.timestamps,'Buy')
        holding_time = eventStudy.histdata.timestamps[hold_time.days::]
        holding_time.extend([eventStudy.histdata.timestamps[-1]]*hold_time.days)
        (sell_orders,sell_timestamps) = self._initialize_event_orders(holding_time,'Sell')
        
        self.event_list = pd.concat([buy_orders, sell_orders],ignore_index=True)
        self.dates = buy_timestamps.tolist()
        self.dates.extend(sell_timestamps.tolist())
        
        self.event_list['Year']  = [date.year for date in self.dates]
        self.event_list['Month'] = [date.month for date in self.dates]
        self.event_list['Day']   = [date.day for date in self.dates]
        
        self.event_list['Number'] = order_amount

        
    def to_csv(self, path):
        self.event_list.to_csv(path_or_buf=path, cols=['Year','Month','Day','Symbol','Buy','Number'])
        pass
    
    def get_market_orders(self):
        return MarketOrders(dataframe=self.event_list)
    
    def _initialize_event_orders(self,timestamps,order_type):
        symb_matrix  = mth.cartesian([np.array(timestamps),self.event_matrix.columns.values])
        symb_matrix  = symb_matrix.reshape(len(timestamps),len(self.event_matrix.columns.values),2)
        order_timestamps  = symb_matrix[~np.isnan(self.event_matrix.values),0]
        order_dataframe   = pd.DataFrame(symb_matrix[~np.isnan(self.event_matrix.values),1], columns=['Symbol'] )
        order_dataframe['Buy'] = order_type
        return (order_dataframe,order_timestamps)