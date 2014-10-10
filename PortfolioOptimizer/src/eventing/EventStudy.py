'''
Created on Oct 10, 2014

@author: Jason
'''

from portfolio import HistoricalData as hs
import qstkstudy.EventProfiler as ep
import numpy

class EventStudy(object):
    '''
    classdocs
    '''

    def __init__(self, symbols, benchmark, start_date, end_date, event_functions):
        '''
        Constructor
        event_functions is a list of dictionaries, where each entry defines:
            func: the event function to be called accepts a HistoricalData object
                  this function returns a data-frame of size num_days x num_symbols where each column is a symbol in HistoricalData.symbols,
                  each row is a timestamp in HistoricalData.timestamp
                  and each value entry is NaN for no event, or 1 for event
            args: any additional args the function needs
        '''
        self.symbols = symbols
        self.benchmark = benchmark
        symbols.append(benchmark)
        self.data = hs.HistoricalData(symbols,start_date,end_date)
        self.event_matrix = self.data.unnormalized_data['close'] * numpy.NaN
        
        if isinstance(event_functions, dict):
            event_functions_copy = event_functions
            event_functions = []
            event_functions.append(event_functions_copy)
      
        for event_function in event_functions: 
            func = event_function['func']
            args = event_function['args']
            self.event_matrix = self.event_matrix.combine_first( func(self.data,args) )
        
        self.num_events = self.event_matrix.notnull().values.nonzero()[0].shape[0]
        
    def plot(self,filename,output_dir = ''):
        ep.eventprofiler(self.event_matrix, self.data.unnormalized_data, i_lookback=20, i_lookforward=20,
                s_filename=output_dir+filename, b_market_neutral=True, b_errorbars=True,
                s_market_sym=self.benchmark)
        