#Masha and Amrita, October 2019

import string

class Reader:

    #method use to read file
    def read_text(self, file_name):
        f = open(file_name,'r')
        text = f.read()
        f.close()
        return text

    #splits file into lines
    def lines(self, text):
        return text.split('\n')

    #tokenized and normalizes text
    def tokenize(self, text):
        clear_text = self.normalize(text)
        return clear_text.split()

    # normalizes string (strips punctuation & to lower case)
    def normalize(self, text):
        lower_text = text.lower()
        translator = str.maketrans('', '', string.punctuation)
        return lower_text.translate(translator)

    # method is used to calculate a term frequency
    def get_word_counts(self, tokens):
        word_count_dict = {} #create an empty dictionaryself,
        #loops through the elements in tokens
        for i in tokens:
            if (word_count_dict.get(i,0) == 0):  #Chekcks if token is in the dictionary
                word_count_dict[i] = 1 #if not it adds it to the dictionary with a value of 1
            else:
                word_count_dict[i] += 1 #If it is its value is incremented by 1
        return word_count_dict

    #saves overlap scores in a file
    def save_scores(self, scores, file_name):
        f1 = open(file_name,"w+")
        for score in scores:
               f1.write(score)
        f1.close()
