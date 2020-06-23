#Masha and Amrita, October 2019

import string
import math
from reader import Reader

class tfidf:
    # creates the scores global variable
    def __init__(self):
        self.k = 2
        self.scores = []

    # calculates and saves the score for each query-document pair
    def tfidf(self):
        #Reads the files
        reader = Reader();
        docs = reader.read_text('docs.txt')
        qrys = reader.read_text('qrys.txt')
        # reads the file that contains the stop words
        stop_words = reader.read_text('english.stop')

        # breaks the files into separate lines (queries and docs)
        docs_list = reader.lines(docs)
        qrys_list = reader.lines(qrys)
        stop_words_list = reader.tokenize(stop_words)

        # Dictionary of types mapped to dictionaries of frequencies in documents
        global_vocab = {}

        # Dictionary with sizes of each document
        text_size = {}

        #length of document collection
        collection_len = 0;

        # for each document in the list of the documents
        for doc in docs_list:
            # tokenize the doc
            tokens = reader.tokenize(doc)
            #if the doc is not empty
            if(len(tokens) > 0):
                # save doc_id
                doc_id = tokens[0]
                # delete the id
                del tokens[0]
                #save the size of the document
                text_size[doc_id] = 0;

                # for each token
                for token in tokens:
                    # if its not a stop words
                    if token not in stop_words_list:
                        # we delete the references
                        if token == "references":
                            break;

                        # use n-grams
                        if len(token) > 14:
                            token = token[0:14]
                        #increment the size of the document
                        text_size[doc_id]+=1;
                        #if we encountered it before
                        if token in global_vocab:
                            #get a reference to the dictionary of this token
                            term_dict = global_vocab[token]
                            # if the doc_id already in that dictionary
                            if(doc_id in term_dict):
                                #increment
                                term_dict[doc_id] += 1
                            else:
                                #otherwise add the id and count of 1
                                term_dict[doc_id] = 1
                        else:
                            #otherwise add the word to the global dictionary
                            global_vocab[token] = {doc_id: 1}

            #increase the size of total vocab
            collection_len += text_size[doc_id]

        #calculate the collection size
        self.collection_size = len(docs_list)-1
        #calculate the average length of the document
        self.avg_doc_len = collection_len/self.collection_size

        qrys_terms = {}
        for qry in qrys_list:
            tokens = reader.tokenize(qry)
            if(len(tokens) > 0):
                for token in tokens:
                    # remove the stopwords
                    if token in stop_words_list:
                        tokens.remove(token)
                    # use n-grams
                    elif(len(token)>14):
                        token = token[0:14]
                #store the query id
                qry_id = tokens[0]
                # delete the query id
                del tokens[0]
                qrys_terms[qry_id] = reader.get_word_counts(tokens)

        #for each of the queries
        for query_id, query_dict in qrys_terms.items():
            #for each of the docs
            for doc_id, doc_len in text_size.items():
                #start score is 0
                score = 0
                #for each term in query
                for term, tfq in query_dict.items():
                    #if there is a document with such term
                    if term in global_vocab:
                        #get the list of documents with it
                        doc_dict = global_vocab[term]
                        #if the doc we calculating is in this list
                        if doc_id in doc_dict:
                            #calculate the tfidf for this pair
                            tfd = doc_dict[doc_id]
                            df = len(global_vocab[term])
                            idf = math.log(self.collection_size/df)
                            norm_tf = tfq * idf * (tfd/(tfd + self.k*doc_len/self.avg_doc_len))
                            term_score = norm_tf*idf
                            score+=term_score
                #save score
                self.scores.append(query_id+" 0 "+doc_id+ " 0 " + str(round(score)) + " 0 \n")
        #save all the scores
        reader.save_scores(self.scores, 'best.top')

t = tfidf()
t.tfidf()
