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
nltk.download('wordnet')
nltk.download('punkt')
nltk.help.upenn_tagset('NNP')
nltk.help.upenn_tagset('NN')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('averaged_perceptron_tagger')

try:
  with open("/home/ubuntu/Workspace/fr1.txt", "r", encoding="utf-8") as file:
    text_data = file.read()
except:
  print("There is not such a file  or path is incorrect")

text_data_clean_brackets = re.sub('[\(\[\{].*?[\)\]\}]', '', text_data)

custom_char = ["-","#",":","+","~","*","/","&quot;","&","'"] # ???
for i in custom_char:
    text_data_clean_brackets = text_data_clean_brackets.replace(i, '')  # must be equal each other

text_data_clean = clean(text_data_clean_brackets,
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
                        no_punct=True,
                        no_emoji=True,
                        replace_with_url='',
                        replace_with_email='',
                        replace_with_phone_number='',
                        replace_with_number='',
                        replace_with_digit='',
                        replace_with_currency_symbol='',
                        replace_with_punct=''
                        )

word_tokens = nltk.word_tokenize(text_data_clean)

capital_word = pd.Series(word_tokens)

capital_word = capital_word.value_counts().sort_values(ascending=False)

df_capital = pd.DataFrame(capital_word)

df_capital = df_capital.reset_index()

df_capital = df_capital.rename(columns={"index": "word", 0 : "frequency"})

df_capital.to_csv("Not_Apply_Lower_Word1.csv", index=False)

lower_list = []
for i in word_tokens:
    lower_list.append(i.lower())

tokens_without_punc = pd.Series(lower_list)

tokens_without_punc = tokens_without_punc.value_counts().sort_values(ascending=False)

freq_word_df = pd.DataFrame(tokens_without_punc)

freq_word_df = freq_word_df.reset_index()

freq_word_df = freq_word_df.rename(columns={"index": "word", 0 : "frequency"})

freq_word_df["ratio"] = round((freq_word_df.frequency/(sum(freq_word_df.frequency))*100),7)

freq_word_df["cumul_ratio"] = np.cumsum(freq_word_df["ratio"])

freq_word_df_5 = freq_word_df[freq_word_df.frequency>=5]

freq_word_df_5.to_csv("Word_Tokenize_FR1.csv", index=False)

freq_word_df.to_csv("Word_Tokenize_Full_FR1.csv", index=False)