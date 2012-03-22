#coding=utf-8
#!/usr/bin/env python
from django.http import HttpResponseRedirect, HttpResponse, Http404
from models import *
from random import randint
from pet.models import Comment, Link
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db import connection
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
	links = Link.objects.all()
	return render_to_response("comic/index.html", {'links': links, 'comments': comments, 'hot_comic': hot_comic, 'top_comic': top_comic, 'hit_comic': hit_comic, 'random_comic': random_comic})

def chapter(request, comic_id):
	comics = Comic.objects.get(pk = comic_id)
	authors = []
	authors1 = []
	for item in comics.author.all():
		authors.append("<a href='%s'>%s</a>" % (item.get_absolute_url(), item.title))
	for item in comics.author.all():
		authors1.append(item.title)
	author = ', '.join(authors)
	author1 = ', '.join(authors1)
	category = []
	for item in comics.category.all():
		category.append("<a href='%s'>%s</a>" % (item.get_absolute_url(), item.title))
	category = ', '.join(category)
	chapters = Chapter.objects.filter(comic = comic_id).order_by('id')
	comments = Comment.objects.filter(type = 'comic', typeid = comic_id)
	comment_count = len(comments)
	try :
		readcomic = request.COOKIES['readcomic']
	except:
		readcomic = ""
	response = render_to_response("comic/chapter.html", {'category': category, 'comics': comics, 'author': author, 'author1': author1, 'chapters': chapters, 'comments': comments, 'comment_count': comment_count})
	if readcomic.find(comic_id) == -1:
		comics.hit += 1
		comics.save()
		response.set_cookie('readcomic', "%s|%s" % (readcomic, comic_id), 86400)
	return response

def read(request, comic_id, chapter_id):
	return HttpResponseRedirect("/display/%s/" % chapter_id)

def readcomic(request, chapter_id):
	after_range_num = 5
	bevor_range_num = 4
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
	return render_to_response("comic/read.html", {'page': page, 'page_pre': page_pre, 'page_next': page_next, 'comic_id': comics.pk, 'chapter_id': chapter_id, 'comics': comics, 'chapters': chapters, 'pics': pics, 'chapter_next': chapter_next, 'chapter_pre': chapter_pre})

def readcomicajax(request, chapter_id):
	chapters = get_object_or_404(Chapter, pk = chapter_id)
	comics = chapters.comic
	try:
		page = request.GET["p"]
	except:
		page = 1
	pic_list = Pic.objects.filter(chapter = chapters.pk).order_by("title")
	try:
		pics = pic_list[int(page)-1]
	except:
		raise Http404
	return render_to_response("comic/read_ajax.html", {'pics': pics, 'comic_id': comics.pk, 'chapter_id': chapter_id, 'comics': comics, 'chapters': chapters})
def word(request, word_id, page):
	try:
		comiclist = Comic.objects.filter(word = word_id).order_by("-create")
		comiccount = len(comiclist)
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
	return render_to_response("comic/word.html", {'comiccount':comiccount, "comics": comics.object_list,'paginator': paginator,
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
	authorlist = Author.objects.all().order_by('word')
	return render_to_response("comic/author.html", {"authors": authorlist})

def author_list(request, author_name, page):
	after_range_num = 5
	bevor_range_num = 4
	try:
		comiclist = Comic.objects.filter(author__title = author_name).order_by("-create")
		comiccount = len(comiclist)
	except:
		comiclist = None
	pageSize = 12
	paginator = Paginator(comiclist, pageSize)
	try:
		page = int(page)
	except ValueError:
		page = 1
	if page >= after_range_num:
		page_range = paginator.page_range[page-after_range_num:page+bevor_range_num]
	else:
		page_range = paginator.page_range[0:int(page)+bevor_range_num]
	try:
		comics = paginator.page(page)
	except:
		comics = paginator.page(paginator.num_pages)
	return render_to_response("comic/author_list.html", {'comiccount':comiccount, "comics": comics.object_list,'paginator': paginator,
														'is_paginated': paginator.num_pages > 1,
														'has_next': paginator.num_pages > page+1,
														'has_previous': page - 1 > 0,
														'current_page': page,
														'next_page': page + 1,
														'previous_page': page - 1,
														'pages': paginator.num_pages,
														'page_numbers': page_range,
														'author_name': author_name})
	
def category(request, category_ids, page):
	after_range_num = 5
	bevor_range_num = 4
	categorys = Category.objects.get(pk = category_ids)
	try:
		comiclist = Comic.objects.filter(category__pk = category_ids).order_by("-id")
		comiccount = len(comiclist)
	except:
		comiclist = None
	pageSize = 18
	paginator = Paginator(comiclist, pageSize)
	try:
		page = int(page)
	except ValueError:
		page = 1
	if page >= after_range_num:
		page_range = paginator.page_range[page-after_range_num:page+bevor_range_num]
	else:
		page_range = paginator.page_range[0:int(page)+bevor_range_num]
	try:
		comics = paginator.page(page)
	except:
		comics = paginator.page(paginator.num_pages)
	return render_to_response("comic/list.html", {'comiccount':comiccount, "categorys": categorys, "category_id": category_ids, "comics": comics.object_list,'paginator': paginator,
														'is_paginated': paginator.num_pages > 1,
														'has_next': paginator.num_pages > page+1,
														'has_previous': page - 1 > 0,
														'current_page': page,
														'next_page': page + 1,
														'previous_page': page - 1,
														'pages': paginator.num_pages,
														'page_numbers': page_range,
														})
	
def search(request):
	after_range_num = 5
	bevor_range_num = 4
	try:
		keyword = request.GET["keyword"]
	except:
		keyword = ""
	if keyword == "":
		comics = Comic.objects.all()
	else:
		try:
			comiclist = Comic.objects.filter(title__contains = keyword)
			comiccount = len(comiclist)
		except:
			return render_to_response("comic/search.html", {"comics": None})
	pageSize = 18
	paginator = Paginator(comiclist, pageSize)
	try:
		page = int(request.GET["page"])
	except:
		page = 1
	if page >= after_range_num:
		page_range = paginator.page_range[page-after_range_num:page+bevor_range_num]
	else:
		page_range = paginator.page_range[0:int(page)+bevor_range_num]
	try:
		comics = paginator.page(page)
	except:
		comics = paginator.page(paginator.num_pages)
	return render_to_response("comic/search.html", {'comiccount':comiccount, "keyword": keyword, "comics": comics.object_list,'paginator': paginator,
														'is_paginated': paginator.num_pages > 1,
														'has_next': paginator.num_pages > page+1,
														'has_previous': page - 1 > 0,
														'current_page': page,
														'next_page': page + 1,
														'previous_page': page - 1,
														'pages': paginator.num_pages,
														'page_numbers': page_range,
														})
