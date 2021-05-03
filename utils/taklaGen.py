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
                x[0]=random.choice([maps[x[0]],x[0]])
            # end
            if x[-1] in maps.keys() and x[-2] not in self.vowels:
                x[-1]=random.choice([maps[x[-1]],x[-1]])
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
                        x[idx]=random.choice([maps[c],c]) 

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
                x.replace(_map,random.choice([maps[_map],_map]))

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
        self.__removeEndingPhone()
        # initial vowel 1st degree
        self.__vowelChange()
    
#---------------------------------------------------------------------------------------
# random gen
#---------------------------------------------------------------------------------------

        
class RandomTaklaGenerator(object):
    def __init__(self):
        self.gaps=['b','c','f','g','j','k','p','q','s','v','x','z']
        self.reps= [['b','v'],
                    ['c','c','c','s','s','k'],
                    ['f','p'],
                    ['g','g','j','z'],
                    ['j','j','g','z'],
                    ['k','k','q','c'],
                    ['p','f'],
                    ['q','q','k','c'],
                    ['s','s','c'],
                    ['v','v','b'],
                    ['x','x','x','x','eks','aks','acs','ecs'],
                    ['z','z','g','j']]
            
        self.vowels='aeiou'
        self.CHARS  = ["a","e","i","o","u","","",""]

#---------------------------------------------------------------------------------------
# helpers
#---------------------------------------------------------------------------------------


    def random_generator(self):
        rand  = np.random.rand(1)
        if rand<0.5:
            return random.choice(self.vowels)
        else:
            return "".join(random.choices(self.vowels, k=2))
#---------------------------------------------------------------------------------------
# ops
#---------------------------------------------------------------------------------------

    def VC(self):
        return re.sub(f'[{self.vowels}]', lambda L: random.choice(self.vowels), self.text, flags=re.I)

    def VA(self):
        return re.sub(f'[{self.vowels}]', lambda L: self.random_generator(),self.text , flags=re.I)

    def VR(self):
        return re.sub(f'[{self.vowels}]', lambda L: random.choice(self.CHARS),self.text , flags=re.I)

    def THR(self):
        return re.sub("[h]",lambda L: random.choice(["h","h","","",""]),self.text)     

    def RPSS(self):
        for gap,rep in zip(self.gaps,self.reps): 
            self.text=re.sub(f"[{gap}]",lambda L: random.choice(rep),self.text)
        return self.text


#---------------------------------------------------------------------------------------
# wrapper
#---------------------------------------------------------------------------------------

    def create_takla(self,
                    text,
                    num_samples,
                    num_max_ops,
                    num_max_degree):
        '''
            creates a takla based on given text and number of random operations
            args:
                text            :   Romanized Standard text
                num_samples     :   Number of samples to generate
                num_max_ops     :   the time of random operations to occur at one occurance
                num_max_degree  :   the number of sequence of operations
            returns:
                takla text (as generated)
        '''
        takla_list=[]
        for _ in range(num_samples):
            self.text=text
            
            # degree / sequence of ops
            degree=random.randint(1,num_max_degree)
            
            for _ in range(degree):
                # take number of operations
            
                nops=random.randint(1,num_max_ops) 
            
                OPS=[self.VC,self.VA,self.VR,self.THR,self.RPSS]
            
                random.shuffle(OPS)
                for i in range(nops):
                    self.text=OPS[i]()
            # append
            takla_list.append(self.text)
        return takla_list
