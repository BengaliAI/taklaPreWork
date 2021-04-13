#-*- coding: utf-8 -*-
"""
@author:MD.Nazmuddoha Ansary
"""
from __future__ import print_function
#-------------------------------------------
# imports
#-------------------------------------------
import os 
import unittest
from wordCleaner import WordCleaner
#-------------------------------------------
# global ops
#-------------------------------------------
# path to class map
class_map_csv=os.path.join(os.getcwd(),"class_map.csv")
# initialize word cleaner
WC=WordCleaner(class_map_csv) 

#-------------------------------------------
# unittestcase
#-------------------------------------------
class TestWordCleaner(unittest.TestCase):
    def test_values(self):
        '''
            test known failure cases
        '''
        # case:unwanted doubles
        ## (a)'যুুদ্ধ'==(b)'যুদ্ধ'
        self.assertEqual(WC.clean('যুুদ্ধ'),'যুদ্ধ')
        ## (a)'দুুই'==(b)'দুই'
        self.assertEqual(WC.clean('দুুই'),'দুই')
        # case:unwanted middle connector '্'  
        ## (a)'চু্ক্তি'==(b)'চুক্তি' 
        self.assertEqual(WC.clean('চু্ক্তি'),'চুক্তি')
        ## (a)'যু্ক্ত'==(b)'যুক্ত' 
        self.assertEqual(WC.clean('যু্ক্ত'),'যুক্ত')
        # case: replace broken diacritic 
        ## (a)'আরো'==(b)'আরো'
        self.assertEqual(WC.clean('আরো'),'আরো')
        
        
        # Dummy Non-Bangla,Numbers and Space cases/ Invalid start end cases
        self.assertEqual(WC.clean('ASD1234'),None)
        self.assertEqual(WC.clean('১২৩'),None)
        self.assertEqual(WC.clean('্'),None)
        
    def test_types(self):
        '''
            test the invalid input types
        '''
        # int
        self.assertRaises(TypeError,WC.clean,123)
        # float
        self.assertRaises(TypeError,WC.clean,123.456)
        # boolean
        self.assertRaises(TypeError,WC.clean,True)
        # complex
        self.assertRaises(TypeError,WC.clean,3+4j)
        # list
        self.assertRaises(TypeError,WC.clean,['যুদ্ধ','চুক্তি'])

        
        
        


        
        
        
                


                
                