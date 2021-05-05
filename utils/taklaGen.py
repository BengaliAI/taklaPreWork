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
        # operations maps
        self.ops_map={"VC"      :self.__vowelChange,
                      "VR"      :self.__vowelRemoval,
                      "THR"     :self.__removeH,
                      "RPSS"    :self.__replaceConsonants,
                      "SHORT"   :self.__shotenWords}

        
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

        self.data["standard"]=phoneRemoved# operations maps

    def __vowelChange(self,x):
        '''
            first degree vowel change:
        '''
        # start and end
        maps={"e":"a",
                "i":"e",
                "o":"a"}
        
        # make list
        x=list(x)
        
        if len(x)>1:
            # start
            if x[0] in maps.keys() and x[1] not in self.vowels:
                x[0]=random.choice([maps[x[0]],x[0]])
            # end
            if x[-1] in maps.keys() and x[-2] not in self.vowels:
                x[-1]=random.choice([maps[x[-1]],x[-1]])
            # middle
            maps={"a":"u",
                    "e":"a",# operations maps
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
        else:
            return random.choice([maps[x[0]],x[0]])

        
    def __shotenWords(self,x):
        '''
            removes the vowels
        '''
        # make list
        x=list(x)
        for idx,c in enumerate(x):
            if idx>0 and idx!=len(x)-1:
                if c in self.vowels:
                    x[idx]=None
        x=[i for i in x if i is not None]
        x="".join(x)
        return x
    
    def __removeH(self,x):
        '''
            removes trailing H 
        '''
        # make list
        x=list(x)
        for idx,c in enumerate(x):
            if idx>0 and c=="h":
                x[idx]=random.choice(["","h"])
        x="".join(x)
        return x
    
    def __vowelRemoval(self,x):
        '''
            removes the vowels but at random
        '''
        # make list
        x=list(x)
        for idx,c in enumerate(x):
            if idx>0 and idx!=len(x)-1:
                if c in self.vowels and np.random.rand(1)<0.5:
                    x[idx]=None
        x=[i for i in x if i is not None]
        x="".join(x)
        return x
    
    
    def __replaceConsonants(self,x):
        '''
            replace consonants
        '''
        maps_alt={"c":["s","ss"],
                  "ch":["s","ss"],
                  "s":["c","ch"]}
                  
        maps={"j":"z",
              "ph":"f",
              "z":"j",
              "f":"ph"}
        # optional replacements
        _x=[]
        for c in x:
            if c not in maps_alt.keys():
                _x.append(c)
            else:
                _x.append(random.choice(maps_alt[c]))
        x="".join(_x)

        # directs
        _x=[]
        for c in x:
            if c not in list(maps.keys()):
                _x.append(c)
            else:
                _x.append(random.choice([c,maps[c]]))
        x="".join(_x)

        return x 


    def createTakla(self,
                    sentence,
                    execute_single_ops=False,
                    randomize_ops=False,
                    operations=["VC","THR","RPSS"]):
        '''
            creates takla from a given sentence
            args:
                sentence            :   a pure bangla sentence 
                execute_single_ops  :   execute separate operations separately
                randomize_ops       :   randomly select operations 
                                        This flag overides selective operations data
                operations          :   the operations to be done: 
                                        allowed operations:VC,VR,THR,RPSS,SHORT

        '''
        results={}
        self.sentence=sentence
        results["bangla"]=sentence
        # convert standard
        self.__convertStandard()
        results["standard_takla"]=" ".join(self.data.standard.tolist())
        # remove ending phone
        # self.__removeEndingPhone()
        
        
        
        # initial vowel 1st degree
        if execute_single_ops:
            self.data["VC"]=self.data.standard.apply(lambda x: self.__vowelChange(x))
            results["vowel_change"]=" ".join(self.data.VC.tolist())
            
            # vowel removal
            self.data["VR"]=self.data.standard.apply(lambda x: self.__vowelRemoval(x))
            results["vowel_removal"]=" ".join(self.data.VR.tolist())

            # h removal
            self.data["THR"]=self.data.standard.apply(lambda x: self.__removeH(x))
            results["h_reduction"]=" ".join(self.data.THR.tolist())

            # replace consonants
            self.data["RPSS"]=self.data.standard.apply(lambda x: self.__replaceConsonants(x))
            results["consonant_replacement"]=" ".join(self.data.RPSS.tolist())

            # shorten the word
            self.data["SHORT"]=self.data.standard.apply(lambda x: self.__shotenWords(x))
            results["pure_shorthand"]=" ".join(self.data.SHORT.tolist())
            
        if randomize_ops:
            colname="randomComb"
            self.data[colname]=self.data.standard.tolist()
            
            # operations
            ops=list(self.ops_map.keys())
            _keys=[]
            max_len=random.randint(1,len(ops))
 
            # shuffle
            random.shuffle(ops)
            ops=ops[:max_len]

            for _key in ops:    
                _keys.append(_key)
                op=self.ops_map[_key]
                self.data[colname]=self.data[colname].apply(lambda x:op(x))
                
            res_name="comb_"+"_".join(_keys)
            results[res_name]=" ".join(self.data[colname].tolist())

        else:
            colname="comb_"+"_".join(operations)
            self.data[colname]=self.data.standard.tolist()
            for _key in operations:
                op=self.ops_map[_key]
                self.data[colname]=self.data[colname].apply(lambda x:op(x))
            results[colname]=" ".join(self.data[colname].tolist())
        return results

        
        
    
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
