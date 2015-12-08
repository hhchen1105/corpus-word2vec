"""w2v URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import analogy.views
import relevance.views
import mismatch.views
import w2v.views

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^analogy/$', analogy.views.index, name='index'),
    url(r'^analogy/index$', analogy.views.index, name='index'),
    url(r'^relevance/$', relevance.views.index, name='index'),
    url(r'^relevance/index$', relevance.views.index, name='index'),
    url(r'^mismatch/$', mismatch.views.index, name='index'),
    url(r'^mismatch/index$', mismatch.views.index, name='index'),
    url(r'^$', w2v.views.index, name='index'),
    url(r'^/$', w2v.views.index, name='index'),
    url(r'^index$', w2v.views.index, name='index'),
]
