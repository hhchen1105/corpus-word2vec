# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render_to_response

import gensim
import opencc

class PhraseAnologyQueryForm(forms.Form):
    phrases = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size':100}))


def index(request):
    result = None
    msg = None
    form = None
    mismatch_examples = [[u'蘋果', u'鳳梨', u'梨子', u'微軟', u'草莓'],
                         [u'蘋果', u'微軟', u'草莓', u'谷歌', u'臉書'],
                         [u'大學', u'中庸', u'高中', u'孟子', u'論語'],
                         [u'大學', u'中庸', u'高中', u'國中', u'國小'],
                        ]
    if request.method == 'GET':
        form = PhraseAnologyQueryForm(request.GET)
        if request.GET:
            model = gensim.models.Word2Vec.load('../../var/zhwiki_word2vec.model')
            phrases = [t.strip() for t in opencc.convert(request.GET['phrases'], 'zhs2zhtw_p.ini').split(',')]
            for phrase in phrases:
                if phrase not in model.vocab:
                    msg = u'Word "%s" is not in vocabulary' % (phrase)
                    break
            else:
                result = model.doesnt_match(phrases)
    vars = {
        'form': form,
        'result': result,
        'msg': msg,
        'mismatch_examples': mismatch_examples
    }
    return render_to_response('mismatch/index.djhtml', vars)


