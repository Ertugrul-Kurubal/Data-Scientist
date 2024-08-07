def file_path(input_path, data_file, output_path):
    '''This function use for file path for input data. \n
    file_path(input_path, data_file, output_path): \n  
    input_path is input data drive location, data_file is input file name \n
    output_path is result data drive location.
    '''
    import unicodedata
    import datetime as dt
    import os
    import sys
    import re
    import numpy as np
    import pandas as pd
    from pathlib import Path
    import nltk
    from nltk import word_tokenize 
    import shutil
    from os.path import isfile, join
    import matplotlib.pyplot as plt
    import seaborn as sns
    import glob
    import locale
    from locale import atof
    # from geopy.geocoders import Nominatim
    # from geopy.point import Point
    # from geopy.exc import GeocoderTimedOut
    from functools import reduce

    # custom character alphabet for word
    tr = re.compile(r"[abcçdefgğhıijklmnoöprsştuüvyzqxw]+", re.IGNORECASE|re.UNICODE) # Turkish filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n0123456789'
    en = re.compile(r"[abcdefghıijklmnopqrstxuvwyz]+", re.IGNORECASE|re.UNICODE) # English
    nl = re.compile(r"[abcdefghıijklmnopqrstxuvwyzāăēĕīĭōŏūŭ]+", re.IGNORECASE|re.UNICODE) # Dutch (Flemenk)
    fr = re.compile(r"[abcçdefghıijklmnopqrstxuvwyzàâæèéêëîïôœùûüÿ]+", re.IGNORECASE|re.UNICODE) # French
    de = re.compile(r"[abcdefghıijklmnopqrstxuvwyzäöüß]+", re.IGNORECASE|re.UNICODE) # German
    es = re.compile(r"[abcdefghıijklmnopqrstxuvwyzñáéíóú]+", re.IGNORECASE|re.UNICODE) # Spanish (¿¡)
    pt = re.compile(r"[abcçdefghıijklmnopqrstxuvwyzàáâãéêíóôõú]+", re.IGNORECASE|re.UNICODE) # Portuguese
    it = re.compile(r"[abcdefghıijklmnopqrstxuvwyzàéèìòùî]+", re.IGNORECASE|re.UNICODE) # Italian
    ar = re.compile(r"[ٿصؼۤڳڲؿڎػڠجڿ٬ٸؽؒؓطۄڀۂؘؔتٚڛےٝڜؖڦ٫ډ۰زۇٖۀ،لۓعٮێڔ۶ؚۧۜڤۏإٞٷؗۖ؈ژۣؕؑٴأۻڸۺگاڴڹۯ؉ْڌ؍ي؟ـٟړۅؐڶُىڽېًۢؠضۚڄٛڏٱۦ٩س٦ڼڂٔۘ٠ښٌٍ۬ٳ۾ٲږذۋٵٜ٘ڞڅںٗهڣۿپڒۥۗڋیؙم؞ثۨٹڵڪظٶۭ١ڭەڨحٕ؎ٺڷٰ۪۫ڻڥۛڑڟټآڡغګ؊ّٯڧڮ؏ۮ؋ؤ٪ؾڗۼق۟دکوِڰڐۃ۽ہفرڇچڝ۴بۈٽڕۡھةٓڃئ؛ڬٙڙڢڱۊَۆۉځ۠ۍۑۙڊنءڈٻشڍ؇۵كخ\ا]+", re.IGNORECASE|re.UNICODE) # Arabic

    def convert_one_character_letter(text):
        '''This function converts two byte occupy of letter to one byte unicode character without any visual change \n
        like as Turkish character ç,ş,ö,ğ. \n
        convert_one_character_letter(text): text is any string word or sentence.
        '''
        new_text = unicodedata.normalize('NFC', f"{text}")
        return new_text

    def clean_text(text, custom_alp=tr): # for only string in specific language
        '''This function extract custom_alp character from string \n
        clean_text(text, custom_alp): text is any string word or sentence and custom_alp is specific alphabet.
        '''
        # text_clean = re.findall(custom_alp, text)
        text_result_list = []
        text_list = re.findall(r'\S+', text)
        for text_var in text_list:
            text_clean = re.findall(custom_alp, str(text_var))
            text_result_var = "".join(text_clean)
            text_result_list.append(text_result_var)
        text_result = " ".join(text_result_list)
        return text_result

    def lower_func(text):
        '''This function convert string character to lowercase. \n
        lower_func(text=str): text is any string word or sentence
        '''
        string_lower = str.lower(text)
        return string_lower

    def upper_func(text):
        '''This function convert string character to uppercase. \n
        upper_func(text=str): text is any string word or sentence
        '''
        string_upper = str.upper(text)
        return string_upper

    def capitalize_func(text):
        '''This function convert string character to capitalize case. \n
        capitalize_func(text=str): text is any string word or sentence
        '''
        string_capitalize = str.capitalize(text)
        return string_capitalize

    def title_func(text):
        '''This function convert string character to title as each word start with capital letter. \n
        title_func(text=str): text is any string word or sentence
        '''
        string_title = str.title(text)
        return string_title

    def character_clean_lower_text(text, custom_alp=tr): # for only string in specific language
        '''This function converts two byte occupy of letter to one byte unicode character without any visual change \n
        like as Turkish character ç,ş,ö,ğ. And also extract custom_alp character from string and convert to lowercase. \n
        character_clean_lower_text(text, custom_alp): text is any string word or sentence and custom_alp is specific alphabet.  
        '''
        new_text = unicodedata.normalize('NFC', f"{text}")
        text_result_list = []
        text_list = re.findall(r'\S+', new_text)  # like as word tokenize
        for text_var in text_list:
            text_clean = re.findall(custom_alp, str(text_var))
            text_result_var = "".join(text_clean)
            text_result_list.append(text_result_var)
        text_join = " ".join(text_result_list)
        text_result = str.lower(text_join)
        return text_result

    def convert_to_float(value):
        '''This function convert string numeric value to float type. Like as 1.200,15
        convert_to_float(value): value is a string numeric value
        '''
        value = value.replace(".","").replace(",",".")
        return float(value)

    def whitespace_del(text):
        '''This function provides removing left right white space.\n
        whitespace_del(text): text is a string value as word or sentence.
        '''
        text_var = str(text)
        text_var = text_var.strip()  # rstrip lstrip
        return text_var

    # input_path = r"C:\Users\user\Desktop\Data Analysis\Adoba\Sales_Report\Data\Entegra\Sales\01.01.2024-11.07.2024"
    # output_path = r"C:\Users\user\Downloads"
    # 
    # data_file = r"Entegra_Sales_List (01.01.2024-11.07.2024)"


    df_entegra = pd.read_csv(fr"{input_path}\{data_file}.csv", low_memory=False)

    df_entegra.columns = [x.lower() for x in df_entegra.columns]
    df_entegra.columns = [x.strip() for x in df_entegra.columns]

    df_entegra_select_var = df_entegra[["model","product_name","datetime","total_product_quantity","entegration",\
        "invoice_city","invoice_country","total","tax","grand_total","cargo_company","status_name"]]

    df_entegra_select_var.loc[:,"invoice_country"] = df_entegra_select_var.loc[:,"invoice_country"].fillna("Türkiye")

    df_entegra_select_var.loc[:,"cargo_company"] = df_entegra_select_var.loc[:,"cargo_company"].fillna("diger")

    df_entegra_select_var = df_entegra_select_var.drop_duplicates()
    df_entegra_select_var = df_entegra_select_var.reset_index(drop=True)

    df_entegra_select_var.loc[:,'datetime'] = pd.to_datetime(df_entegra_select_var.loc[:,'datetime'], format='%Y-%m-%d %H:%M:%S')

    df_entegra_select_var.insert(3,"date",pd.to_datetime(df_entegra_select_var["datetime"]).dt.date)
    df_entegra_select_var.insert(4,"time",pd.to_datetime(df_entegra_select_var["datetime"]).dt.time)

    object_columns = df_entegra_select_var.select_dtypes(include='object')

    for column in object_columns.columns:
        df_entegra_select_var.loc[:,f"{column}"] = df_entegra_select_var.loc[:,f"{column}"].apply(lambda x: convert_one_character_letter(x))
        df_entegra_select_var.loc[:,f"{column}"] = df_entegra_select_var.loc[:,f"{column}"].apply(lambda x: whitespace_del(x))
        df_entegra_select_var.loc[:,f"{column}"] = df_entegra_select_var.loc[:,f"{column}"].apply(lambda x: title_func(x))

    df_entegra_select_product = df_entegra_select_var[["model","product_name"]]

    df_entegra_select_product = df_entegra_select_product.drop_duplicates()

    df_entegra_select = df_entegra_select_var

    entegration_list_all = list(df_entegra_select["entegration"].unique())

    df_entegra_select_sales = df_entegra_select[(df_entegra_select["status_name"] == "Onaylandı") | (df_entegra_select["status_name"] == "Yeni Siparis")]
    df_entegra_select_sales.reset_index(drop=True, inplace=True)

    entegration_list_sales = list(df_entegra_select_sales["entegration"].unique())

    df_sales_quantity_entegration = pd.pivot_table(index="model",columns="entegration", values="total_product_quantity", aggfunc='sum', data=df_entegra_select_sales)
    df_sales_quantity_entegration = df_sales_quantity_entegration.fillna(0)
    df_sales_quantity_entegration.reset_index(inplace=True)

    df_sales_quantity_entegration = df_sales_quantity_entegration.rename_axis(None, axis=1)

    for entegration in entegration_list_all:
        if entegration not in entegration_list_sales:
            df_sales_quantity_entegration[f"{entegration}"] = 0
        else:
            pass

    df_sales_quantity_entegration["toplam_satış_adet"] = 0
    for entg_column in entegration_list_all:
        df_sales_quantity_entegration["toplam_satış_adet"] += df_sales_quantity_entegration[f"{entg_column}"]

    df_sales_name_quantity_entegration  = pd.merge(df_sales_quantity_entegration, df_entegra_select_product, how="left", on="model")
    df_sales_name_quantity_entegration.drop_duplicates(inplace=True)

    cols = list(df_sales_name_quantity_entegration.columns)
    cols = [cols[-1]] + cols[:-1]
    df_sales_name_quantity_entegration = df_sales_name_quantity_entegration[cols]

    df_sales_name_quantity_entegration = df_sales_name_quantity_entegration.sort_values(by="toplam_satış_adet", ascending=False)
    df_sales_name_quantity_entegration.reset_index(drop=True, inplace=True)

    df_sales_name_quantity_entegration_drop = df_sales_name_quantity_entegration.drop_duplicates(subset="model")
    df_sales_name_quantity_entegration_drop.reset_index(drop=True, inplace=True)

    df_sales_name_quantity_entegration_drop.to_excel(fr"{output_path}\Entegra Ürün Satış Rakamları Adet.xlsx", index=False)

    return df_sales_name_quantity_entegration_drop

    # result = df_sales_name_quantity_entegration_drop.to_html()
    # print(result)