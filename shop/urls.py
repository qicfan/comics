# -*- coding:utf-8 -*-
import os.path,logging
from os.path import join
settings_path = os.path.abspath(os.path.dirname(__file__))

from django.conf.urls.defaults import *
from pet.feed import LatestEntries
from django.contrib import admin

admin.autodiscover()
feeds = {
    'latest': LatestEntries,
}
urlpatterns = patterns('',
                       (r'^$', 'myweb.pet.views.blog_index'),
                       (r'^admin/', include(admin.site.urls)),
                       (r'^photo/$', 'myweb.pet.views.photo_index'),
                       (r'^photo/album/(?P<album_id>\d+)_(?P<page>\d+)/$', 'myweb.pet.views.photo_album'),
                       (r'^photo/detail/(?P<photo_id>\d+)/$', 'myweb.pet.views.photo_detail'),
                       (r'^blog/$', 'myweb.pet.views.blog_index'),
                       (r'^blog/detail/(?P<blog_id>\d+)/$', 'myweb.pet.views.blog_detail'),
                       (r'^blog/category/(?P<category_id>\d+)_(?P<page>\d+)/$', 'myweb.pet.views.blog_category'),
                       (r'^comment/add/$', 'myweb.pet.views.comment_add'),
                       (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
                       (r'^static/(?P<path>.*)', 'dynamic_media_serve.serve', {'document_root': join(settings_path, 'static/media')}),
)
