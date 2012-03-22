#coding=utf-8
#!/usr/bin/env python
from django.contrib import admin
from models import *
class GoodsAdmin(admin.ModelAdmin):
    list_display = ('title', 'adddate', 'modifydate', 'price', 'marketprice', 'count', 'views')
    class Media:
        js = (
            '/media/js/tiny_mce/tiny_mce.js',
            '/media/js/textareas.js',
            )

admin.site.register(Category)
admin.site.register(Goods, GoodsAdmin)
