#coding=utf-8
#!/usr/bin/env python
from django.contrib import admin
from models import *
class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('基本', {'fields': ('title', 'content')}),
        ('其他', {'fields': ('category', 'viewcount')})
    ]
    search_fields = ['title']
    list_display = ('title', 'category', 'adddate', 'viewcount')
    class Media:
        js = (
            '/media/js/tiny_mce/tiny_mce.js',
            '/media/js/textareas.js',
            )

class CommentAdmin(admin.ModelAdmin):
    search_fields = ['nickname']
    list_display = ('nickname', 'type', 'adddate', 'ip', 'status')
    list_filter = ('status', 'type')
    actions = ['make_publish', 'make_verify']
    def make_publish(self, request, queryset):
        rows_updated = queryset.update(status = 2)
        if rows_updated == 1:
            message_bit = "1"
        else:
            message_bit = rows_updated
        self.message_user(request, u"%s个评论审核通过." % message_bit)
    def make_verify(self, request, queryset):
        rows_updated = queryset.update(status = 1)
        if rows_updated == 1:
            message_bit = "1"
        else:
            message_bit = rows_updated
        self.message_user(request, u"%s个评论审核未通过." % message_bit)
    make_publish.short_description = u"将选中项设置为正常状态"
    make_verify.short_description = u"将选中项设置为待审核状态"

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'postcount')

class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'url')

admin.site.register(Category,CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Album)
admin.site.register(Photo)
