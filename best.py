import string
import math
from reader import Reader

class tfidf:
    # creates the scores global variable
    def __init__(self):
        self.k = 2
        self.scores = []

    def tfidf(self):
        reader = Reader();
        docs = reader.read_text('docs.txt')
        qrys = reader.read_text('qrys.txt')

        # breaks the files into separate lines (queries and docs)
        docs_list = reader.lines(docs)
        qrys_list = reader.lines(qrys)

        global_vocab = {}
        text_size = {}

        collection_len = 0;

        for doc in docs_list:
            tokens = reader.tokenize(doc)
            if(len(tokens) > 0):
                doc_id = tokens[0]
                # del tokens[0]
                text_size[doc_id] = len(tokens)
                collection_len += len(tokens)

                for token in tokens:
                    if token in global_vocab:
                        term_dict = global_vocab[token]
                        if(doc_id in term_dict):
                            term_dict[doc_id] += 1
                        else:
                            term_dict[doc_id] = 1
                    else:
                        global_vocab[token] = {doc_id: 1}

        self.collection_size = len(docs_list)
        self.avg_doc_len = collection_len/self.collection_size

        qrys_terms = {}
        for qry in qrys_list:
            tokens = reader.tokenize(qry)
            if(len(tokens) > 0):
                qry_id = tokens[0]
                # del tokens[0]
                qrys_terms[qry_id] = reader.get_word_counts(tokens)

        for query_id, query_dict in qrys_terms.items():
            for doc_id, doc_len in text_size.items():
                score = 0
                for term, tfq in query_dict.items():
                    if term in global_vocab:
                        doc_dict = global_vocab[term]
                        if doc_id in doc_dict:
                            tfd = doc_dict[doc_id]
                            df = len(global_vocab[term])
                            idf = math.log(self.collection_size/df)
                            norm_tf = tfq * idf* (tfd/(tfd + self.k*doc_len/self.avg_doc_len))
                            term_score = norm_tf*idf
                            score+=term_score

                self.scores.append(query_id+" 0 "+doc_id+ " 0 " + str(score) + " 0 \n")

        reader.save_scores(self.scores, 'test.top')

t = tfidf()
t.tfidf()
