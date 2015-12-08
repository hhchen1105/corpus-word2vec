# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render_to_response

import gensim
import opencc


class PhraseRelevanceQueryForm(forms.Form):
    available_models = (('../../var/zhwiki.model', '中文維基'),
                        ('../../var/momo.model', 'Momo商品敘述'),
                        ('../../var/zhwiki-and-momo.model', 'both'),)
    phrase1 = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'size':10}))
    selected_model = forms.CharField(max_length=200, widget=forms.Select(choices=available_models))


def index(request):
    results = None
    form = None
    msg = None
    form = PhraseRelevanceQueryForm(request.GET)
    selected_model = form.available_models[0][0]
    sample_phrases = [u'美國', u'魯夫', u'二二八事件', u'宋朝', u'八八風災', u'電話']
    if request.method == 'GET':
        if request.GET:
            selected_model = request.GET['selected_model']
            model = gensim.models.Word2Vec.load(selected_model)
            phrase1 = opencc.convert(request.GET['phrase1'], 'zhs2zhtw_p.ini').strip()
            try:
                results = model.most_similar(phrase1)
            except KeyError:
                msg = u'Word "%s" is not in vocabulary' % (phrase1)
    vars = {
        'form': form,
        'results': results,
        'msg': msg,
        'sample_phrases': sample_phrases,
        'selected_model': selected_model,
    }
    return render_to_response('relevance/index.djhtml', vars)


