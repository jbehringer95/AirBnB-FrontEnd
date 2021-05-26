import numpy as np
import pickle
from datetime import datetime
import sklearn

current_time = datetime.now()


class mt():
    def __init__(self):
        '''
        This class hosts several data cleaning and feature alteration functions that are used in model.ipynb
        '''
        pass
    

    def get_oe():
        filehandler = open('pickled_model',"rb")
        oe = pickle.load(filehandler)
        return oe


    def clean(text):
        '''
            The clean function takes in one argument (text) and returns a modified/cleaned list of word values.
        '''
        
        # texts is a list of words from the argument 'text'
        texts = text.strip("{}").replace(" ","_").replace("\"","").replace(","," ").lower().split(" ")
        tokens = []
    
        # removing redundant values from the texts list
        for x in texts:
            if x != "translation_missing:_en.hosting_amenity_49" and x != "translation_missing:_en.hosting_amenity_50" and len(x) >=1:
                tokens.append(x)
        return tokens

    def get_days(datet):
        '''
            get_days has one argument (text)
            
            It is used to create a new feature in the data set 'host_since_days'
        '''
        dates = datet.split('-')
        days = ((current_time.year - int(dates[0])) * 365) + ((current_time.month - int(dates[1])) * 30) + int(dates[2])
        return days


    def get_token_doc():
        '''
            Applied to the same column as clean. This takes in a list of words and converts to a set to remove repeated values.

            ----------
            
            Doc takes in a word and gives it a doc object number valuation (enumerate)
        '''
        tokens = set()
        for lists in df['amenities']:
            for x in lists:
                tokens.add(x)
        token_doc = {}
        for i, x in enumerate(tokens):
            token_doc[x] = i
        return token_doc

    def tokenize(word_list,token_doc):
        '''
            Encoding word_list (amenities) with new number values for tokenization.
        '''
        encoded_list = []
        for word in word_list:
            encoded_list.append(token_doc[word])
        return encoded_list