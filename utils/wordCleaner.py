#-*- coding: utf-8 -*-
"""
@author:MD.Nazmuddoha Ansary
"""
from __future__ import print_function
#-------------------------------------------
# imports
#-------------------------------------------
import regex
import pandas as pd
#-------------------------------------------
# cleaner class
#-------------------------------------------
class WordCleaner(object):
    def __init__(self):
        # comps    
        self.vds    =['া', 'ি', 'ী', 'ু', 'ূ', 'ৃ', 'ে', 'ৈ', 'ো', 'ৌ']
        self.cds    =['ঁ', 'র্', 'র্য', '্য', '্র', '্র্য', 'র্্র']
        # chars
        self.chars  =['ঁ', 'ং', 'ঃ', 'অ', 'আ', 'ই', 'ঈ', 'উ', 'ঊ', 'ঋ', 'এ', 
                    'ঐ', 'ও', 'ঔ', 'ক', 'খ', 'গ', 'ঘ', 'ঙ', 'চ', 'ছ', 
                    'জ', 'ঝ', 'ঞ', 'ট', 'ঠ', 'ড', 'ঢ', 'ণ', 'ত', 'থ', 
                    'দ', 'ধ', 'ন', 'প', 'ফ', 'ব', 'ভ', 'ম', 'য', 'র', 
                    'ল', 'শ', 'ষ', 'স', 'হ', '়', 'া', 'ি', 'ী', 'ু', 
                    'ূ', 'ৃ', 'ে', 'ৈ', 'ো', 'ৌ', '্', 'ৎ', 'ড়', 'ঢ়', 'য়','\u200d']
        # invalid starters
        self.inv_start=['্','়']+self.vds+self.cds
        
    def __replaceBroken(self):
        '''
            case: replace broken diacritic 
                # Example-1: 
                (a)'আরো'==(b)'আরো' ->  False 
                    (a) breaks as:['আ', 'র', 'ে', 'া']
                    (b) breaks as:['আ', 'র', 'ো']
                # Example-2:
                (a)'বোধগম্য'==(b)'বোধগম্য' ->   False
                    (a) breaks as:['ব', 'ে', 'া', 'ধ', 'গ', 'ম', '্', 'য']
                    (b) breaks as:['ব', 'ো', 'ধ', 'গ', 'ম', '্', 'য']
            
        '''
        # broken vowel diacritic
        # e-kar+a-kar = o-kar
        self.word = self.word.replace('ে'+'া', 'ো')
        # e-kar+e-kar = ou-kar
        self.word = self.word.replace('ে'+'ৗ', 'ৌ')

    def __createDecomp(self):
        # remove non-bengali unicode
        self.decomp=[ch for ch in self.word if ch in self.chars]
        if not self.__checkDecomp():
            self.return_none=True

    def __checkDecomp(self):
        '''
            checks if the decomp has a valid length
        '''
        if len(self.decomp)>0:
            return True
        else:
            return False

    def __cleanInvalidEnds(self):
        '''
            cleans a word that has invalid ending i.e ends with '্' that does not make any sense
        '''
        while self.decomp[-1] is '্':
            del self.decomp[-1]
            if not self.__checkDecomp():
                self.return_none=True
                break 


    def __cleanInvalidStarts(self):
        '''
            cleans a word that has invalid starting
        '''
        while self.decomp[0] in self.inv_start:
            del self.decomp[0]
            if not self.__checkDecomp():
                self.return_none=True
                break

    def __cleanDoubleDecomp(self):
        '''
            take care of doubles(consecutive doubles): proposed for vd and cd only
            removes unwanted doubles(consecutive doubles):
            
            case:unwanted doubles  
                # Example-1: 
                (a)'যুুদ্ধ'==(b)'যুদ্ধ' ->  False 
                    (a) breaks as:['য', 'ু', 'ু', 'দ', '্', 'ধ']
                    (b) breaks as:['য', 'ু', 'দ', '্', 'ধ']
                # Example-2:
                (a)'দুুই'==(b)'দুই' ->   False
                    (a) breaks as:['দ', 'ু', 'ু', 'ই']
                    (b) breaks as:['দ', 'ু', 'ই']

                # Example-3:
                (a)'প্রকৃৃতির'==(b)'প্রকৃতির' ->   False
                    (a) breaks as:['প', '্', 'র', 'ক', 'ৃ', 'ৃ', 'ত', 'ি', 'র']
                    (b) breaks as:['প', '্', 'র', 'ক', 'ৃ', 'ত', 'ি', 'র']
            
        '''
        for idx,d in enumerate(self.decomp):
            # if its not the last one and it is in cd or vd and the next symbol is as same as the current one 
            # remove current symbol    
            if d in self.vds+self.cds and idx<len(self.decomp)-1 and self.decomp[idx+1]==d:
                self.decomp.remove(d)
                # break case
                if not self.__checkDecomp():
                    self.return_none=True
                    break

    
    def __cleanConnector(self):
        '''
            removes unwanted connectors:
            * if the '্' is in between any VDS remove it 
            
            case:unwanted middle connector '্'  
                # Example-1: 
                (a)'চু্ক্তি'==(b)'চুক্তি' ->  False 
                    (a) breaks as:['চ', 'ু', '্', 'ক', '্', 'ত', 'ি']
                    (b) breaks as:['চ', 'ু','ক', '্', 'ত', 'ি']
                # Example-2:
                (a)'যু্ক্ত'==(b)'যুক্ত' ->   False
                    (a) breaks as:['য', 'ু', '্', 'ক', '্', 'ত']
                    (b) breaks as:['য', 'ু', 'ক', '্', 'ত']

                # Example-3:
                (a)'কিছু্ই'==(b)'কিছুই' ->   False
                    (a) breaks as:['ক', 'ি', 'ছ', 'ু', '্', 'ই']
                    (b) breaks as:['ক', 'ি', 'ছ', 'ু','ই']
            
        '''
        connector= '্'
        # remove middle connectors 
        for idx,d in enumerate(self.decomp):
            # if not last char
            if d==connector and idx<len(self.decomp)-1:
                if self.decomp[idx-1] in self.vds or self.decomp[idx+1] in self.vds:
                    del self.decomp[idx]
                    # break case
                    if not self.__checkDecomp():
                        self.return_none=True
                        break



    def __reconstructDecomp(self):
        '''
            reconstructs the word from decomp
        '''
        self.word=''
        for ch in self.decomp:
            self.word+=ch 

    def __checkOp(self,op):
        '''
            execute an operation with  checking and None return
            args:
                opname : the function to execute
        '''
        if self.__checkDecomp():
            op()
            if self.return_none:
                return False
            else:
                return True
        else:
            return False
        
    
    def clean(self,word):
        '''
            cleans a given word
            * handles broken diacritics
            * removes numbers and non-bengali symbols
            * removes invalid starter symbols
            * removes invalid ending symbols
            * removes consecutive doubles of vds and cds
            * removes unwanted connectors in between vds
        '''
        if not isinstance(word, str):
            raise TypeError("The provided argument/ word is not a string") 
        self.word=word
        # None-flag
        self.return_none = False
        # replace broken 
        self.__replaceBroken()
        # create clean decomp
        self.__createDecomp()
        if self.return_none:
            return None
        
        # list of operations
        ops=[self.__cleanInvalidEnds,
             self.__cleanInvalidStarts,
             self.__cleanDoubleDecomp,
             self.__cleanConnector,
             self.__reconstructDecomp]

        for op in ops:
            if not self.__checkOp(op):
                return None
        
        return self.word