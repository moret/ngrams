from __future__ import division

import os
import string
from operator import itemgetter

from cult.redis_db import redis_db

grams_len = 5

def increment_ngrams(ngrams, window):
    for i in range(len(window)):
        gram_size = i + 1
        gram = ' '.join(window[-gram_size:])

        if gram in ngrams[i]:
            ngrams[i][gram] += 1
        else:
            ngrams[i][gram] = 1

def clear_punctuation(s):
    return s.translate(string.maketrans('', ''), string.punctuation)

def run_through_words(ngrams, words):
    for i in range(len(words)):
        window = []
        for j in range(len(ngrams)):
            if i - j >= 0:
                window.append(words[i - j])
        window.reverse()
        increment_ngrams(ngrams, window)

def run_through_file(ngrams, filename):
    words = clear_punctuation(open(filename).read().lower()).split()
    if len(words) < len(ngrams):
        print 'small text - scram!'
        exit()

    run_through_words(ngrams, words)

def list_files(foldername):
    filenames = []
    for filename in os.listdir(foldername):
        filenames.append(foldername + '/' + filename)
    return filenames

def create_ngrams_list():
    ngrams = []
    for i in range(grams_len):
        ngrams.append({})

    return ngrams

def run_file(filename, year):
    ngrams = create_ngrams_list()
    run_through_file(ngrams, filename)
    redis_db.persist(ngrams, year)
    return ngrams

def clear_db_year(year):
    redis_db.clear_year(year)

def top(gram_size, how_many, year):
    ngrams = redis_db.range(gram_size, 0, year)
    ngrams

    grams_total = 0
    for gram, count in ngrams:
        grams_total += count

    for gram, count in ngrams[-how_many:]:
        print '%5d (%.10f%%) %s' % (count, count / grams_total, gram)

    return redis_db.range(gram_size, how_many, year)
