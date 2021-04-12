import pandas as pd

class GraphemeParser():
    def __init__(self, roots, vds, cds):
        self.roots = roots
        self.vds = vds
        self.cds = cds

    def word2grapheme(self,word):
        graphemes = []
        grapheme = ''
        i = 0
        while i < len(word):
            grapheme += (word[i])
            #         print(word[i], grapheme, graphemes)
            # deciding if the grapheme has ended
            if word[i] in ['\u200d', '্']:
                # these denote the grapheme is contnuing
                pass
            elif word[i] == 'ঁ':  # 'ঁ' always stays at the end
                graphemes.append(grapheme)
                grapheme = ''
            elif word[i] in list(self.roots) + ['়']:
                # root is generally followed by the diacritics
                # if there are trailing diacritics, don't end it
                if i + 1 == len(word):
                    graphemes.append(grapheme)
                elif word[i + 1] not in ['্', '\u200d', 'ঁ', '়'] + list(self.vds):
                    # if there are no trailing diacritics end it
                    graphemes.append(grapheme)
                    grapheme = ''

            elif word[i] in self.vds:
                # if the current character is a vowel diacritic
                # end it if there's no trailing 'ঁ' + diacritics
                # Note: vowel diacritics are always placed after consonants
                if i + 1 == len(word):
                    graphemes.append(grapheme)
                elif word[i + 1] not in ['ঁ'] + list(self.vds):
                    graphemes.append(grapheme)
                    grapheme = ''

            i = i + 1
            # Note: df_cd's are constructed by df_root + '্'
            # so, df_cd is not used in the code

        return graphemes

    def sequencer(self,comps):
        # comps = (root,vd,cd)
        # Take root, consonant and diacritic components
        # and put it in a unicode sequence that follows grapheme
        # creation rule
        
        # Rules maintained in grapheme unicode
        # 1. Vowel diacritic is always at the end except for the case of
            # consonant diacritic 'ঁ'
        # 2. Consonant diacritic 'র্' always sits in front of Root
        # 3. If there is no 'র্', root comes before everything else
        # 4. Consonant diacritics sits in front of vowel diacritics.
            # In case of '্র্য', '্র' comes before '্য', in case of 'র্য', 'র্'
            # comes before root and '্য' is placed after root

        # pseudo code
        # Does it have 'র্' or 'র্য'?
            # place 'র্' in front and then place root.
        # else:
            # place root
        # Is there consonant diacritic?
            # Is there '্র্য' or 'র্য'?
                # If yes for '্র্য'
                    # for '্র্য' place '্র' first and '্য' later
                # If yes for 'র্য'
                    # place '্য' ('র্' already placed before root)
            # else
                # if it is not '্র' or 'ঁ'
                    # place it afterwards
        # Is there vowel diacritic?
            # place it
        uc_sequenced = []
        # print(comps)
        if comps[2] in ['র্' , 'র্য',  'র্্র']:
            uc_sequenced.append('র্')
            uc_sequenced.append(comps[0])
            # if comps[2] ==  'র্্র':
            #     uc_sequenced.append('্র')
        else:
            uc_sequenced.append(comps[0])
        if comps[2] != '0':
            if comps[2] == '্র্য' or comps[2] == 'র্য':
                if comps[2] == '্র্য':
                    uc_sequenced.append('্র')
                    uc_sequenced.append('্য')
                if comps[2] == 'র্য':
                    uc_sequenced.append('্য')
            elif comps[2] ==  'র্্র':
                 uc_sequenced.append('্র')
            else:
                if comps[2] != 'র্' and comps[2] != 'ঁ':
                    uc_sequenced.append(comps[2])
        if comps[1] != '0':
            uc_sequenced.append(comps[1])
        if comps[2] == 'ঁ':
            uc_sequenced.append('ঁ')
        # print(uc_sequenced)
        return uc_sequenced

    def make_grapheme(self,sequence):
        # given the sequenced unicode,create the grapheme
        grapheme = ''
        for item in sequence:
            grapheme += item
        return grapheme
    def grapheme2word(self,graphemes):
        return ''.join(graphemes)

    def comp2grapheme(self,comps):
        uc_sequenced = self.sequencer(comps)
        grapheme = self.make_grapheme(uc_sequenced)
        return grapheme

    # '্'
    def grapheme2component(self,grapheme):
        root = ''
        cd = ''
        vd = ''
        i = 0
        while i < len(grapheme):
            # print(grapheme[i])
            if grapheme[i] == '্': # hoshonto
                # print('1',grapheme[i],[uc for uc in grapheme[i+1:]])
                if (i+1)>= len(grapheme):
                    print('grapheme ending unexpectedly after ্')
                else:
                    if grapheme[i+1] == 'র': # deal ref
                        cd += '্র'
                        i += 1
                    elif grapheme[i + 1] == 'য': # deal with jo-fola
                            cd += '্য'
                            i += 1
                    else:
                        root+=grapheme[i]+grapheme[i + 1] # deal with consonant conjuncts
                        i += 1
            elif grapheme[i] in list(self.roots) +  ['়']: # deal with roots and dot
                # print('2',grapheme[i], [uc for uc in grapheme[i+1:]])
                if grapheme[i] == 'র': # ro could be starting of ref
                    if (i + 1) < len(grapheme):
                        if grapheme[i+1] == '্': # deal with ref
                            cd += 'র্'
                            i += 1
                        elif grapheme[i+1] == '\u200d': # deal with ro+jofola
                            root += grapheme[i]
                            i += 1
                        else:
                            root += grapheme[i]
                    else:
                        root += grapheme[i]
                else:
                    root += grapheme[i]

            elif grapheme[i] in self.vds: # deal with vds
                vd += grapheme[i]
            elif grapheme[i] in self.cds: # deal with cds but at this point there should only be 'ঁ' left
                cd += grapheme[i]
            else:
                print('Out of dictionary symbol encountered: ', grapheme[i])
            i += 1
            
        #squeeze duplicate hoshonoto 'র', '্', '্', 'য'
        if cd == ''.join(['র', '্', '্', 'য']):
            cd = ''.join(['র', '্', 'য'])
        # print(root, vd, cd)
        return root, vd, cd


if __name__ == '__main__':
    path_class_map = 'class_map.csv'
    df_map = pd.read_csv(path_class_map, encoding = 'utf-8')
    df_root = df_map.groupby('component_type').get_group('grapheme_root')
    df_root.set_index('label', inplace = True)
    df_root.drop(columns=['component_type'], inplace = True)
    df_vd = df_map.groupby('component_type').get_group('vowel_diacritic')
    df_vd.set_index('label', inplace = True)
    df_vd.drop(columns=['component_type'], inplace = True)
    df_cd = df_map.groupby('component_type').get_group('consonant_diacritic')
    df_cd.set_index('label', inplace = True)
    df_cd.drop(columns=['component_type'], inplace = True)

    word_list = ['আর্দ্র',  'আবহাওয়াবিদ্যা', 'সৌন্দর্য', 'র‍্যাব','হিজড়াদের', 'শ্য়পূ', 'প্রকাশ্যে',
                 'প্রিথ্রীব্রি', 'য়ন্তে', 'য়র্সে', 'ধ্য়য়নে', 'খ্য়যো', 'মায়াবি', '়য়বা',
                 'ন্দর্যে', 'উৎকৃষ্টতম্', 'হতাে', 'ফেক্সােফেনাডিন', 'জুতশীঅশােক',
                 'টাের্মিনাসগুলির', 'র্যােককুন','ওরা']
    word_list = ['শ্য়পূ'] # the dot needs normalization
    graphemeparser = GraphemeParser(df_root.values, df_vd.values, df_cd.values)
    # print( ''.join(['র', '্', '্', 'র']))
    for word in word_list:
        graphemes = graphemeparser.word2grapheme(word)
        comps_all = [graphemeparser.grapheme2component(grp) for grp in graphemes]

        grapheme_rec_all = [graphemeparser.comp2grapheme(comp)  for comp in comps_all]

        word_rec = graphemeparser.grapheme2word(grapheme_rec_all)

        if word != word_rec:
            # print(repr('শ্য়পূ'))
            print(word, word_rec)
            print([uc for uc in word], [uc for uc in word_rec])
            print('===================')
            print('word', word)
            for grp in graphemes:
                print('grapheme', grp, 'unicodes', [uc for uc in grp],
                      'components', graphemeparser.grapheme2component(grp))
            # print('reconstructed')
