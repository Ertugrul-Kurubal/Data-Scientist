#!pip install unicodedata2
#!pip install clean-text
#!pip install openpyxl

import numpy as np
import pandas as pd
import re
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.tokenize import sent_tokenize, word_tokenize
from cleantext import clean
from nltk.stem import WordNetLemmatizer
from openpyxl.workbook import Workbook
nltk.download('tagsets')
nltk.download('punkt')
nltk.download('wordnet')
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

text_data_clean_brackets = re.sub('[\(\[\{].*?[\)\]\}]', '', text_data)

custom_char = ["-","#",":"]
for i in custom_char:
    text_data_clean_brackets = text_data_clean_brackets.replace(i, '')

text_data_clean_apos = re.sub(r"\'", "", string=text_data_clean_brackets) 

text_data_clean = clean(text_data_clean_apos,
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

sentence = sent_tokenize(text_data_clean)

sentence_lower =  []
for i in sentence:
    sentence_lower.append(i.lower())

sent_token_df = pd.DataFrame(sentence_lower)

sent_token_df = sent_token_df.rename(columns={0:"sentence"})

sent_token_no_punc = sent_token_df.sentence.apply(lambda x: re.sub(pattern="[^\w\s]", repl="", string=x))

sent_token_no_punc_df = pd.DataFrame(data=sent_token_no_punc)

def space(sentence):
    a_1 = word_tokenize(sentence)
    a_2 = " ".join(a_1)
    return a_2

sent_token_no_punc_df.sentence = sent_token_no_punc_df.sentence.apply(lambda x : space(x))

sent_token_no_punc_df.drop(sent_token_no_punc_df[sent_token_no_punc_df.sentence == ""].index, inplace=True)

sent_token_no_punc_df = sent_token_no_punc_df.sentence.value_counts().sort_values(ascending=False)

sent_token_no_punc_df2 = pd.DataFrame(sent_token_no_punc_df)

sent_token_no_punc_df2 = sent_token_no_punc_df2.reset_index()

sent_token_no_punc_df2 = sent_token_no_punc_df2.rename(columns={"index":"sentence", "sentence":"frequency"})

total_value = sent_token_no_punc_df2.frequency.sum()

sent_token_no_punc_df2["ratio"] = (sent_token_no_punc_df2.frequency/total_value)*100

sent_token_no_punc_df2["cumul_ratio"] = np.cumsum(sent_token_no_punc_df2["ratio"])

sent_token_no_punc_df3 = sent_token_no_punc_df2.head(500000)

def sentence_lenght(sentence):
    var1 = word_tokenize(sentence)
    if len(var1) <= 10:
        var2 = " ".join(var1)
        return var2
    else:
        return "sentence is bigger ten word"

sent_token_no_punc_df3.sentence = sent_token_no_punc_df3.sentence.apply(sentence_lenght)

sent_token_no_punc_df3 = sent_token_no_punc_df3.reset_index(drop=True)

sent_token_no_punc_df3.to_excel("Sentence_Tokenize.xlsx", sheet_name='sent_tokenize', index=False)