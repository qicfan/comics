#coding=utf-8
#!/usr/bin/env python
"""
主要用来实现网页的采集（支持多线程采集）
采集流程：
    2、根据ID采集漫画（漫画资料入库）
    3、根据漫画采集章节（章节资料入库）
    4、根据章节采集图片（图片资料入库，下载图片）
采集到的图片要经过处理，在不影响质量的前提下，小图不超过4KB，大图不超过100KB
"""
from django.utils.encoding import smart_unicode, smart_str
from django.http import HttpResponse
from urllib2 import HTTPError, URLError
import urllib, urllib2, os, sys, thread, threading, time, re
from models import *
from PIL import Image
from django.shortcuts import render_to_response
import StringIO
thread_count = 0
def index(request):
    """
    取得所有的章节数据，并显示一个列表
    """
    chapter = Chapter.objects.filter().order_by("comic")
    return render_to_response("spider/list.html", {"chapter": chapter})

def fetchcomic(request):
    """
    根据ID来采集漫画
    获取到一个正常的漫画数据并且正常入库之后则启动一个子线程来爬取章节
    """
    settings_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    host = "http://www.imanhua.com"
    comic_id = request.GET['comic_id']
    if comic_id == 0:
        comic_id = 1
    i = 1
    x = 1
    succ = 0
    while i < 2:
        while x < 3000:
            id = (i - 1) * 10 + x + int(comic_id)
            url = "http://www.imanhua.com/comic/%d/" % (id)
            page = fetchpage(url)
            if page == False:
                x += 1
                continue
            else:
                comic = parseComic(page, id)
                #return HttpResponse(comic["chapter"])
                insertComic(comic)
                # 下载图片
                exts = comic["pic"].split('.')
                ext = exts[len(exts)-1]
                ext = re.sub("\n", "", ext)
                p = re.compile("jpg|png|gif|bmp|jpeg|JPG|PNG")
                ext = p.findall(ext)
                ext = ext[0]
                newpath =  "%s/static/media/img/upload/ComicData/%s.%s" % (settings_path, id, ext)
                if os.path.isfile(newpath) == False:
                    photodata = fetchphoto(host + comic["pic"])
                    fi = open(newpath, "wb")
                    fi.write(photodata)
                    fi.close()
                    #image = Image.open(StringIO.StringIO(photodata))
                    #image.save(newpath, quality= 50)
                succ += 1
                    # 创建一个子线程，进行章节的采集
                thread.start_new_thread(fetchchapter, (id, comic["name"], comic["chapter"]))
            x += 1
        i += 1
        #time.sleep(1)
    return HttpResponse("采集完成，成功采集%d个漫画" % (succ))
def fetchchapter(comic_id, name, chapter):
    """
    接受一个参数chapter(通过fetchcomic分析得到的章节的一个列表)
    根据这个参数爬取所有的章节并且入库
    每成功爬取到一个章节的情况下则启动一个子线程来爬去所有的图片
    """
    for item in chapter:
        # 首先将章节数据插入数据库
        chapter_id = item[0]
        title = item[1]
        insertChapter(comic_id, chapter_id, title)
    return

def fetchjs(request, category_id, comic_id, chapter_id):
    """
    根据comic_id和chapter_id来抓取所有的漫画图片
    漫画图片的抓取必须通过AJAX的方式实现，所以必须要与客户端有一个交互的过程
    本函数主要负责抓取到对方页面的加密过的JS字串，并输出给客户端
    """
    # 获取到目标页面的内容
    try:
        url = "http://www.imanhua.com/comic/%s/list_%s.html" % (comic_id, chapter_id)
        headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)"}
        req = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(req)
        the_page = response.read()
        the_page = the_page.decode("gbk")
    except:
        return HttpResponse("false")
    try:
        p = re.compile("eval(.+?)</script>")
        str1 = p.findall(the_page)
        js = "eval%s" % (str1[0])
        js = re.sub("return p", "$('jsbox').value=p;return p", js)
    except:
        p = re.compile("<script language=\"javascript\">var len=(\d+);(.+?)var sid")
        str1 = p.findall(the_page)
        js = str1[0][1]
        js = re.sub("var pic=", "$('jsbox').value='%s';" % (js), js)
    return HttpResponse(js)

def fetchpic(request, category_id, comic_id, chapter_id):
    """
    本函数主要负责对客户端提交的解析过的JS代码进行分析，解析出所有的图片路径，并进行下载
    /pictures/1/3956/010.jpg
    """
    global thread_count
    settings_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    media_path = "%s/static/media/img/comic/" % (settings_path)
    js = request.POST["js"]
    p = re.compile("var pic=\[(.+?)\];");
    str1 = p.findall(js)
    str1 = str1[0]
    str1 = str1.split(',')
    i= 1
    try :
        datafile = open("d:/data.txt", "a")
        for item in str1:
            item = re.sub('"', '', item)
            url = u"http://121.14.157.211:82%s" % (item)
            # 判断目录是否存在
            comic_path = u"%s%s/" % (media_path, comic_id)
            if os.path.isdir(comic_path) != True:
                os.mkdir(comic_path)
            chapter_path = u"%s%s/" % (comic_path, chapter_id)
            if os.path.isdir(chapter_path) != True:
                os.mkdir(chapter_path)
            photo_path = u"%s%d.jpg" % (chapter_path, i)
            exts = item.split('.')
            ext = exts[len(exts)-1]
            new_path = u"/img/comic/%s/%s/%d.%s" % (comic_id, chapter_id, i, ext)
            insertPic(comic_id, chapter_id, i, new_path, url)
            # 创建一个子线程，进行图片的采集
            #thread.start_new_thread(threadgetpic, (comic_id, chapter_id, url, photo_path, new_path, i))
            i += 1
            datafile.write("%s,%s,%s,%s\n" % (comic_id, chapter_id, i, url))
        datafile.close()
    except Exception, e:
        return HttpResponse(str(e))
    return HttpResponse('true')


def threadgetpic(comic_id, chapter_id, url, photo_path, new_path, i):
    # 下载图片
    #if os.path.isfile(photo_path) == True:
    #    return True
    #photodata = fetchphoto(url)
    #image = Image.open(StringIO.StringIO(photodata))
    #image.save(photo_path, quality= 80)
    # 数据入库
    insertPic(comic_id, chapter_id, i, new_path, url)
    return

def fetchpage(url = "http://www.imanhua.com/comic/3029/"):
    """
    根据URL获取到网页的内容
    如果网页不存在或者请求错误，则返回False
    """
    headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)", "HTTP_REFERER": "http://www.imanhua.com/"}
    req = urllib2.Request(url, None, headers)
    try:
        try:
            response = urllib2.urlopen(req)
        except Exception, e:
            return False
        the_page = response.read()
        # 清除掉所有的换行
        the_page = re.sub("\r", "", the_page)
        the_page = re.sub("\n", "", the_page)
        # 清除所有JS
        the_page = re.sub("<script(.+?)</script>", "", the_page)
        # 清除所有STYLE
        the_page = re.sub("style=\"(.+?)\"", "", the_page)
        p = re.compile("<div class=\"bookInfo\">(.+?)<div class=\"blank4\"></div></div></div>")
        the_page = p.findall(the_page)
        return the_page[0].decode("gbk")
    except HTTPError, e:
        return False

def parseComic(page, comic_id):
    """
    根据传入的页面内容分析得出漫画的所有细节字段
    """
    # 得到漫画图片
    p = re.compile("<div class=\"bookCover\"><img src=\"(.+?)\"")
    pic = p.findall(page)
    # 得到漫画名称
    p = re.compile(u"<h1>(.+?)</h1>")
    name = p.findall(page)
    # 得到漫画作者
    p = re.compile(u"原作者：(.+?) \|")
    author = p.findall(page)
    # 得到字母索引
    p = re.compile(u"<a href=\"/comic/(\w)\">\w</a>")
    word = p.findall(page)
    # 得到漫画状态
    p = re.compile(u"<span>完结状态：\[(.+?)\]</span>")
    status = p.findall(page)
    if status[0] == u" <em>连载中</em> ":
        status = 2
    else:
        status = 1
    # 得到漫画简介
    p = re.compile(u"<div class=\"intro\">(.+?)</div>")
    description = p.findall(page)
    # 得到章节列表
    p = re.compile(u"<ul id=\"subBookList\">(.+?)</ul>")
    page1 = p.findall(page)
    p = re.compile("<a href=\"/comic/%s/list_(.+?).html\" title=\"(.+?)\"" % (comic_id))
    chapter = p.findall(page1[0])
    return {"id": comic_id , "status": status,  "pic": pic[0], "name": name[0], "author": author[0], "word": word[0], "description": description[0], "chapter": chapter}

def fetchphoto(url):
    headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)", "HTTP_REFERER": "http://www.imanhua.com/", "REFERER": "http://www.imanhua.com/"}
    req = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req)
    the_data = response.read()
    return the_data

def insertComic(comic):
    """
    将采集到的漫画数据入库
    """
    # 首先检查漫画分类是否存在，并且取得分类ID, 犹豫无法采集到分类，所以默认分类ID为1
    # 再检查漫画是否存在
    try:
        comicM = Comic.objects.get(title = comic["name"])
        return False
    except:
        comicM = Comic()
        comicM.pk = comic["id"]
        comicM.title = comic["name"]
        comicM.photo = "/img/upload/ComicData/%s.jpg" % (comic["id"])
        comicM.author = comic["author"]
        comicM.description = comic["description"]
        comicM.status = comic["status"]
        comicM.word = comic["word"]
        comicM.hot = 1
        comicM.up = 0
        comicM.hit = 0
        comicM.category = Category(pk=1)
        comicM.save()
        return True

def insertChapter(comic_id, chapter_id, title):
    """
    将采集到的章节数据入库
    """
    # 首先检查这个章节是否存在
    try:
        chapterM = Chapter.objects.get(order = chapter_id, comic = comic_id)
    except:
        chapterM = Chapter()
        chapterM.title = title
        chapterM.category = Category(pk=1)
        chapterM.comic = Comic(pk = comic_id)
        chapterM.order = chapter_id
        chapterM.save()
    return True

def insertPic(comic_id, chapter_id, i, path, url):
    try:
        picM = Pic.objects.get(comic = comic_id, chapter = chapter_id, title = i)
        if not picM:
            return
    except:
        picM = Pic()
        picM.title = i
        picM.comic = Comic(pk = comic_id)
        picM.category = Category(pk=1)
        picM.chapter = Chapter(pk=chapter_id)
        picM.photo = path
        picM.picpath = url
        picM.save()
    return

def putpic(request):
    pics = Pic.objects.all()
    f = open("D:/webroot/myweb/static/media/img/data.txt","w")
    for item in pics:
        f.write("%s,%s,%s,%s\n" % (item.comic.pk, item.chapter_id, item.title, item.picpath))
    f.close()
    return HttpResponse("ok")
