# coding: utf-8
from __future__ import absolute_import
import sys
sys.path = ['.'] + sys.path

import os

from paver.easy import task
from paver.easy import sh
from paver.easy import consume_args

import cult.ngram as ngram
from cult.worker_server import worker_server

@task
def run_worker_server():
    clean()

    if 'AWS_ACCESS_KEY_ID' not in os.environ:
        print 'must have AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY on env'
        exit()

    if 'AWS_SECRET_ACCESS_KEY' not in os.environ:
        print 'must have AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY on env'
        exit()

    worker_server()

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

    ngram.top(gram_size, how_many, year)

    clean()

@task
def clean():
    sh('find . -name "__pycache__" -delete')
    sh('find . -name "*.pyc" -delete')
    sh('find . -name "*~" -delete')

