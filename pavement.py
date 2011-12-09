# coding: utf-8
from __future__ import absolute_import
import sys
sys.path = ['.'] + sys.path

from paver.easy import task
from paver.easy import sh
from paver.easy import consume_args

import cult.ngram as ngram

@consume_args
@task
def run(args):
    clean()

    if len(args) != 2:
        print 'too few arguments - use: paver run year folder_name/'
        exit()

    year = int(args[0])
    files_folder = args[1]

    ngram.run_folder(files_folder, year)

    clean()

@consume_args
@task
def clear_db_year(args):
    clean()

    if len(args) != 1:
        print 'too few arguments - use: paver clear_db_year year'
        exit()

    year = int(args[0])

    ngram.clear_db_year(year)

    clean()

@consume_args
@task
def top(args):
    clean()

    if len(args) != 3:
        print 'too few arguments - use: paver top year gram_size how_many'
        exit()

    year = int(args[0])
    gram_size = int(args[1])
    how_many = int(args[2])

    print ngram.top(gram_size, how_many, year)

    clean()

@task
def clean():
    sh('find . -name "__pycache__" -delete')
    sh('find . -name "*.pyc" -delete')
    sh('find . -name "*~" -delete')

