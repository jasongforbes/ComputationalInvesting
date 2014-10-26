'''
Created on Oct 10, 2014

@author: Jason
'''
import unittest
import datetime                  as dt
from eventing  import EventStudy as es
from eventing  import events
from qstkutil  import DataAccess as da
from eventing.SimpleEventToMarketOrderConverter import SimpleEventToMarketOrderConverter
from portfolio.PortfolioSimulation import PortfolioSimulation
from portfolio.PortfolioAnalyzer import PortfolioAnalyzer

class EventStudyTest(unittest.TestCase):


    def setUp(self):
        dataobj = da.DataAccess('Yahoo')
        self.symbols      = [dataobj.get_symbols_from_list('sp5002008'),     dataobj.get_symbols_from_list('sp5002012')]
        self.function     = [{"func": events.price_min_limit, "args": 5.0}, {"func": events.price_min_limit, "args": 5.0}]
        self.testName     = ['SP500-2008-PriceMinimumLimit-5',              'SP500-2012-PriceMinimumLimit-5']
        self.startDate    = [dt.datetime(2008, 1, 1),                        dt.datetime(2008, 1, 1)]
        self.endDate      = [dt.datetime(2009, 12, 31),                      dt.datetime(2009, 12, 31)]
        self.expNumEvents = [326,                                            176]


    def tearDown(self):
        pass


    def testStudyEvent(self):
        for index in range(0, len(self.testName)):
            event = es.EventStudy(self.symbols[index],self.startDate[index],self.endDate[index],self.function[index],'SPY',(-20,20))
            event.plot(True, self.testName[index]+'.pdf', 'C:/Users/Jason/Desktop/')
            self.ValidateEvent(self.testName[index], event, self.expNumEvents[index])
            
    def testToOrderCsv(self):
        for index in range(0, len(self.testName)):
            print "\nTesting {0} strategy".format(self.testName[index])  
            study = es.EventStudy(self.symbols[index],start_date=self.startDate[index], end_date=self.endDate[index], event_functions=self.function[index])
            converter = SimpleEventToMarketOrderConverter(study, 100, dt.timedelta(days=5))
            print "Generating csv of orders...."
            converter.to_csv("../../Resources/" + self.testName[index] + ".csv")
            print "Simulating portfolio...."
            portfolio_sim = PortfolioSimulation(converter.get_market_orders(),50000)
            print "Analyzing portfolio...."
            analyzer = PortfolioAnalyzer()
            analyzer.analyze(portfolio_sim, "$SPX", self.testName[index])
              

    def ValidateEvent(self, test_name, event, expected_num_events):
        print "\nTesting {0}".format(test_name)  
        print "-----------------------------"
        print "Number of Events          {0}".format(event.num_events)  
        self.assertEqual(event.num_events, expected_num_events, "Number of Events {0} != {1}".format(event.num_events, expected_num_events))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testStudyEvent']
    unittest.main()