# -*- coding:utf-8 -*-
from django.conf.urls.defaults import *
urlpatterns = patterns('',
					   (r'^$', 'myweb.pet.views.index'),
					   (r'photo/$', 'myweb.pet.photo.views.index'),
					   (r'photo/(?P<album_id>\d+)/$', 'myweb.pet.photo.views.list'),
                       (r'blog/$', 'myweb.pet.blog.views.index'),
                       (r'blog/detail/(?P<blog_id>\d+)/$', 'myweb.pet.blog.views.detail'),
                       (r'comment/add/$', 'myweb.pet.comment.views.add'),
)
