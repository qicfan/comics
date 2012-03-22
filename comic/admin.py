#coding=utf-8
#!/usr/bin/env python
from django.contrib import admin
from models import *
class PicAdmin(admin.ModelAdmin):
    list_display = ('title', 'create')

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'comic', 'create')

class ComicAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'author', 'word', 'status', 'create', 'hot', 'up', 'hit')
    list_filter = ['category', 'author', 'word']

admin.site.register(Category)
admin.site.register(Comic, ComicAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Pic, PicAdmin)
