'''
Created on Nov 2, 2014

@author: Jason
'''
import unittest

from portfolio import BollingerBands as bb
from portfolio import HistoricalData as hd
import datetime as dt

class BollingerTest(unittest.TestCase):

    def setUp(self):
        '''                 name            period         start-date            end-date                 symbols               '''
        self.test_data = [('test1',          20,       dt.date(2010,1,1),  dt.date(2010,12,31), ['AAPL','GOOG','IBM','MSFT']) \
                          ]
        pass
    
    def tearDown(self):
        pass

    def testBollingerBand(self):
        for name,period,start_date,end_date,symbols in self.test_data:
            print "-----Starting {0} -----------------------".format(name)
            histData = hd.HistoricalData(symbols, start_date, end_date)
            bollinger = bb.BollingerBands(histData,period)
            print bollinger.get_bollinger_values()[:][-6:]
            bollinger.plot(symbols[0], title=name)
        pass
    
    def testBollingerBandSpecificDate(self):
        print "-----Starting quiz -----------------------"
        for name,period,start_date,end_date,symbols in self.test_data:
            histData = hd.HistoricalData(symbols, start_date, end_date)
            bollinger = bb.BollingerBands(histData,period)
            print bollinger.get_bollinger_values()['AAPL'][bollinger.get_bollinger_values()['AAPL'].index.date == dt.date(2010,6,14)]
            print bollinger.get_bollinger_values()['MSFT'][bollinger.get_bollinger_values()['MSFT'].index.date == dt.date(2010,5,21)]


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'BollingerTest.testBollingerBand']
    unittest.main()