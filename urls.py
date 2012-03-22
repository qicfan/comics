# -*- coding:utf-8 -*-
import os.path,logging
from os.path import join
settings_path = os.path.abspath(os.path.dirname(__file__))

from django.conf.urls.defaults import *
from pet.feed import LatestEntries
from django.contrib import admin
from django.contrib import auth

admin.autodiscover()
feeds = {
    'latest': LatestEntries,
}
urlpatterns = patterns('',
                       (r'^$', 'myweb.comic_new.views.index'),
                       (r'^comic/(?P<comic_id>\d+)/$', 'myweb.comic_new.views.chapter'),
                       (r'^comic/(?P<comic_id>\d+)/(?P<chapter_id>\d+)/$', 'myweb.comic_new.views.read'),
                       (r'^display/(?P<chapter_id>\d+)/$', 'myweb.comic_new.views.readcomic'),
                       (r'^display_ajax/(?P<chapter_id>\d+)/$', 'myweb.comic_new.views.readcomicajax'),
                       (r'^word/(?P<word_id>\w)_(?P<page>\d+)/$', 'myweb.comic_new.views.word'),
                       (r'^author/$', 'myweb.comic_new.views.author'),
                       (r'^author/(?P<author_name>.+?)_(?P<page>\d+)/$', 'myweb.comic_new.views.author_list'),
                       (r'^category/(?P<category_ids>\d+)_(?P<page>\d+)/$', 'myweb.comic_new.views.category'),
                       (r'^search/$', 'myweb.comic_new.views.search'),
                       (r'^admin/', include(admin.site.urls)),
                       (r'^comment/add/$', 'myweb.pet.views.comment_add'),
                       (r'^static/(?P<path>.*)', 'dynamic_media_serve.serve', {'document_root': join(settings_path, 'static/media')}),
)
