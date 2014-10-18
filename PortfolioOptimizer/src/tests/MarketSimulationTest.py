'''
Created on Oct 18, 2014

@author: Jason
'''
import unittest
import datetime as dt
from portfolio import MarketOrders as mo


class MarketSimulationTest(unittest.TestCase):

    def setUp(self):
        '''                   csv_files                     start-date         end-date                 symbols               '''
        self.test_data = [('../../Resources/orders.csv', dt.date(2011,1,10), dt.date(2011,12,20), ['AAPL','IBM','GOOG','XOM']) \
                          ]
        pass


    def tearDown(self):
        pass
    
    def testLoading(self):
        for csvfile,startdate,enddate,symb in self.test_data:
            orders = mo.MarketOrders(csvfile)
            self.assertEqual(startdate, orders.start_date(), "start date {0} != {1}".format(startdate,orders.start_date()))
            self.assertEqual(enddate,   orders.end_date(), "end date {0} != {1}".format(enddate,orders.end_date()))
            self.assertTrue(len(symb) == len(orders.symbols()) and sorted(symb) == sorted(orders.symbols()), "Symbols are not as expected")
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'MarketSimulationTest.testLoading']
    unittest.main()