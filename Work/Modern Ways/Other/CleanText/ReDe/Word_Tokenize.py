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
    text_data_clean_brackets = text_data_clean_brackets.replace(i, '')  # must be equal each other

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

tokens_without_punc_lemma = []
for word in tokens_without_punc:
    tokens_without_punc_lemma.append(WordNetLemmatizer().lemmatize(word))

tokens_without_punc = pd.Series(tokens_without_punc_lemma)

tokens_without_punc = tokens_without_punc.value_counts().sort_values(ascending=False)

freq_word_df = pd.DataFrame(tokens_without_punc)

freq_word_df = freq_word_df.reset_index()

freq_word_df = freq_word_df.rename(columns={"index": "word", 0 : "frequency"})

freq_word_df["ratio"] = round((freq_word_df.frequency/(sum(freq_word_df.frequency))*100),7)

freq_word_df["cumul_ratio"] = np.cumsum(freq_word_df["ratio"])

freq_word_df_5 = freq_word_df[freq_word_df.frequency>=5]

freq_word_df_5.to_excel("Word_Tokenize.xlsx", sheet_name='word_tokenize_5', index=False)