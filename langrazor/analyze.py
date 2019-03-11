# version 0.1

# AIM - create functions that analyse and throw out CMI index

import pandas as pd
import nltk
import os
import sys
import numpy as np

BASE_PATH = os.getcwd()
sys.path.insert(0,BASE_PATH)

from langrazor import language_models



def initiate_languages(list_models):
    assert list_models is list, "Check initiate_languages input"

    path_list = []
    for model in list_models:
        if language_models.check_existance(model):
            model_path =  language_models.check_existance(model, path_return =True)
            path_list.append(model_path)
        else:
            raise ValueError(f'{model} does not exist in language_universe')
    return(path_list)


def load_model(model_path):

    #Assumptions on the file type - any tsv seperated file with first column of the words
    # No repeated words in the dataset

    word_df = pd.read_csv(model_path, sep = '\t', header = None)
    word_list = word_df.loc[:,0].values

    print(f'---- Language loaded from {model_path}')
    print(f'Number of words {len(word_list)}')
    print("-------------------------------------")

    #converting into lower case
    word_list = [str(x).lower() for x in word_list]

    return(word_list)


def load_data(path, sep = '\t'):
    #Assumptions on the file  - the column that needs to be analysed is clean as per the users requirement
    raw_data = pd.read_csv(path, sep)
    print(f'---- Raw data loaded from {path}')
    print(f'Shape of the data frame is {raw_data.shape}')
    print("-------------------------------------")
    return(raw_data)


def number_of_words(text):
    text = str(text)
    words = text.split(" ")
    total_words = len(words)

    return(total_words)

def language_words(text, language_list):
    text = str(text)
    text_words = text.split(" ")
    lang_count = 0
    lang_words = []
    for word in text_words:
        if str(word) in language_list :
            lang_words.append(word)
    return(lang_words)

def calculate_language_words(raw_data, column_name,language_list, lang_number):
    identifier = "language_" + lang_number
    column_1 = identifier + "_words"
    column_2 = "num_" + identifier + "_words"


    raw_data[column_1] = raw_data.apply(lambda row : language_words(row[column_name],language_list),1)
    raw_data[column_2] = raw_data[column_1].apply(len,0)

    return(raw_data)


def calculate_cmi(raw_data,column_name,lang_list_1,lang_list_2, drop_cols = True):
    raw_data['num_total_words'] = raw_data[column_name].apply(number_of_words,1)
    raw_data = calculate_language_words(raw_data,column_name,lang_list_1, "1")
    raw_data = calculate_language_words(raw_data,column_name,lang_list_2, "2")
    print(raw_data.columns)
    raw_data['num_tokens_identified'] = raw_data['num_language_1_words'] + raw_data['num_language_2_words']
    raw_data['max_lang1_lang2'] = raw_data[['num_language_1_words','num_language_2_words']].max(axis=1)
    raw_data.max_lang1_lang2 = raw_data.max_lang1_lang2.astype(int)
    raw_data['buff_diff'] = raw_data.num_tokens_identified - raw_data.max_lang1_lang2
    raw_data['cmi'] = raw_data['buff_diff'].divide(raw_data.num_tokens_identified.where(raw_data.num_tokens_identified !=0, np.nan))
    raw_data['cmi'] = raw_data['cmi'].fillna(0)

    if drop_cols :
        print(raw_data.columns)
        new_columns = ['buff_diff','max_lang1_lang2','num_total_words','num_tokens_identified','num_language_1_words','num_language_2_words','language_1_words','language_2_words']
        raw_data = raw_data.drop(new_columns, axis = 1)


    return(raw_data)












## Trial Code

list  = ["conference_dump","google_1gram"]
path_list = initiate_languages(list)
wordlist1 = load_model(path_list[0])
wordlist2 = load_model(path_list[1])

data = load_data("/Users/apple/Documents/gatech/nlp/project/data/raw/india_jan17.csv", sep = ",")
data = data.loc[1:10]
data1 = calculate_cmi(data,"body",wordlist1,wordlist2,drop_cols = True)
print(data1)
