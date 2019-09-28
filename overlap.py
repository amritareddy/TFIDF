import string
class Reader:

    def read_text(self, file_name):
        f = open(file_name,'r')
        text = f.read()
        f.close()
        return text

    def lines(self, text):
        return text.split('\n')

    def tokenize(self, text):
        clear_text = self.normalize(text)
        return tokens = clear_text.split()

    def normalize(self, text):
        lower_text = text.lower()
        translator = str.maketrans('', '', string.punctuation)
        return lower_text.translate(translator)

    def get_word_counts(self, tokens):
        word_count_dict = {} #create an empty dictionaryself,
        #loops through the elements in tokens
        for i in tokens:
            if (word_count_dict.get(i,0) == 0):  #Chekcks if token is in the dictionary
                word_count_dict[i] = 1 #if not it adds it to the dictionary with a value of 1
            else:
                word_count_dict[i] += 1 #If it is its value is incremented by 1
        return word_count_dict

    def save_scores(self, scores, file_name):
        f1 = open(file_name,"w+")
        for score in scores:
               f1.write(score)
        f1.close()

class Overlap:

    def __init__(self):
        self.scores = [];
        self.scores.append("query_id\t doc_id\t score\n")

    def overlap(self):
        reader = Reader();
        docs = reader.read_text('docs.txt')
        qrys = reader.read_text('qrys.txt')

        docs_list = reader.lines(docs)
        qrys_list = reader.lines(qrys)

        docs_terms = {}
        for doc in docs_list:
            tokens = tokenize(doc)
            docs_terms[tokens[0]] = reader.get_word_counts(tokens)

        qrys_terms = {}
        for qry in qrys_list:
            tokens = tokenize(qrys)
            qrys_terms[tokens[0]] = reader.get_word_counts(tokens)

        for query_id, query_dict in qrys_terms:
            for doc_id, doc_dict in docs_terms:
                score = compare(query_dict, doc_dict)
                self.scores.append(""+query_id+"\t"+doc_id+ "\t" + score + "\n")

        reader.save_scores(self.scores, 'overlap.txt')

    def compare(self, qry, doc):
        # token[0] is the id of each
        # list of scores - text_id + query_id + score \n

        #occur in query + #occur in doc - sum for all the tokens
        score = 0

        for word in qry:
            score += qry[word] * doc[word]

        return score
