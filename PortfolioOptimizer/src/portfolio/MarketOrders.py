'''
Created on Oct 18, 2014

@author: Jason
'''
import datetime as dt
import numpy as np
from pandas.io import parsers as io

class MarketOrders(object):
    '''
    classdocs
    '''
    keys = ['Year','Month','Day','Symbol','Buy','Number']

    def __init__(self, csv_filepath):
        '''
        Constructor
        '''
        self.orders=io.read_csv(csv_filepath, header=None, names=self.keys,index_col=False)
        self.orders['Date'] = [dt.date(year,month,day) for (year,month,day) in zip(self.orders['Year'].values,self.orders['Month'].values,self.orders['Day'].values)]
        self.orders['Buy'].replace(to_replace='Buy',  value=1,  inplace=True)
        self.orders['Buy'].replace(to_replace='Sell', value=-1, inplace=True)
        
    def start_date(self):
        return np.min(self.orders['Date'].values)
    
    def end_date(self):
        return np.max(self.orders['Date'].values)
    
    def symbols(self):
        return list(set(self.orders['Symbol'].values))