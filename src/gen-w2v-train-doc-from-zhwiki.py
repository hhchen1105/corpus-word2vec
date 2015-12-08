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


def process_zhwiki(min_content_length=10):
    jieba.load_userdict('../var/tw-dict.dict')
    i = 0
    with open('../var/zhwiki_text.txt', 'w') as f_out:
        for title, content, pageid in gensim.corpora.wikicorpus.extract_pages(
                bz2.BZ2File('../var/zhwiki-20150901-pages-articles.xml.bz2'), filter_namespaces=('0',)):
            content = gensim.corpora.wikicorpus.filter_wiki(content)
            if len(content) >= min_content_length:
                try:
                    all_terms = [ ]
                    content = content.lower().replace('\n', ' ')
                    for sent in content.split():
                        if all(([('a' <= t <= 'z') or ('0' <= t <= '9') for t in sent])):
                            all_terms.append(sent)
                        else:
                            all_terms.extend([t for t in jieba.cut(opencc.convert(sent, 'zhs2zhtw_p.ini'), cut_all=False) if t != ' '])
                    f_out.write('%s ::: %s\n' % (opencc.convert(title, 'zhs2zhtw_p.ini').encode('utf-8'), ' '.join(all_terms).encode('utf-8')))
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


