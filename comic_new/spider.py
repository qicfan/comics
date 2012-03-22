#coding=utf-8
#!/usr/bin/env python
from django.http import HttpResponse
from urllib2 import HTTPError, URLError
from models import *
from comic.convert import *
from django.shortcuts import render_to_response
import urllib, urllib2, os, sys, thread, threading, time, re, socket, StringIO

timeout = 10     
socket.setdefaulttimeout(timeout)#这里对整个socket层设置超时时间。后续文件中如果再使用到socket，不必再设置  
def fetchphoto(url):
    headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)", "HTTP_REFERER": "http://anime.xunlei.com/", "REFERER": "http://anime.xunlei.com/"}
    req = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req)
    the_data = response.read()
    response.close()
    return the_data

def fetchpage(url):
    try:
        headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)", "HTTP_REFERER": "http://anime.xunlei.com/", "REFERER": "http://anime.xunlei.com/"}
        req = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(req)
        the_data = response.read()
        response.close()
        return the_data
    except:
        return False

def index(request):
    chapters = Chapter.objects.filter(pk__gt = 14649)
    for item in chapters:
        # 获取数据
        exts = item.url.split('.')
        ext = exts[len(exts)-1]
        ext = re.sub("\n", "", ext)
        page_data = fetchpage(item.url)
        urls = re.sub("http://", "", item.url)
        urls = urls.split('/')
        url = []
        for i in xrange(0, len(urls)-1):
            url.append(urls[i])
        url = '/'.join(url)
        url = "http://%s/" % (url)
        p = re.compile("images_arr\[(\d+)\] = '(.+?)'")
        links = p.findall(page_data)
        for link in links:
            url_tmp = "%s%s" % (url, link[1])
            try:
                pic = Pic.objects.get(chapter = item.pk, title = link[0])
                pic.url = url_tmp
                pic.save()
                continue
            except Exception, e:
                photo = "img/comic/%s/%s/%s.%s" % (item.comic.pk, item.pk, link[0], ext)
                pic = Pic()
                try:
                    pic.title = link[0]
                    pic.photo = photo
                    pic.chapter = item
                    pic.url = url_tmp
                    pic.save()
                except Exception, e:
                    return HttpReponse(str(e))
    return HttpResponse("suc")

def parse(request):
    pic_file = open("D:/pic_data1.txt", "w")
    i_list = [11, 12, 13, 14]
    for i in i_list:
        start = i*100000
        end = start + 100000 - 1
        pics = Pic.objects.all().order_by('pk')[start:end]   
        for item in pics:
            pic_file.write("%s\n%s\n%s\n\n" % (item.pk, item.photo, item.url))
    pic_file.close()
    return HttpResponse("suc")

def author(request):
    authors = Author.objects.all()
    convert=CConvert()
    for item in authors:
        try:
            title = item.title
            out=convert.convert(title.encode("gbk"))
            word = out[0][:1]
        except Exception,e:
            word = u"or"
        try:
            item.word = word
            item.save()
        except:
            pass