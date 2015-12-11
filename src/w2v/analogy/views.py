# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render_to_response

import gensim
import opencc

class PhraseAnologyQueryForm(forms.Form):
    phrase1 = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'size':10}))
    phrase2 = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'size':10}))
    phrase3 = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'size':10}))


def index(request):
    results = None
    msg = None
    form = None
    analogy_examples = [[u'台灣', u'台北', u'法國'],
                        [u'國民黨', u'馬英九', u'民進黨'],
                        [u'海賊王', u'魯夫', u'火影忍者'],
                        [u'爵士樂', u'紐奧良', u'鄉村音樂'],
                        [u'中研院', u'李遠哲', u'工研院'],
                        [u'台灣', u'台灣大學', u'美國'],
                       ]
    if request.method == 'GET':
        form = PhraseAnologyQueryForm(request.GET)
        if request.GET:
            model = gensim.models.Word2Vec.load('../../var/zhwiki.model')
            phrase1 = opencc.convert(request.GET['phrase1'], 'zhs2zhtw_p.ini').strip()
            phrase2 = opencc.convert(request.GET['phrase2'], 'zhs2zhtw_p.ini').strip()
            phrase3 = opencc.convert(request.GET['phrase3'], 'zhs2zhtw_p.ini').strip()
            try:
                results = model.most_similar_cosmul(positive=[phrase3, phrase2], negative=[phrase1])
            except KeyError:
                if phrase1 not in model.vocab:
                    not_exist_phrase = phrase1
                elif phrase2 not in model.vocab:
                    not_exist_phrase = phrase2
                else:
                    not_exist_phrase = phrase3
                msg = u'Word "%s" is not in vocabulary' % (not_exist_phrase)

    vars = {
        'form': form,
        'results': results,
        'msg': msg,
        'analogy_examples': analogy_examples,
    }
    return render_to_response('analogy/index.djhtml', vars)


