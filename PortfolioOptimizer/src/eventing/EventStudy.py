'''
Created on Oct 10, 2014

EventStudy inspired by the EventProfiler with the following copywrite:
    (c) 2011, 2012 Georgia Tech Research Corporation
    This source code is released under the New BSD license.  Please see
    http://wiki.quantsoftware.org/index.php?title=QSTK_License
    for license details.

Improvements made for speed, but functionality is very similar

@author: Jason
'''
from utils      import transforms     as tf
from portfolio  import HistoricalData as hs
from matplotlib import pyplot         as plt
import numpy

class EventStudy(object):
    '''
    classdocs
    '''

    def __init__(self, symbols, start_date, end_date, event_functions, benchmark=None, event_window = []):
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
        if benchmark:
            symbols.append(benchmark)
        self.histdata = hs.HistoricalData(symbols,start_date,end_date)
        self.event_matrix = self.histdata.get_close()* numpy.NaN      
        event_functions = tf.wrap(event_functions, list)
        for event_function in event_functions: 
            self.event_matrix = self.event_matrix.combine_first( event_function['func'](self.histdata,event_function['args']) )
        if len(event_window) == 2:
            (self.time, self.returns) = self.study(event_window)
        
    def study(self, event_window):
        assert len(event_window) == 2,             "event_window is not a tuple of size 2"
        assert event_window[1] >= event_window[0], "event_windwo[1] must be > event_windw[0]"
        events = self.event_matrix.copy()
        #normalize to benchmark
        benchmark_index = self.histdata.get_symbols().index(self.benchmark)
        
        returns = self.histdata.get_returns().values
        returns = (returns.T - returns.T[benchmark_index]).T
        returns = numpy.delete(returns,benchmark_index,1)
                
        del events[self.benchmark]
        #remove events which cannot be centered on a full event_window
        upper_bounds = min((-1,event_window[0]))
        lower_bounds = max((0,event_window[1]))
        events.iloc[0:lower_bounds,:]  = numpy.NaN
        events.iloc[upper_bounds:: ,:] = numpy.NaN
        #calculate number of events
        self.num_events= int(numpy.logical_not(numpy.isnan(events.values)).sum())
        assert self.num_events > 0, "Zero events in the event matrix"
        #get result data in event window
        (event_time,event_stock) = events.notnull().values.nonzero()
        event_windows = map(lambda x: range(x+event_window[0],x+event_window[1]+1),event_time)
        event_returns = numpy.ndarray((len(event_stock),event_window[1] - event_window[0] + 1))
        for i in range(0,len(event_stock)):
            event_returns[i,:] = returns.T[event_stock[i],event_windows[i]]
        #ensure data is of proper shape
        if len(event_returns.shape) == 1:
            event_returns = numpy.expand_dims(event_returns, axis=0)
        self.time    = numpy.array(range(event_window[0], event_window[1] + 1))
        self.returns = event_returns

        return (self.time, self.returns)
        
    def plot(self, b_save, filename='', output_dir = ''):
        cumret = numpy.cumprod(self.returns + 1, axis=1)
        cumret = (cumret.T / cumret[:, self.time == 0].T).T
        mean   = numpy.mean(cumret, axis=0)
        stddev = numpy.std (cumret, axis=0)
        
        plt.clf()
        plt.axhline(y=1.0, xmin=self.time[0], xmax=self.time[-1], color='k')
        plt.errorbar(self.time[self.time>0], mean[self.time>0],
                        yerr=stddev[self.time>0], ecolor='#AAAAFF', alpha=0.8)
        plt.plot(self.time, mean, linewidth=3, label='mean', color='b')
        plt.xlim(self.time[0], self.time[-1])
        plt.title('Market Relative mean return of ' + str(self.num_events) + ' events')
        plt.xlabel('Days')
        plt.ylabel('Cumulative Returns')
        if b_save:
            plt.savefig(output_dir+filename, format='pdf')
        else:
            plt.show()   
        