# Word Cleaning 
### case:unwanted doubles  
* Example-1: 
```python
    (a)'যুুদ্ধ'==(b)'যুদ্ধ' ->  False 
        (a) breaks as:['য', 'ু', 'ু', 'দ', '্', 'ধ']
        (b) breaks as:['য', 'ু', 'দ', '্', 'ধ']
```
* Example-2:
```python 
    (a)'দুুই'==(b)'দুই' ->   False
        (a) breaks as:['দ', 'ু', 'ু', 'ই']
        (b) breaks as:['দ', 'ু', 'ই']
```
* Example-3:
```python
    (a)'প্রকৃৃতির'==(b)'প্রকৃতির' ->   False
        (a) breaks as:['প', '্', 'র', 'ক', 'ৃ', 'ৃ', 'ত', 'ি', 'র']
        (b) breaks as:['প', '্', 'র', 'ক', 'ৃ', 'ত', 'ি', 'র']
```

### case:unwanted middle connector '্'  
* Example-1: 
```python
    (a)'চু্ক্তি'==(b)'চুক্তি' ->  False 
        (a) breaks as:['চ', 'ু', '্', 'ক', '্', 'ত', 'ি']
        (b) breaks as:['চ', 'ু','ক', '্', 'ত', 'ি']
```
* Example-2:
```python
    (a)'যু্ক্ত'==(b)'যুক্ত' ->   False
        (a) breaks as:['য', 'ু', '্', 'ক', '্', 'ত']
        (b) breaks as:['য', 'ু', 'ক', '্', 'ত']
```
* Example-3:
```python
    (a)'কিছু্ই'==(b)'কিছুই' ->   False
        (a) breaks as:['ক', 'ি', 'ছ', 'ু', '্', 'ই']
        (b) breaks as:['ক', 'ি', 'ছ', 'ু','ই']
```
### case: replace  diacritic 
* Example-1: 
```python
(a)'আরো'==(b)'আরো' ->  False 
    (a) breaks as:['আ', 'র', 'ে', 'া']
    (b) breaks as:['আ', 'র', 'ো']
```
* Example-2:
```python
(a)পৌঁছে==(b)পৌঁছে ->  False
    (a) breaks as:['প', 'ে', 'ৗ', 'ঁ', 'ছ', 'ে']
    (b) breaks as:['প', 'ৌ', 'ঁ', 'ছ', 'ে']
```
* Example-3:
```python
(a)সংস্কৄতি==(b)সংস্কৃতি ->  False
    (a) breaks as:['স', 'ং', 'স', '্', 'ক', 'ৄ', 'ত', 'ি']
    (b) breaks as:['স', 'ং', 'স', '্', 'ক', 'ৃ', 'ত', 'ি']
```
### case: nukta unicode:
* If the connecting char is with in the valid list ['য','ব','ড','ঢ'] then replace with ['য়','র','ড়', 'ঢ়']
* Otherwise remove the nukta char completely

**the connecting char**: is defined as the previous non-vowle-diacritic char 
* Example-1:**when the nukta is immidiately next to a char i.e-'য', '়'**
```python
(a)কেন্দ্রীয়==(b)কেন্দ্রীয় ->  False
    (a) breaks as:['ক', 'ে', 'ন', '্', 'দ', '্', 'র', 'ী', 'য', '়']
    (b) breaks as:['ক', 'ে', 'ন', '্', 'দ', '্', 'র', 'ী', 'য়']
```
* Example-2:**when there is a diacritic inbetween the nukta and a char  i.e-'য', 'ে', '়'**
```python
(a)রযে়ছে==(b)রয়েছে ->  False
    (a) breaks as:['র', 'য', 'ে', '়', 'ছ', 'ে']
    (b) breaks as:['র', 'য়', 'ে', 'ছ', 'ে']
```
* Example-3:Otherwise 
```python
(a)জ়ন্য==(b)জন্য ->  False
    (a) breaks as:['জ', '়', 'ন', '্', 'য']
    (b) breaks as:['জ', 'ন', '্', 'য']
```
### case:invalid hosonto for vowels
* Example-1:
```python
(a)দুই্টি==(b)দুইটি-->False
    (a) breaks as ['দ', 'ু', 'ই', '্', 'ট', 'ি']
    (b) breaks as ['দ', 'ু', 'ই', 'ট', 'ি']
```
* Example-2:
```python
(a)এ্তে==(b)এতে-->False
    (a) breaks as ['এ', '্', 'ত', 'ে']
    (b) breaks as ['এ', 'ত', 'ে'] 
```
* Example-3:
```python
(a)নেট্ওয়ার্ক==(b)নেটওয়ার্ক-->False
    (a) breaks as ['ন', 'ে', 'ট', '্', 'ও', 'য়', 'া', 'র', '্', 'ক']
    (b) breaks as ['ন', 'ে', 'ট', 'ও', 'য়', 'া', 'র', '্', 'ক']
```
* Example-4:
```python
(a)এস্আই==(b)এসআই-->False
    (a) breaks as ['এ', 'স', '্', 'আ', 'ই']
    (b) breaks as ['এ', 'স', 'আ', 'ই']
```

### case: Vowel Diacs after vowels 
* Example-1:
```python
(a)উুলু==(b)উলু-->False
    (a) breaks as ['উ', 'ু', 'ল', 'ু']
    (b) breaks as ['উ', 'ল', 'ু']
```

* Example-2:
```python
(a)আর্কিওোলজি==(b)আর্কিওলজি-->False
    (a) breaks as ['আ', 'র', '্', 'ক', 'ি', 'ও', 'ো', 'ল', 'জ', 'ি']
    (b) breaks as ['আ', 'র', '্', 'ক', 'ি', 'ও', 'ল', 'জ', 'ি']
```
### Normalizes 'এ' and 'ত্র'
```python
(a)একএে==(b)একত্রে-->False
	(a) breaks as ['এ', 'ক', 'এ', 'ে']
	(b) breaks as ['এ', 'ক', 'ত', '্', 'র', 'ে']
```

### case:invalid consecutive vowel diacritics  
* since there is no way to ensure which one is right it simply returns none

**Note**: Examples of more Invalid Word cases can be found under **invalid_cases** folder

### Current Cases Handled:
* handles diacritics (Also Normalizes 'এ' and 'ত্র')
* removes numbers and non-bengali symbols
* removes invalid starter symbols
* removes invalid ending symbols
* removes invalid nukta symbols and normalizes the unicode
* removes invalid hosonto cases for vowels and 'ঁ', 'ং', 'ঃ'
* removes consecutive doubles of vds and cds
* removes unwanted connectors in between vds
* removes vowel diacritics after vowels 

## TODO
- [x] Problematic Bangla Symbol removal
- [x] unittest for values
- [x] unittest for types (not sure if the pipeline should handle this)
- [X] removes invalid nukta symbols and normalizes the unicode
- [x] handle consecutive VDS 

# Unittest
* change directory to utils:```cd utils```
* run the two tests:``` python3 -m unittest test_wordCleaner```


