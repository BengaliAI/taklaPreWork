import pandas as pd

class GraphemeParser():
    def __init__(self,df_root, df_vd, df_cd):
        self.df_root = df_root
        self.df_vd = df_vd
        self.df_cd = df_cd

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
            elif word[i] in list(df_root.values) + ['়']:
                # root is generally followed by the diacritics
                # if there are trailing diacritics, don't end it
                if i + 1 == len(word):
                    graphemes.append(grapheme)
                elif word[i + 1] not in ['্', '\u200d', 'ঁ', '়'] + list(df_vd.values):
                    # if there are no trailing diacritics end it
                    graphemes.append(grapheme)
                    grapheme = ''

            elif word[i] in df_vd.values:
                # if the current character is a vowel diacritic
                # end it if there's no trailing 'ঁ' + diacritics
                # Note: vowel diacritics are always placed after consonants
                if i + 1 == len(word):
                    graphemes.append(grapheme)
                elif word[i + 1] not in ['ঁ'] + list(df_vd.values):
                    graphemes.append(grapheme)
                    grapheme = ''

            i = i + 1
            # Note: df_cd's are constructed by df_root + '্'
            # so, df_cd is not used in the code

        return graphemes

if __name__ == '__main__':
    path_class_map = 'class_map.csv'
    df_map = pd.read_csv(path_class_map)
    df_root = df_map.groupby('component_type').get_group('grapheme_root')
    df_root.set_index('label', inplace = True)
    df_root.drop(columns=['component_type'], inplace = True)
    df_vd = df_map.groupby('component_type').get_group('vowel_diacritic')
    df_vd.set_index('label', inplace = True)
    df_vd.drop(columns=['component_type'], inplace = True)
    df_cd = df_map.groupby('component_type').get_group('consonant_diacritic')
    df_cd.set_index('label', inplace = True)
    df_cd.drop(columns=['component_type'], inplace = True)


    word_list = ['আর্দ্র', 'ওরা', 'হিজড়াদের', 'শ্য়পূ', 'আবহাওয়াবিদ্যা', 'প্রকাশ্যে',
                 'প্রিথ্রীব্রি', 'য়ন্তে', 'য়র্সে', 'ধ্য়য়নে', 'খ্য়যো', 'মায়াবি', '়য়বা',
                 'ন্দর্যে', 'সৌন্দর্য', 'উৎকৃষ্টতম্', 'হতাে', 'ফেক্সােফেনাডিন', 'জুতশীঅশােক',
                 'টাের্মিনাসগুলির', 'র্যােককুন']

    graphemeparser = GraphemeParser(df_root, df_vd, df_cd)
    for word in word_list:
        print(word, graphemeparser.word2grapheme(word))
