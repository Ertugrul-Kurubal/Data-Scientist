import pandas as pd
import numpy as np
import re




digit_and_not_alnum = []
string_word = []
for i in word_list:
    i = str(i)
    if not(i[0].isalnum()) or i[0].isdigit():
        digit_and_not_alnum.append(i)
    else:
        string_word.append(i)
special_name_list = []  
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
        pass