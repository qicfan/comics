#coding=utf-8
#!/usr/bin/env python
from django.contrib import admin
from models import *
class PicAdmin(admin.ModelAdmin):
    list_display = ('title', 'create')

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'comic', 'create', 'pics')

class ComicAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'word', 'status', 'create', 'hot', 'up', 'hit')
    search_fields = ['title']

admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Comic, ComicAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Pic, PicAdmin)
