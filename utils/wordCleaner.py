#-*- coding: utf-8 -*-
"""
@author:MD.Nazmuddoha Ansary
"""
from __future__ import print_function
#-------------------------------------------
# imports
#-------------------------------------------
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
                    'ূ', 'ৃ', 'ে', 'ৈ', 'ো', 'ৌ',
                    '্', 'ৎ', 'ড়', 'ঢ়', 'য়','\u200d']
        
        self.vowels=['অ', 'আ', 'ই', 'ঈ', 'উ', 'ঊ', 'ঋ', 'এ', 'ঐ', 'ও', 'ঔ']
        # invalid starters
        self.inv_start=['্','়']+self.vds+self.cds
        # invalid hosonto cases
        self.inv_hosonto_before=self.vowels+['্']
        self.inv_hosonto_after=self.inv_hosonto_before+['ঁ', 'ং', 'ঃ']
        
    def __replaceDiacritics(self):
        '''
            case: replace  diacritic 
                # Example-1: 
                (a)'আরো'==(b)'আরো' ->  False 
                    (a) breaks as:['আ', 'র', 'ে', 'া']
                    (b) breaks as:['আ', 'র', 'ো']
                # Example-2:
                (a)পৌঁছে==(b)পৌঁছে ->  False
                    (a) breaks as:['প', 'ে', 'ৗ', 'ঁ', 'ছ', 'ে']
                    (b) breaks as:['প', 'ৌ', 'ঁ', 'ছ', 'ে']
                # Example-3:
                (a)সংস্কৄতি==(b)সংস্কৃতি ->  False
                    (a) breaks as:['স', 'ং', 'স', '্', 'ক', 'ৄ', 'ত', 'ি']
                    (b) breaks as:['স', 'ং', 'স', '্', 'ক', 'ৃ', 'ত', 'ি']
                
                            
        '''
        # broken vowel diacritic
        # e-kar+a-kar = o-kar
        self.word = self.word.replace('ে'+'া', 'ো')
        # e-kar+e-kar = ou-kar
        self.word = self.word.replace('ে'+'ৗ', 'ৌ')
        # 'অ'+ 'া'-->'আ'
        self.word = self.word.replace('অ'+ 'া','আ')
        # unicode normalization of 'ৄ'-> 'ৃ'
        self.word = self.word.replace('ৄ','ৃ')
        
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
        while self.decomp[-1] == '্':
            self.decomp=self.decomp[:-1]
            if not self.__checkDecomp():
                self.return_none=True
                break 


    def __cleanInvalidStarts(self):
        '''
            cleans a word that has invalid starting
        '''
        if self.decomp[0] in self.inv_start:
            self.return_none=True
            

    def __cleanInvalidNuktaChars(self):
        '''
            handles nukta unicode as follows:
                * If the connecting char is with in the valid list ['য','ব','ড','ঢ'] then replace with ['য়','র','ড়', 'ঢ়']
                * Otherwise remove the nukta char completely
            **the connecting char**: is defined as the previous non-vowle-diacritic char 
            Example-1:If case-1
            (a)কেন্দ্রীয়==(b)কেন্দ্রীয় ->  False
                (a) breaks as:['ক', 'ে', 'ন', '্', 'দ', '্', 'র', 'ী', 'য', '়']
                (b) breaks as:['ক', 'ে', 'ন', '্', 'দ', '্', 'র', 'ী', 'য়']
            Example-2:Elif case-2
            (a)রযে়ছে==(b)রয়েছে ->  False
                (a) breaks as:['র', 'য', 'ে', '়', 'ছ', 'ে']
                (b) breaks as:['র', 'য়', 'ে', 'ছ', 'ে']
            Example-3:Otherwise 
            (a)জ়ন্য==(b)জন্য ->  False
                (a) breaks as:['জ', '়', 'ন', '্', 'য']
                (b) breaks as:['জ', 'ন', '্', 'য']
        '''            
        __valid_chars =['য','ব','ড','ঢ']
        __replacements=['য়','র','ড়','ঢ়']
        for idx,d in enumerate(self.decomp):
            if d=='়':
                check=False
                # check the precedding char
                if self.decomp[idx-1] in __valid_chars:
                    cid=idx-1
                    check=True
                # check the previous char before vowel diacritic
                elif idx>2 and self.decomp[idx-2] in __valid_chars and self.decomp[idx-1] in self.vds:
                    cid=idx-2
                    check=True
                else:
                    self.decomp.remove(d)
                    if not self.__checkDecomp():
                        self.return_none=True
                        break        

                if check:
                    rep_char_idx=__valid_chars.index(self.decomp[cid])
                    # replace
                    self.decomp[cid]=__replacements[rep_char_idx]
                    self.decomp.remove(d)
                    if not self.__checkDecomp():
                        self.return_none=True
                        break        

    def __cleanInvalidHosontoForVowels(self):
        '''
            take care of the in valid hosontos that come after / before the vowels and the 'ঁ', 'ং', 'ঃ'
            # Example-1:
            (a)দুই্টি==(b)দুইটি-->False
                (a) breaks as ['দ', 'ু', 'ই', '্', 'ট', 'ি']
                (b) breaks as ['দ', 'ু', 'ই', 'ট', 'ি']
            # Example-2:
            (a)এ্তে==(b)এতে-->False
                (a) breaks as ['এ', '্', 'ত', 'ে']
                (b) breaks as ['এ', 'ত', 'ে']
            # Example-3:
            (a)নেট্ওয়ার্ক==(b)নেটওয়ার্ক-->False
                (a) breaks as ['ন', 'ে', 'ট', '্', 'ও', 'য়', 'া', 'র', '্', 'ক']
                (b) breaks as ['ন', 'ে', 'ট', 'ও', 'য়', 'া', 'র', '্', 'ক']
            # Example-4:
            (a)এস্আই==(b)এসআই-->False
                (a) breaks as ['এ', 'স', '্', 'আ', 'ই']
                (b) breaks as ['এ', 'স', 'আ', 'ই']
        '''
        for idx,d in enumerate(self.decomp):
            if d=='্':
                # after case: where the hosonto cant be valid 
                if self.decomp[idx-1] in self.inv_hosonto_after and self.decomp[idx+1]!='য':
                    self.decomp.remove(d)
                    # break case
                    if not self.__checkDecomp():
                        self.return_none=True
                        break
                # before case
                elif idx+1<len(self.decomp) and self.decomp[idx+1] in self.inv_hosonto_before:
                    self.decomp.remove(d)
                    # break case
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

    def __cleanDoubleDiacritics(self):
        '''
            case:invalid consecutive vowel diacritics  
            * since there is no way to ensure which one is right it simply returns none                
        '''
        for idx,d in enumerate(self.decomp):
            if idx<len(self.decomp)-1 and  d in self.vds and self.decomp[idx+1] in self.vds:
                self.return_none=True
                break
                    
    def __cleanVowelDiacsWithVowels(self):
        '''
            takes care of vowels followed by vowel diacritics
            # Example-1:
            (a)উুলু==(b)উলু-->False
                (a) breaks as ['উ', 'ু', 'ল', 'ু']
                (b) breaks as ['উ', 'ল', 'ু']
            # Example-2:
            (a)আর্কিওোলজি==(b)আর্কিওলজি-->False
                (a) breaks as ['আ', 'র', '্', 'ক', 'ি', 'ও', 'ো', 'ল', 'জ', 'ি']
                (b) breaks as ['আ', 'র', '্', 'ক', 'ি', 'ও', 'ল', 'জ', 'ি']
            # Example-3:
            ### Normalizes 'এ' and 'ত্র'
            (a)একএে==(b)একত্রে-->False
                (a) breaks as ['এ', 'ক', 'এ', 'ে']
                (b) breaks as ['এ', 'ক', 'ত', '্', 'র', 'ে']

        '''
        for idx,d in enumerate(self.decomp):
            if  d in self.vds and self.decomp[idx-1] in self.vowels:
                if self.decomp[idx-1] !='এ':
                    self.decomp.remove(d)
                    # break case
                    if not self.__checkDecomp():
                        self.return_none=True
                        break
                else:
                    self.decomp[idx-1:idx]='ত', '্', 'র'

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
            * handles diacritics
            * removes numbers and non-bengali symbols
            * removes invalid starter symbols
            * removes invalid nukta symbols and normalizes the unicode
            * removes invalid ending symbols
            * removes consecutive doubles of vds and cds
            * removes unwanted connectors in between vds
        '''
        if not isinstance(word, str):
            raise TypeError("The provided argument/ word is not a string") 
        self.word=word
        # None-flag
        self.return_none = False
        # replace Diacritics
        self.__replaceDiacritics()
        # create clean decomp
        self.__createDecomp()
        if self.return_none:
            return None
        
        # list of operations
        ops=[self.__cleanInvalidEnds,
             self.__cleanInvalidStarts,
             self.__cleanVowelDiacsWithVowels,
             self.__cleanInvalidNuktaChars,
             self.__cleanInvalidHosontoForVowels,
             self.__cleanDoubleDecomp,
             self.__cleanConnector,
             self.__cleanDoubleDiacritics,
             self.__reconstructDecomp]

        for op in ops:
            if not self.__checkOp(op):
                return None
        
        return self.word