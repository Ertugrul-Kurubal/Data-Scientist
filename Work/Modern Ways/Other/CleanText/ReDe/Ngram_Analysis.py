#!pip install unicodedata2
#!pip install clean-text
#!pip install openpyxl

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from cleantext import clean
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk import ngrams
from collections import Counter
from openpyxl.workbook import Workbook
import re
nltk.download('tagsets')
nltk.download('wordnet')
nltk.download('punkt')
nltk.help.upenn_tagset('NNP')
nltk.help.upenn_tagset('NN')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('averaged_perceptron_tagger')

try:
  with open("test1_2.txt", "r", encoding="utf-8") as file:
    text_data = file.read()
except:
  print("There is not such a file  or path is incorrect")

text_data_clean = clean(text_data,
                        fix_unicode=True,
                        to_ascii=False,
                        lower=False,
                        normalize_whitespace=True,
                        no_line_breaks=True,
                        strip_lines=False,
                        keep_two_line_breaks=False,
                        no_urls=True,
                        no_emails=True,
                        no_phone_numbers=True,
                        no_numbers=True,
                        no_digits=True,
                        no_currency_symbols=True,
                        no_punct=False,
                        no_emoji=True,
                        replace_with_url='',
                        replace_with_email='',
                        replace_with_phone_number='',
                        replace_with_number='',
                        replace_with_digit='',
                        replace_with_currency_symbol='',
                        replace_with_punct=''
                        )

text_data_clean_apos = re.sub(r"\'", "", string=text_data_clean)

text_data_clean_brackets = re.sub('[\(\[\{].*?[\)\]\}]', '', text_data_clean_apos)

custom_char = ["-","#",":"]
for i in custom_char:
    text_data_clean_brackets = text_data_clean_brackets.replace(i, '') 

word_tokens = nltk.word_tokenize(text_data_clean_brackets)

pos_tags = nltk.pos_tag(word_tokens)

chunks = nltk.ne_chunk(pos_tags, binary=True)

entities =[]
labels =[]
for chunk in chunks:
    if hasattr(chunk,'label'):
        #print(chunk)
        entities.append(' '.join(c[0] for c in chunk))
        labels.append(chunk.label())
        
entities_labels = list(set(zip(entities, labels)))
entities_df = pd.DataFrame(entities_labels)
entities_df.columns = ["Entities","Labels"]

entities_list = []
for i in entities_labels:
    entities_list.append(i[0])

for ent in entities_list:
    text_data_clean_brackets = text_data_clean_brackets.replace(ent, '')
text_data_clean_ne = text_data_clean_brackets

var1 = re.findall(r'\w+.', text_data_clean_ne)
var2 = " ".join(var1)
text_data_clean_punc_alone = var2

text_data_clean2 = clean(text_data_clean_punc_alone,
                        fix_unicode=True,
                        to_ascii=False,
                        lower=False,
                        normalize_whitespace=True,
                        no_line_breaks=True,
                        strip_lines=False,
                        keep_two_line_breaks=False,
                        no_urls=True,
                        no_emails=True,
                        no_phone_numbers=True,
                        no_numbers=True,
                        no_digits=True,
                        no_currency_symbols=True,
                        no_punct=False,
                        no_emoji=True,
                        replace_with_url='',
                        replace_with_email='',
                        replace_with_phone_number='',
                        replace_with_number='',
                        replace_with_digit='',
                        replace_with_currency_symbol='',
                        replace_with_punct=''
                        ) # White space

word_tokens_2 = word_tokenize(text_data_clean2.lower())

tokens_without_punc = [w for w in word_tokens_2 if w.isalpha()]

text = " ".join(tokens_without_punc)

twogram_1 = []
n = 2
twograms = ngrams(text.split(), n)

for grams in twograms:
    twogram_1.append(list(grams))

twogram_1_df = pd.DataFrame(twogram_1)

twogram_1_df = twogram_1_df.rename(columns = {0: "one", 1 : "two"})

twogram_1_df["twogram"] = twogram_1_df["one"].astype(str) +" "+ twogram_1_df["two"].astype(str)

twogram_2_df = pd.DataFrame(twogram_1_df["twogram"].value_counts().sort_values(ascending = False))

twogram_2_df = twogram_2_df.reset_index()

twogram_2_df.rename(columns={"index":"twograms","twogram":"frequency"}, inplace=True)

twogram_2_df["ratio"] = round(twogram_2_df.frequency/twogram_2_df.frequency.sum()*100,7)

twogram_2_df["cumul_ratio"] = np.cumsum(twogram_2_df["ratio"])

twogram_3_df = twogram_2_df[twogram_2_df.frequency>=5]

twogram_3_df.to_excel("TwoGrams.xlsx", sheet_name='twograms', index=False)

threegram_1 = []
n = 3
threegrams = ngrams(text.split(), n)

for grams in threegrams:
    threegram_1.append(list(grams))

threegram_1_df = pd.DataFrame(threegram_1)

threegram_1_df = threegram_1_df.rename(columns = {0 : "one", 1 : "two", 2 : "three"})

threegram_1_df["threegram"] = threegram_1_df["one"].astype(str) +" "+ threegram_1_df["two"].astype(str) +" "+ threegram_1_df["three"].astype(str)

threegram_2_df = pd.DataFrame(threegram_1_df["threegram"].value_counts().sort_values(ascending = False))

threegram_2_df = threegram_2_df.reset_index()

threegram_2_df.rename(columns={"index":"threegrams","threegram":"frequency"}, inplace=True)

threegram_2_df["ratio"] = round(threegram_2_df.frequency/threegram_2_df.frequency.sum()*100,7)

threegram_2_df["cumul_ratio"] = np.cumsum(threegram_2_df["ratio"])

threegram_3_df = threegram_2_df[threegram_2_df.frequency>=4]

threegram_3_df.to_excel("ThreeGrams.xlsx", sheet_name='threegrams', index=False)

fourgram_1 = []
n = 4
fourgrams = ngrams(text.split(), n)

for grams in fourgrams:
    fourgram_1.append(list(grams))

fourgram_1_df = pd.DataFrame(fourgram_1)

fourgram_1_df = fourgram_1_df.rename(columns = {0 : "one", 1 : "two", 2 : "three", 3 : "four"})

fourgram_1_df["fourgram"] = fourgram_1_df["one"].astype(str) +" "+ fourgram_1_df["two"].astype(str) +" "+ fourgram_1_df["three"].astype(str) +" "+ fourgram_1_df["four"].astype(str)

fourgram_2_df = pd.DataFrame(fourgram_1_df["fourgram"].value_counts().sort_values(ascending = False))

fourgram_2_df = fourgram_2_df.reset_index()

fourgram_2_df.rename(columns={"index":"fourgrams","fourgram":"frequency"}, inplace=True)

fourgram_2_df["ratio"] = round(fourgram_2_df.frequency/fourgram_2_df.frequency.sum()*100,7)

fourgram_2_df["cumul_ratio"] = np.cumsum(fourgram_2_df["ratio"])

fourgram_3_df = fourgram_2_df[fourgram_2_df.frequency>=3]

fourgram_3_df.to_excel("FourGrams.xlsx", sheet_name='fourgrams', index=False)

fivegram_1 = []
n = 5
fivegrams = ngrams(text.split(), n)

for grams in fivegrams:
    fivegram_1.append(list(grams))

fivegram_1_df = pd.DataFrame(fivegram_1)

fivegram_1_df = fivegram_1_df.rename(columns = {0 : "one", 1 : "two", 2 : "three", 3 : "four", 4 : "five"})

fivegram_1_df["fivegram"] = fivegram_1_df["one"].astype(str) +" "+ fivegram_1_df["two"].astype(str) +" "+ fivegram_1_df["three"].astype(str) +" "+ fivegram_1_df["four"].astype(str) +" "+ fivegram_1_df["five"].astype(str)

fivegram_2_df = pd.DataFrame(fivegram_1_df["fivegram"].value_counts().sort_values(ascending = False))

fivegram_2_df = fivegram_2_df.reset_index()

fivegram_2_df.rename(columns={"index":"fivegrams","fivegram":"frequency"}, inplace=True)

fivegram_2_df["ratio"] = round(fivegram_2_df.frequency/fivegram_2_df.frequency.sum()*100,7)

fivegram_2_df["cumul_ratio"] = np.cumsum(fivegram_2_df["ratio"])

fivegram_3_df = fivegram_2_df[fivegram_2_df.frequency>=2]

fivegram_3_df.to_excel("FiveGrams.xlsx", sheet_name='fivegrams', index=False)

sixgram_1 = []
n = 6
sixgrams = ngrams(text.split(), n)

for grams in sixgrams:
    sixgram_1.append(list(grams))

sixgram_1_df = pd.DataFrame(sixgram_1)

sixgram_1_df = sixgram_1_df.rename(columns = {0 : "one", 1 : "two", 2 : "three", 3 : "four", 4 : "five", 5 : "six"})

sixgram_1_df["sixgram"] = sixgram_1_df["one"].astype(str) +" "+ sixgram_1_df["two"].astype(str) +" "+ sixgram_1_df["three"].astype(str) +" "+ sixgram_1_df["four"].astype(str) +" "+ sixgram_1_df["five"].astype(str) +" "+ sixgram_1_df["six"].astype(str)

sixgram_2_df = pd.DataFrame(sixgram_1_df["sixgram"].value_counts().sort_values(ascending = False))

sixgram_2_df = sixgram_2_df.reset_index()

sixgram_2_df.rename(columns={"index":"sixgrams","sixgram":"frequency"}, inplace=True)

sixgram_2_df["ratio"] = round(sixgram_2_df.frequency/sixgram_2_df.frequency.sum()*100,7)

sixgram_2_df["cumul_ratio"] = np.cumsum(sixgram_2_df["ratio"])

sixgram_3_df = sixgram_2_df[sixgram_2_df.frequency>=1]

sixgram_3_df.to_excel("SixGrams.xlsx", sheet_name='sixgrams', index=False)