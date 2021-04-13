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
### case: replace broken diacritic 
* Example-1: 
    ```python
    (a)'আরো'==(b)'আরো' ->  False 
        (a) breaks as:['আ', 'র', 'ে', 'া']
        (b) breaks as:['আ', 'র', 'ো']
    ```
* Example-2:
    ```python
    (a)'বোধগম্য'==(b)'বোধগম্য' ->   False
        (a) breaks as:['ব', 'ে', 'া', 'ধ', 'গ', 'ম', '্', 'য']
        (b) breaks as:['ব', 'ো', 'ধ', 'গ', 'ম', '্', 'য']
    ```

**Note**: Examples of more Invalid Word cases can be found under **invalid_cases** folder

### Current Cases Handled:
* handles broken diacritics
* removes numbers
* removes non-bengali symbols
* removes invalid starter symbols
* removes invalid ending symbols
* removes consecutive doubles of vds and cds
* removes unwanted connectors in between vds

## TODO
- [ ] Problematic Bangla Symbol removal
- [x] unittest for values
- [x] unittest for types (not sure if the pipeline should handle this)

# Unittest
* change directory to utils:```cd utils```
* run the two tests:``` python3 -m unittest test_wordCleaner```

# Note:
* unittest fails if type assertion is given as follows
```python
if type(word)!=str:
    TypeError("The word must be a string")
```
