'''
Created on Oct 18, 2014

@author: Jason
'''
import unittest
import datetime as dt
from portfolio import PortfolioAnalyzer as az
from portfolio import MarketOrders as mo
from portfolio import PortfolioSimulation as ps


class MarketSimulationTest(unittest.TestCase):

    def setUp(self):
        '''                   csv_files                                    output                    start-date         end-date                 symbols               '''
        self.test_data = [('../../Resources/orders.csv',       '../../Resources/output.csv',       dt.date(2011,1,10), dt.date(2011,12,20), ['AAPL','IBM','GOOG','XOM']), \
                          ('../../Resources/orders-short.csv', '../../Resources/output-short.csv', dt.date(2011,1,5),  dt.date(2011,1,20),  ['AAPL']), \
                          ('../../Resources/orders2.csv',       '../../Resources/output2.csv',     dt.date(2011,1,14), dt.date(2011,12,14), ['AAPL','IBM','GOOG','XOM']) \
                          ]


    def tearDown(self):
        pass
    
    def testLoadingCsv(self):
        for csvfile,outputcsv,startdate,enddate,symb in self.test_data:
            orders = mo.MarketOrders(csvfile)
            self.assertEqual(startdate, orders.start_date(), "start date {0} != {1}".format(startdate,orders.start_date()))
            self.assertEqual(enddate,   orders.end_date(), "end date {0} != {1}".format(enddate,orders.end_date()))
            self.assertTrue(len(symb) == len(orders.symbols()) and sorted(symb) == sorted(orders.symbols()), "Symbols are not as expected")
    
    def testPortfolioSimulation(self):
         for csvfile, outputcsv, startdate, enddate, symb in self.test_data:
            orders = mo.MarketOrders(csvfile)
            portfolio = ps.PortfolioSimulation(orders,1000000)
            portfolio.to_csv(outputcsv)

    def testPortfolioAnalyzer(self):
         for csvfile, outputcsv, startdate, enddate, symb in self.test_data:
            orders = mo.MarketOrders(csvfile)
            portfolio = ps.PortfolioSimulation(orders,1000000)
            az.PortfolioAnalyzer().analyze(portfolio,'$SPX')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'MarketSimulationTest.testLoadingCsv']
    unittest.main()