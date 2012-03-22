#coding=utf-8
#!/usr/bin/env python
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import Http404
from models import *
from random import randint
from pet.models import Comment
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db import connection
from convert import *
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404

def index(request):
	# 取得热门漫画
	hot_comic = Comic.objects.all().order_by('-hot')[:3]
	# 取得关注度最高的10个漫画
	top_comic = Comic.objects.all().order_by('-up')[:10]
	# 点击排行前10
	hit_comic = Comic.objects.all().order_by('-hit')[:10]
	# 随便看看
	all_comic = Comic.objects.all()
	all = len(all_comic)
	radom = randint(6, all - 6)
	random_comic = all_comic[radom:radom+6]
	# 取评论
	comments = Comment.objects.filter(type = 'comic').order_by("-id")[:5]
	return render_to_response("comic/index.html", {'comments': comments, 'hot_comic': hot_comic, 'top_comic': top_comic, 'hit_comic': hit_comic, 'random_comic': random_comic})

def chapter(request, comic_id):
	comics = Comic.objects.get(pk = comic_id)
	chapters = Chapter.objects.filter(comic = comic_id).order_by('id')
	comments = Comment.objects.filter(type = 'comic', typeid = comic_id)
	comment_count = len(comments)
	try :
		readcomic = request.COOKIES['readcomic']
	except:
		readcomic = ""
	response = render_to_response("comic/chapter.html", {'comics': comics, 'chapters': chapters, 'comments': comments, 'comment_count': comment_count})
	if readcomic.find(comic_id) == -1:
		comics.hit += 1
		comics.save()
		response.set_cookie('readcomic', "%s|%s" % (readcomic, comic_id), 86400)
	return response

def read(request, comic_id, chapter_id):	
	chapters = get_object_or_404(Chapter, pk = chapter_id)
	comics = chapters.comic
	try:
		chapter_pre = chapters.get_previous_by_create(comic = comic_id)
	except:
		chapter_pre = None
	try:
		chapter_next = chapters.get_next_by_create(comic = comic_id)
	except:
		chapter_next = None;
	try:
		page = request.GET["p"]
	except:
		page = 1
	try:
		pics = Pic.objects.get(chapter = chapters.order, title = page).order_by("title")
	except:
		pics = None
	page_pre = int(page) - 1
	if page_pre < 1:
		page_pre = 1
	page_next = int(page) + 1
	piccount = Pic.objects.count()
	if page_next > piccount:
		page_next = piccount
	try:
		pics = pic_list[int(page)-1]
	except:
		raise Http404
	return render_to_response("comic/read.html", {'page_pre': page_pre, 'page_next': page_next, 'comic_id': comic_id, 'chapter_id': chapter_id, 'comics': comics, 'chapters': chapters, 'pics': pics, 'chapter_next': chapter_next, 'chapter_pre': chapter_pre})

def readcomic(request, chapter_id):	
	chapters = get_object_or_404(Chapter, pk = chapter_id)
	comics = chapters.comic
	try:
		chapter_pre = chapters.get_previous_by_create(comic = comics.pk)
	except:
		chapter_pre = None
	try:
		chapter_next = chapters.get_next_by_create(comic = comics.pk)
	except:
		chapter_next = None;
	try:
		page = request.GET["p"]
	except:
		page = 1
	pic_list = Pic.objects.filter(chapter = chapters.order).order_by("title")
	if len(pic_list) == 0:
		pic_list = Pic.objects.filter(chapter = chapters.pk).order_by("title")
	page_pre = int(page) - 1
	if page_pre < 1:
		page_pre = 1
	page_next = int(page) + 1
	piccount = pic_list.count()
	if page_next > piccount:
		page_next = piccount
	try:
		pics = pic_list[int(page)-1]
	except:
		raise Http404
	return render_to_response("comic/read.html", {'page_pre': page_pre, 'page_next': page_next, 'comic_id': comics.pk, 'chapter_id': chapter_id, 'comics': comics, 'chapters': chapters, 'pics': pics, 'chapter_next': chapter_next, 'chapter_pre': chapter_pre})

def word(request, word_id, page):
	try:
		comiclist = Comic.objects.filter(word = word_id).order_by("-create")
	except:
		comiclist = None
	pageSize = 12
	paginator = Paginator(comiclist, pageSize)
	try:
		page = int(page)
	except ValueError:
		page = 1
	try:
		comics = paginator.page(page)
	except:
		comics = paginator.page(paginator.num_pages)
	return render_to_response("comic/word.html", {"comics": comics.object_list,'paginator': paginator,
														'is_paginated': paginator.num_pages > 1,
														'has_next': paginator.num_pages > page+1,
														'has_previous': page - 1 > 0,
														'current_page': page,
														'next_page': page + 1,
														'previous_page': page - 1,
														'pages': paginator.num_pages,
														'page_numbers': paginator.page_range,
														'word_id': word_id})

def author(request):
	authors = cache.get("authors")
	if authors == None:
		cursor = connection.cursor()
		cursor.execute("SELECT author FROM comic_comic GROUP BY author")
		authorlist = cursor.fetchall()
		cursor.close()
		newlist = []
		convert=CConvert()
		for item in authorlist:
			try:				
				out=convert.convert(item[0].encode("gbk"))
				newlist.append([out[0][:1], item[0]])
			except:
				newlist.append(["orther", item[0]])
		wordlist = {"A--D":[], "E--H":[], "I--L":[], "M--P":[], "Q--T":[], "U--W":[], "X--Z":[], "orther":[]}
		for item in newlist:
			item[0] = item[0].lower()
			if item[0] == "a" or item[0] == "b" or item[0] == "c" or item[0] == "d":
				wordlist["A--D"].append(item[1])
			if item[0] == "e" or item[0] == "f" or item[0] == "g" or item[0] == "h":
				wordlist["E--H"].append(item[1])
			if item[0] == "i" or item[0] == "j" or item[0] == "k" or item[0] == "l":
				wordlist["I--L"].append(item[1])
			if item[0] == "m" or item[0] == "n" or item[0] == "o" or item[0] == "p":
				wordlist["M--P"].append(item[1])
			if item[0] == "q" or item[0] == "r" or item[0] == "s" or item[0] == "t":
				wordlist["Q--T"].append(item[1])
			if item[0] == "u" or item[0] == "v" or item[0] == "w":
				wordlist["U--W"].append(item[1])
			if item[0] == "x" or item[0] == "y" or item[0] == "z":
				wordlist["X--Z"].append(item[1])
			if item[0] == "orther":
				wordlist["orther"].append(item[1])
		authors = sorted(wordlist.items(), key = lambda d: d[0])
		cache.set("authors", authors, 60*60*24)
	return render_to_response("comic/author.html", {"authors": authors})

def author_list(request, author_name, page):
	try:
		comiclist = Comic.objects.filter(author = author_name).order_by("-create")
	except:
		comiclist = None
	pageSize = 12
	paginator = Paginator(comiclist, pageSize)
	try:
		page = int(page)
	except ValueError:
		page = 1
	try:
		comics = paginator.page(page)
	except:
		comics = paginator.page(paginator.num_pages)
	return render_to_response("comic/author_list.html", {"comics": comics.object_list,'paginator': paginator,
														'is_paginated': paginator.num_pages > 1,
														'has_next': paginator.num_pages > page+1,
														'has_previous': page - 1 > 0,
														'current_page': page,
														'next_page': page + 1,
														'previous_page': page - 1,
														'pages': paginator.num_pages,
														'page_numbers': paginator.page_range,
														'author_name': author_name})
	
def category(request, category_ids, page):
	categorys = Category.objects.get(pk = category_ids)
	try:
		comiclist = Comic.objects.filter(category = category_ids).order_by("-id")
	except:
		comiclist = None
	pageSize = 18
	paginator = Paginator(comiclist, pageSize)
	try:
		page = int(page)
	except ValueError:
		page = 1
	try:
		comics = paginator.page(page)
	except:
		comics = paginator.page(paginator.num_pages)
	return render_to_response("comic/list.html", {"categorys": categorys, "category_id": category_ids, "comics": comics.object_list,'paginator': paginator,
														'is_paginated': paginator.num_pages > 1,
														'has_next': paginator.num_pages > page+1,
														'has_previous': page - 1 > 0,
														'current_page': page,
														'next_page': page + 1,
														'previous_page': page - 1,
														'pages': paginator.num_pages,
														'page_numbers': paginator.page_range,
														})
	
def search(request):
	try:
		keyword = request.GET["keyword"]
	except:
		keyword = ""
	if keyword == "":
		comics = Comic.objects.all()
	else:
		try:
			comiclist = Comic.objects.filter(title__contains = keyword)
		except:
			return render_to_response("comic/search.html", {"comics": None})
	pageSize = 18
	paginator = Paginator(comiclist, pageSize)
	try:
		page = int(request.GET["page"])
	except:
		page = 1
	try:
		comics = paginator.page(page)
	except:
		comics = paginator.page(paginator.num_pages)
	return render_to_response("comic/search.html", {"keyword": keyword, "comics": comics.object_list,'paginator': paginator,
														'is_paginated': paginator.num_pages > 1,
														'has_next': paginator.num_pages > page+1,
														'has_previous': page - 1 > 0,
														'current_page': page,
														'next_page': page + 1,
														'previous_page': page - 1,
														'pages': paginator.num_pages,
														'page_numbers': paginator.page_range,
														})
