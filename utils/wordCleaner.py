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
    def __init__(self,class_map_csv):
        # gets class map
        self.class_map_csv=class_map_csv
        # initializes components
        self.__getComps()
        # invalid starters
        self.inv_start=['্','়']+self.vds+self.cds
        
    def __getComps(self):
        '''
            **Private Initialization**

            reads and creates dataframe for roots,consonant_diacritic,vowel_diacritic and graphemes 
            args:
                class_map_csv        : path of classes.csv
            returns:
                tuple(df_root,df_vd,df_cd)
                df_root          :     dataframe for grapheme roots
                df_vd            :     dataframe for vowel_diacritic 
                df_cd            :     dataframe for consonant_diacritic
                
        '''
        # read class map
        df_map=pd.read_csv(self.class_map_csv)
        # get grapheme roots
        df_root = df_map.groupby('component_type').get_group('grapheme_root')
        df_root.index = df_root['label']
        df_root = df_root.drop(columns = ['label','component_type'])
        # get vowel_diacritic
        df_vd = df_map.groupby('component_type').get_group('vowel_diacritic')
        df_vd.index = df_vd['label']
        df_vd = df_vd.drop(columns = ['label','component_type'])
        # get consonant_diacritic
        df_cd = df_map.groupby('component_type').get_group('consonant_diacritic')
        df_cd.index = df_cd['label']
        df_cd = df_cd.drop(columns = ['label','component_type'])
        
        self.vds    =df_vd.component.tolist()
        self.cds    =df_cd.component.tolist()
        self.roots  =df_root.component.tolist()


    def __cleanNumbers(self):
        '''
            cleans numbers from a given word
        '''
        nms=['১','২','৩','৪','৫','৬','৭','৮','৯','০']
        for num in nms:
            if num in self.word:
                self.word=self.word.replace(num,"")
        # none case
        if not self.word.strip():
            self.return_none=True
         

    def __cleanNonBengali(self):
        '''
            cleans non-bengali symbols
        '''
        
        # this is to filter non-bengali chars
        self.decomp=regex.findall(r"[\p{Bengali}]",self.word)
        # none case
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
            * removes numbers
            * removes non-bengali symbols
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
    
        # messy checks--> needs better replacement
        self.__cleanNumbers()
        if self.return_none:
            return None


        self.__cleanNonBengali()
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