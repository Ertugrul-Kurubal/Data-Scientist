import pandas as pd
import numpy as np
import re

#df_word = pd.read_excel("/media/kurubal/SSD1/Data Scientist/Work/Modern Ways/Project/Pyspark/Product/Sentence_Single.xlsx")

word_list = ["ramiro", "Thomas", "Peter","Arthur", "Kirkland", "Sizi","Ertugrul", "Gregor", "$ali", "20str", "evet","neden"]

with open("/media/kurubal/SSD1/Data Scientist/Work/Modern Ways/Project/Pyspark/ReDe/xaa.tr", "r",encoding="latin1") as file:
    text = file.read()


digit_and_not_alnum = []
string_word = []
for i in word_list:
#for i in df_word.sentence:
    i = str(i)
    if not(i[0].isalnum()) or i[0].isdigit():
        digit_and_not_alnum.append(i)
    else:
        string_word.append(i)

special_name_list = []
not_special_name_list = []  
for j in string_word:
    var1_list = re.findall(f"(?:\s|^){j}(?:\s|$)", text, flags=re.IGNORECASE)
    var2_list = []
    for k in var1_list:
        k = re.findall(r'\w+', k)
        var2_list.append(k[0])
    upper_list = []
    lower_list = []
    for m in var2_list:
        if m[0] == m[0].upper():
            upper_list.append(m)
        else:
            lower_list.append(m)
    if round((len(upper_list))/(len(upper_list)+len(lower_list)+0.1)*100,5) >= 98:
        special_name_list.append(j.capitalize())
    else:
        not_special_name_list.append(j)

df_special_name = pd.DataFrame(special_name_list)
df_special_name.rename(columns={0:"Special_Name"}, inplace=True)
df_special_name.to_excel("Special_Names.xlsx", sheet_name="Name_Entity", index=False)

df_not_special_name = pd.DataFrame(not_special_name_list)
df_not_special_name.rename(columns={0:"Not_Special_Name"}, inplace=True)
df_not_special_name.to_excel("Not_Special_Names.xlsx", sheet_name="Not_Name_Entity", index=False)