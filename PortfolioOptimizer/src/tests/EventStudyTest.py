'''
Created on Oct 10, 2014

@author: Jason
'''
import unittest
import datetime                  as dt
from eventing  import EventStudy as es
from eventing  import events
from qstkutil  import DataAccess as da

class EventStudyTest(unittest.TestCase):


    def setUp(self):
        dataobj = da.DataAccess('Yahoo')
        self.symbols = [dataobj.get_symbols_from_list('sp5002008'),dataobj.get_symbols_from_list('sp5002012')]
        self.function = [{"func": events.price_min_limit, "args": 7.0},{"func": events.price_min_limit, "args": 9.0}]
        self.testName = ['SP500-2008-PriceMinimumLimit-7','SP500-2012-PriceMinimumLimit-9']
        self.expNumEvents = [478,458]


    def tearDown(self):
        pass


    def testStudyEvent(self):
        for index in range(0, len(self.testName)):
            event = es.EventStudy(self.symbols[index],'SPY',dt.datetime(2008, 1, 1),dt.datetime(2009, 12, 31),self.function[index])
            event.plot(self.testName[index]+'.pdf', 'C:/Users/Jason/Desktop/')
            self.ValidateEvent(self.testName[index], event, self.expNumEvents[index])

    def ValidateEvent(self, test_name, event, expected_num_events):
        print "\nTesting {0}".format(test_name)  
        print "-----------------------------"
        print "Number of Events          {0}".format(event.num_events)  
        self.assertEqual(event.num_events, expected_num_events, "Number of Events {0} != {1}".format(event.num_events, expected_num_events))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testStudyEvent']
    unittest.main()