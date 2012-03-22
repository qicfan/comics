#coding=utf8
from django.contrib.syndication.feeds import Feed
from models import Post

class LatestEntries(Feed):
    title = "MINI和YOYO的快乐生活"
    link = "/blog/"
    description = "Updates on changes and additions to www.mqpet.com"

    def items(self):
        try:
            obj = Post.objects.all()[:5]
        except Post.DoesNotExist:
            return HttpResponse("该项目不存在！")
        return obj
