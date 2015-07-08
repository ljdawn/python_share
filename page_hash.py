# -*- coding: UTF-8 -*-

"""
from http://www.oschina.net/code/snippet_1180874_27326
"""

import cProfile as profile
import pstats
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import networkx as nx

def text_rank4(content):
    sents = list(cut_sentence(content))
    vect = TfidfVectorizer(min_df=1,tokenizer=Tokenize)
    tfidf = vect.fit_transform(sents)
    tfidf_graph = tfidf*tfidf.T
    nx_graph = nx.from_scipy_sparse_matrix(tfidf_graph)
    scores = nx.pagerank(nx_graph)
    res = sorted(((scores[i],i) for i,s in enumerate(sents)), reverse=True)
    top_n_summary = [sents[i] for _,i in sorted(res[:3])]
    print 'text_rank4', u'。 '.join(top_n_summary).replace('\r','').replace('\n','')+u'。'


'''
prof = profile.Profile()
prof.run('test4()')
stats = pstats.Stats(prof)
stats.strip_dirs().print_stats()
'''
