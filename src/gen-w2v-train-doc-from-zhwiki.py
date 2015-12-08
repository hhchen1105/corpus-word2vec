#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Desc

'''

# Hung-Hsuan Chen <hhchen1105@gmail.com>
# Creation Date : 11-25-2015
# Last Modified:

import logging
import sys

import gensim
import gflags
import jieba
import opencc

FLAGS = gflags.FLAGS
gflags.DEFINE_string('arg1', '', '')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def usage(cmd):
    logger.warn('Usage: %s --arg1="VAL"' % (cmd))
    return


def check_args(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError:
        logger.error(FLAGS, exc_info=True)

    #if FLAGS.arg1 == '':
    #    usage(argv[0])
    #    logger.error('flag --arg1 cannot be empty', exc_info=True)
    #    raise


def process_zhwiki():
    jieba.load_userdict('../var/tw-dict.dict')
    wiki = gensim.corpora.WikiCorpus('../var/zhwiki-20150901-pages-articles.xml.bz2', dictionary={})
    i = 0
    with open('../var/wiki_zh_text.txt', 'w') as f_out:
        for article in wiki.get_texts():
            try:
                f_out.write(' '.join(
                    [term for term in jieba.cut(
                        opencc.convert(' '.join(article), 'zhs2zhtw_p.ini'), cut_all=False) if term != ' ']).encode('utf-8') + '\n')
                i += 1
            except:
                pass
            if i % 1000 == 0:
                logger.info("Saved %i articles" % (i))

    logger.info("Totally saved %i articles" % (i))


def main(argv):
    check_args(argv)

    process_zhwiki()


if __name__ == "__main__":
    main(sys.argv)


