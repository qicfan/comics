#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib, urllib2, os, sys, thread, threading, time, re, StringIO
from urllib2 import HTTPError, URLError
from PIL import Image

def fetchphoto(url):
    headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)", "HTTP_REFERER": "http://www.imanhua.com/", "REFERER": "http://www.imanhua.com/"}
    req = urllib2.Request(url, None, headers)
    try:
        try:
            response = urllib2.urlopen(req)
        except Exception, e:
            return False
        the_data = response.read()
        return the_data
    except:
        return False

settings_path = os.path.abspath(os.path.dirname(__file__))
settings_path = re.sub('\\\\', '/', settings_path)
media_path = "%s/comic/" % (settings_path)
if os.path.isdir(media_path) != True:
    os.mkdir(media_path)
f = open("data.txt", "r")
fl = f.readlines()
def fetchpic(fl, media_path, ii):
    # 开启一个LOG文件，记录下载过程
    f = open("log_fail_%d.txt" % (ii), "w")
    for item in fl:
        data = item
        if not data:
            continue
        try:
            data = re.sub("\"", "", data)
        except:
            pass
        str = data.split(',')
        comic_id = str[0]
        chapter_id = str[1]
        i = str[2]
        url = str[3]
        comic_path = "%s%s/" % (media_path, comic_id)
        if os.path.isdir(comic_path) != True:
            os.mkdir(comic_path)
        chapter_path = "%s%s/" % (comic_path, chapter_id)
        if os.path.isdir(chapter_path) != True:
            os.mkdir(chapter_path)
        exts = url.split('.')
        ext = exts[len(exts)-1]
        ext = re.sub("\n", "", ext)
        p = re.compile("jpg|png|gif|bmp|jpeg|JPG|PNG")
        ext = p.findall(ext)
        ext = ext[0]
        photo_path = "%s%s.%s" % (chapter_path, i, ext)
        new_path = "/img/comic/%s/%s/%s.%s" % (comic_id, chapter_id, i, ext)
        if os.path.isfile(photo_path) != True:
        	try:
        	    photodata = fetchphoto(url)
        	    #fi = open(photo_path, "wb")
        	    #fi.write(photodata)
        	    #fi.close()
        	    image = Image.open(StringIO.StringIO(photodata))
        	    image.save(photo_path)
        	    putinfo = u"%s download succesfull" % (url)
        	except Exception, e:
        	    try:
        	        putinfo = u"%s download failed" % (url)
        	        f.writelines("Error: %s; %s; %s" %(e, data, photo_path))
        	    except Exception, e:
        	    	print u"%s" % (e)
        	    	continue

        else:
            putinfo = u"%s.jpg exists" % (i)
        times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print u"Thread%s:[%s]  %s\n" % (ii, times, putinfo)
    f.close()
'''
thread_pool = []
i_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for i in i_list:
    th = threading.Thread(target=fetchpic,args=(fl[1000*(i-1):1000*i], media_path, i) );
    thread_pool.append(th)
for i in i_list:
    thread_pool[i].start()
for i in i_list:
    threading.Thread.join(thread_pool[i])

th = threading.Thread(target=fetchpic,args=(fl, media_path, 1) );
th.start()
threading.Thread.join(th)
'''
count = len(fl)
n = count/40000
thread_pool = []
for i in range(n):
    th = threading.Thread(target=fetchpic,args=(fl[40000*(i-1):40000*i-1], media_path, i) );
    thread_pool.append(th)
for i in range(n):
    thread_pool[i].start()
for i in range(n):
    threading.Thread.join(thread_pool[i])
#fetchpic(fl, media_path, 1)