#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Desc

'''

# Hung-Hsuan Chen <hhchen1105@gmail.com>
# Creation Date : 11-25-2015
# Last Modified:

import bz2
import logging
import sys
import unicodedata

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


def keep_acceptable_chars(unistr):
    def is_accepted_char(uchar):
        if unicodedata.name(uchar).startswith('CJK'):
            return True
        if unicodedata.name(uchar).startswith('LATIN'):
            return True
        if unicodedata.name(uchar).startswith('SPACE'):
            return True
        if unicodedata.name(uchar).startswith('DIGIT'):
            return True
        if unicodedata.name(uchar).startswith('GREEK'):
            return True
        return False

    return ''.join([uchar if uchar.isalpha() and is_accepted_char(uchar) else ' ' for uchar in unistr])


def regularize_content(unistr):
    return unistr.lower()


def process_zhwiki(min_content_length=10):
    jieba.load_userdict('../var/tw-dict.dict')
    i = 0
    with open('../var/zhwiki_text.txt', 'w') as f_out:
        for title, content, pageid in gensim.corpora.wikicorpus.extract_pages(
                bz2.BZ2File('../var/zhwiki-20150901-pages-articles.xml.bz2'), filter_namespaces=('0',)):
            content = gensim.corpora.wikicorpus.filter_wiki(content)
            content = opencc.convert(content, 'zhs2zhtw_p.ini')
            content = keep_acceptable_chars(content)
            content = regularize_content(content)
            if len(content) >= min_content_length:
                try:
                    tag = opencc.convert(title, 'zhs2zhtw_p.ini')
                    doc_content = ' '.join([t for t in jieba.cut(content, cut_all=False) if t != ' '])
                    f_out.write('%s ::: %s\n' % (tag.encode('utf-8'), doc_content.encode('utf-8')))
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


