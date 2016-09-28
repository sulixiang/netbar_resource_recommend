# -*- coding: utf-8 -*-
import os
import csv
from gensim.models import Word2Vec
from gensim import utils, matutils
from numpy import dot, array, float as REAL 

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecommendationEngine:
    """A resource recommendation engine via word2vec
    """

    def __load_model(self):
        """Load the exists model file
        """
        self.model = Word2Vec.load_word2vec_format(os.path.join('model','wordVector.txt'),binary=False)

    def __train_model(self):
        """Train the word2vec model with the current dataset
        """
        logger.info("Training the word2vec model...")
        self.model = Word2Vec(self.sentences,\
                        size=self.size,\
                        workers=self.num_workers,\
                        #max_vocab_size=self.num_features,\
                        min_count = self.min_word_count,\
                        window = self.window)
        self.model.save_word2vec_format(os.path.join('model','wordVector.txt'),binary=False)
        logger.info("word2vec model built!")
    
    def build_model(self, dataset_path):
        """Add additional sentences
        """
        # Load data for later use
        logger.info("Loading corpus data...")
        self.dataset_path = dataset_path
        self.sentences = []
        with open(os.path.join(self.dataset_path,'export_gamerun_series.csv'),'rt') as f:
                reader = csv.reader(f)
                for row in reader:
                        self.sentences.append(row)
        # train the word2vec model
        self.__train_model()
    
    def add_sentences(self, sentences):
        """Add additional sentences
        """
        f = open(os.path.join(self.dataset_path,'export_gamerun_series.csv'),'a')
        for row in sentences:
                self.sentences.append(row)
                f.write(row+"\n")
        f.close()
        # Re-train the word2vec model with the new sentences
        self.__train_model()
        return sentences

    def reload_model(self):
        self.__load_model()
        

    def get_vec(self, rawdata):
        """Recommends up to topn most similar to positive and most unsimilar to negative
        """
        return self.model[rawdata]
    
    def get_most_similar(self, positive, negative, topn):
        """Recommends up to topn most similar to positive and most unsimilar to negative
        """
        return self.model.most_similar(positive=positive, negative=negative, topn=topn)
    
    def get_ranking_by_similar(self, positive, negative, rawdata):
        """Recommends up to topn most similar to positive and most unsimilar to negative
        """
        i=0
        distinct_words = set()
        word2index = {}
        index2word = {}
        all_vecs = []
        for word in positive+negative+rawdata:
            distinct_words.add(word)
        for word in distinct_words:
            word2index[word]=i
            index2word[i]=word
            i=i+1
            all_vecs.append(self.model[word])
        
        positive = [(word,1.0) for word in positive]
        negative = [(word,-1.0) for word in negative]
        mean = []
        for word,weight in positive+negative:
            mean.append(weight*all_vecs[word2index[word]])
        mean = matutils.unitvec(array(mean).mean(axis=0)).astype(REAL)
        dists = dot(all_vecs,mean)
        best = matutils.argsort(dists, len(all_vecs), reverse=True)
        result = [(index2word[sim],float(dists[sim])) for sim in best if index2word[sim] in rawdata]
        return result

    def __init__(self):
        """Init the recommendation engine given a dataset path
        """
        logger.info("Starting up the Recommendation Engine: ")

        # Init the model
        #self.num_features = 1000 # 最多多少个不同的features，即限制语料库里有多少个独立的词，用于控制内存占用
        self.min_word_count = 1 # 一个word最少出现多少次才被计入
        self.num_workers = 8     # 多少thread一起跑
        self.size = 64          # vec的size
        self.window = 5          # 前后观察多长的“语境”，即前后多少个词
        self.__load_model()
