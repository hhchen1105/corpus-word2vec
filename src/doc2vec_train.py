#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Desc

'''

# Hung-Hsuan Chen <hhchen1105@gmail.com>
# Creation Date : 11-2-2015
# Last Modified:

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

    if os.path.isfile(FLAGS.save_model):
        if raw_input('File "%s" exists.  Do you want to continue? (y/n) ' % (FLAGS.save_model)) not in ('y', 'Y'):
            raise Exception('File "%s" exists, the script is cancelled' % (FLAGS.save_model))

    for doc in FLAGS.train_docs.split(','):
        if not os.path.isfile(doc.strip()):
            usage(argv[0])
            raise Exception('File "%s" does not exist!' % (doc.strip()))


class MyLabeledSentences(object):
    def __init__(self, docs):
        self.docs = [d.strip() for d in docs.split(',')]

    def __iter__(self):
        for filename in self.docs:
            for line in open(filename):
                words = line[(line.find(':::')+len(':::')):].decode('utf-8').split()
                tags = [line[:line.find(':::')].strip()]
                yield gensim.models.doc2vec.LabeledSentence(words=words, tags=tags)


def train_doc2vec_model():
    model = gensim.models.Doc2Vec(MyLabeledSentences(FLAGS.train_docs),
                                  size=200, window=5, min_count=5, workers=multiprocessing.cpu_count())
    model.save("%s" % (FLAGS.save_model))
    model.save_word2vec_format("%s.text.vector" % (FLAGS.save_model), binary=False)


def main(argv):
    check_args(argv)

    train_doc2vec_model()


if __name__ == "__main__":
    main(sys.argv)

