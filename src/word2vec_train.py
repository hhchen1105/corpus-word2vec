#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Desc

'''

# Hung-Hsuan Chen <hhchen1105@gmail.com>
# Creation Date : 11-2-2015
# Last Modified:

import json
import logging
import multiprocessing
import os
import sys

import gensim
import gflags

FLAGS = gflags.FLAGS
gflags.DEFINE_string('train_docs', '', '')
gflags.DEFINE_string('save_model', '', '')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def usage(cmd):
    logger.warn('Usage: %s --train_docs="VAL" --save_model="PATH/TO/SAVE/MODEL"' % (cmd))
    return


def check_args(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError:
        logger.error(FLAGS, exc_info=True)

    if FLAGS.train_docs == '':
        usage(argv[0])
        raise Exception('flag --train_docs cannot be empty')

    if FLAGS.save_model== '':
        usage(argv[0])
        raise Exception('flag --save_model cannot be empty')

    for doc in FLAGS.train_docs.split(','):
        if not os.path.isfile(doc.strip()):
            usage(argv[0])
            raise Exception('File "%s" does not exist!' % (doc.strip()))


class MySentences(object):
    def __init__(self, docs):
        self.docs = [d.strip() for d in docs.split(',')]

    def __iter__(self):
        for filename in self.docs:
            for line in open(filename):
                yield line[line.find(':::')+len(':::'):].decode('utf-8').split()


def train_word2vec_model():
    w2v_args = json.load(open('../etc/w2v_settings.py'))
    model = gensim.models.Word2Vec(MySentences(FLAGS.train_docs),
                                   size=w2v_args['hidden_vector_dim'],
                                   window=w2v_args['window_len'],
                                   min_count=w2v_args['min_word_count'],
                                   iter=w2v_args['iters'],
                                   workers=multiprocessing.cpu_count())
    model.save("%s" % (FLAGS.save_model))
    model.save_word2vec_format("%s.text.vector" % (FLAGS.save_model), binary=False)


def main(argv):
    check_args(argv)

    train_word2vec_model()


if __name__ == "__main__":
    main(sys.argv)


