#Masha and Amrita, October 2019

import string
from reader import Reader

class Overlap:

    # creates the scores global variable
    def __init__(self):
        self.scores = [];

    # checks if there is an overlap
    def overlap(self):
        reader = Reader();
        docs = reader.read_text('docs.txt')
        qrys = reader.read_text('qrys.txt')

        # breaks the files into separate lines (queries and docs)
        docs_list = reader.lines(docs)
        qrys_list = reader.lines(qrys)

        # tokenizes and records the docs tokenlists into a dictionary,
        # where key is doc_id and value is list of tokens for that doc
        docs_terms = {}
        for doc in docs_list:
            tokens = reader.tokenize(doc)
            if(len(tokens) > 0):
                docs_terms[tokens[0]] = tokens
                # docs_terms[tokens[0]] = reader.get_word_counts(tokens)


        qrys_terms = {}
        for qry in qrys_list:
            tokens = reader.tokenize(qry)
            if(len(tokens) > 0):
                qrys_terms[tokens[0]] = tokens
            #     qrys_terms[tokens[0]] = reader.get_word_counts(tokens)

        #compares each query with every document
        for query_id, query_dict in qrys_terms.items():
            for doc_id, doc_dict in docs_terms.items():
                score = self.compare(query_dict, doc_dict)
                self.scores.append(query_id+" 0 "+doc_id+ " 0 " + str(score) + " 0 \n")

        reader.save_scores(self.scores, 'overlap.top')

    #compares each word in the query with the document and generates a scores for each query
    def compare(self, qry, doc):
        # token[0] is the id of each
        # list of scores - text_id + query_id + score \n

        #occur in query + #occur in doc - sum for all the tokens
        score = 0

        for word in qry:
            if word in doc:
                score += 1
            # qry[word] * doc.get(word,0)

        return score

overlap = Overlap()
overlap.overlap()
