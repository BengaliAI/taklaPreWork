# -*-coding: utf-8 -
'''
    @author: Ashif Sushmit,MD. Nazmuddoha Ansary
'''
#---------------------------------------------------------------------------------------
# imports
#---------------------------------------------------------------------------------------
import re 
import random
import numpy as np
import pandas as pd
import json

from gps import GraphemeParser
from wordCleaner import WordCleaner 
#---------------------------------------------------------------------------------------
# takla generator class
#---------------------------------------------------------------------------------------

class TalkaGenerator(object):
    def __init__(self,map_json,translit_json,class_map_csv):
        '''
            The takla generation class
            args:
                map_json      =  the takla converter json map
                translit_json =  the transliteration json map
                class_map_csv =  the csv file to initialize grapheme parser
        '''
        # initialize resources
        with open(map_json) as f:
            self.map = json.load(f)
        with open(translit_json) as f:
            self.translit=json.load(f)
        self.en_vocab=sorted(self.translit.keys())
        # class initialization
        self.grapheme_parser=GraphemeParser(class_map_csv)
        self.word_cleaner=WordCleaner()
        # globals
        self.vowels=["a","e","i","o","u"]

        
    def __taklization(self,word):
        '''
            creates takla counter part of a word from a given map
        '''
        graphemes = self.grapheme_parser.word2grapheme(word)
        takla = "".join([self.map[grapheme] for grapheme in graphemes])
        return takla

    def __convertStandard(self):
        '''
            converts a bangla sentence 
        '''
        standard=[]
        words   =[]
        for word in self.sentence.split():
            # ensure non-space and string
            word=str(word)
            word=word.strip()
            # passing type and value unit test
            if len(word)>0:
                # clean the word
                word=self.word_cleaner.clean(word)
            
                # check transliteration cases
                if word is not None:
                    words.append(word)
                    if word in self.en_vocab:
                        standard.append(self.translit[word]) 
                    else:
                        #print('ov', each)
                        standard.append(self.__taklization(word)) 
        
        self.data=pd.DataFrame({"word":words,"standard":standard})
        self.words=words
        self.standard=standard
    
    def __removeEndingPhone(self):
        '''
            removes o from words that doesnot end with O-kar
        '''
        phoneRemoved=[]
        for word,takla in zip(self.words,self.standard):
            if word[-1] not in ['ো','ও'] and takla[-1]=="o":
                phoneRemoved.append(takla[:-1])
            else:
                phoneRemoved.append(takla)

        self.data["standard"]=phoneRemoved

    def __vowelChange(self):
        '''
            first degree vowel change:
        '''
        # private lambda
        def __lambda(x):
            # start and end
            maps={"e":"a",
                  "i":"e",
                  "o":"a"}
            
            # make list
            x=list(x)
            # start
            if x[0] in maps.keys() and x[1] not in self.vowels:
                x[0]=maps[x[0]]
            # end
            if x[-1] in maps.keys() and x[-2] not in self.vowels:
                x[-1]=maps[x[-1]]
            # middle
            maps={"a":"u",
                  "e":"a",
                  "i":"e",
                  "o":"a",
                  "u":"a"}
            
            for idx,c in enumerate(x):
                # for middle ones
                if idx>0 and idx<len(x)-1:
                    # consecutive vowel
                    if x[idx-1] not in self.vowels and x[idx+1] not in self.vowels and c in maps.keys():
                        x[idx]=maps[c] 

            # double
            x="".join(x)
            maps={"aa":"a",
                  "ai":"ae",
                  "ao":"au",
                  "au":"ao",
                  "ee":"e",
                  "ei":"ae",
                  "eo":"eu",
                  "eu":"eo",
                  "ie":"iye",
                  "io":"eo",
                  "ii":"i",
                  "iu":"ew",
                  "oa":"ua",
                  "oe":"oi",
                  "oi":"oy",
                  "oo":"o",
                  "ou":"ow",
                  "ua":"o",
                  "ui":"e",
                  "uo":"o",
                  "uu":"u"}

            for _map in maps.keys():
                x.replace(_map,maps[_map])

            return x

        self.data["FVC"]=self.data.standard.apply(lambda x: __lambda(x))

    
    
    def createTakla(self,sentence):
        '''
            creates takla from a given sentence
        '''
        self.sentence=sentence
        # convert standard
        self.__convertStandard()
        # remove ending phone
        #self.__removeEndingPhone()
        # initial vowel 1st degree
        self.__vowelChange()
    

        

# #---------------------------------------------------------------------------------------
# # globals
# #---------------------------------------------------------------------------------------

# gaps=['b','c','f','g','j','k','p','q','s','v','x','z']
# reps=[['b','v'],
#       ['c','c','c','s','s','k'],
#       ['f','p'],
#       ['g','g','j','z'],
#       ['j','j','g','z'],
#       ['k','k','q','c'],
#       ['p','f'],
#       ['q','q','k','c'],
#       ['s','s','c'],
#       ['v','v','b'],
#       ['x','x','x','x','eks','aks','acs','ecs'],
#       ['z','z','g','j']]
      
# sem_vowels='aeiouwy'
# CHARS  = ["a","e","i","o","u","","",""]

# #---------------------------------------------------------------------------------------
# # helpers
# #---------------------------------------------------------------------------------------


# def random_generator(vowels):
#     rand  = np.random.rand(1)
#     if rand<0.5:
#         return random.choice(vowels)
#     else:
#         return "".join(random.choices(vowels, k=2))
# #---------------------------------------------------------------------------------------
# # ops
# #---------------------------------------------------------------------------------------

# def VC(text):
#     return re.sub(f'[{sem_vowels}]', lambda L: random.choice(sem_vowels), text, flags=re.I)

# def VA(text):
#     return re.sub(f'[{sem_vowels}]', lambda L: random_generator(sem_vowels),text , flags=re.I)

# def VR(text):
#     return re.sub(f'[{sem_vowels}]', lambda L: random.choice(CHARS),text , flags=re.I)

# def THR(text):
#     return re.sub("[h]",lambda L: random.choice(["h","h","","",""]),text)     

# def RPSS(text):
#     for gap,rep in zip(gaps,reps): 
#         text=re.sub(f"[{gap}]",lambda L: random.choice(rep),text)
#     return text

# OPS=[VC,VA,VR,THR,RPSS]
# #---------------------------------------------------------------------------------------
# # wrapper
# #---------------------------------------------------------------------------------------

# def create_takla(text,num_ops=1):
#     '''
#         creates a takla based on given text and number of random operations
#         args:
#             text    :    Romanized Standard Text
#             num_ops :    the time of random operations to occur
#         returns:
#             takla text (as generated)
#     '''
#     for i in range(num_ops):
#         text=random.choice(OPS)(text)
#     return text

