def clean_word(word):      
    # remove non-bengali unicode
    start = 0x0980
    end = 0x09FF
    
    word = ''.join([s for s in word if (ord(s) >= start and ord(s)<=end) or s =='\u200d'])
    
    # remove hoshonto at the end
    
    if word[-1] == '্':
        word = word[:-1] 
        
    # broken vowel diacritic
    # e-kar+a-kar = o-kar
    word = word.replace('ে'+'া', 'ো')
    # e-kar+e-kar = ou-kar
    word = word.replace('ে'+'ৗ', 'ৌ')
    
    return word