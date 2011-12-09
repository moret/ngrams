from __future__ import division

import os
import string
from operator import itemgetter

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

def print_most_common(how_many, grams):
    total = sum(grams.values())
    tops = sorted(grams.items(), key=itemgetter(1),
            reverse=True)[:how_many - 1]

    for top in tops:
        print '%5d (%.10f%%) %s' % (top[1], top[1] / total, top[0])

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

def create_ngrams_list(grams_len):
    ngrams = []
    for i in range(grams_len):
        ngrams.append({})

    return ngrams

def main():
    grams_len = 5
    ngram_to_print = 3
    top_ngrams_to_print = 30
    files_folder = 'shakespeare/'

    ngrams = create_ngrams_list(grams_len)
    for filename in list_files(files_folder):
        run_through_file(ngrams, filename)

    print_most_common(top_ngrams_to_print, ngrams[ngram_to_print - 1])

if __name__ == '__main__':
    main()
