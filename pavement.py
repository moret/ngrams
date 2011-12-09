# coding: utf-8
from __future__ import absolute_import
import sys
sys.path = ['.'] + sys.path

from paver.easy import task
from paver.easy import sh

from cult.ngram import run_folder
from cult.ngram import print_most_common

@task
def run():
    clean()

    grams_len = 5
    ngram_to_print = 3
    top_ngrams_to_print = 30
    files_folder = 'shakespeare/'

    ngrams = run_folder(grams_len, files_folder)
    print_most_common(top_ngrams_to_print, ngrams[ngram_to_print - 1])

@task
def clean():
    sh('find . -name "__pycache__" -delete')
    sh('find . -name "*.pyc" -delete')
    sh('find . -name "*~" -delete')

