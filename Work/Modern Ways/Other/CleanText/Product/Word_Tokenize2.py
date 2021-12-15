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
  with open("test1_2.txt", "r", encoding="utf-8") as file:
    text_data = file.read()
except:
  print("There is not such a file  or path is incorrect")

text_data_clean_brackets = re.sub('[\(\[\{].*?[\)\]\}]', '', text_data)

text_data_clean = clean(text_data_clean_brackets,
                        fix_unicode=True,
                        to_ascii=False,
                        lower=True,
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

tokens_without_punc_lemma = []
for word in word_tokens:
    tokens_without_punc_lemma.append(WordNetLemmatizer().lemmatize(word))

tokens_without_punc = pd.Series(tokens_without_punc_lemma)

tokens_without_punc = tokens_without_punc.value_counts().sort_values(ascending=False)

freq_word_df = pd.DataFrame(tokens_without_punc)

freq_word_df = freq_word_df.reset_index()

freq_word_df = freq_word_df.rename(columns={"index": "word", 0 : "frequency"})

freq_word_df["ratio"] = round((freq_word_df.frequency/(sum(freq_word_df.frequency))*100),7)

freq_word_df["cumul_ratio"] = np.cumsum(freq_word_df["ratio"])

freq_word_df_1b = freq_word_df.head(1000000)

freq_word_df_5 = freq_word_df[freq_word_df.frequency>=5]

freq_word_df_1b.to_excel("Word_Tokenize1.xlsx", sheet_name='word_tokenize_1b', index=False)

freq_word_df_5.to_excel("Word_Tokenize2.xlsx", sheet_name='word_tokenize_5', index=False)