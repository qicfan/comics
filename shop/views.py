#coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import *

def blog_index(request):
	# 取出分类信息
	categories = Category.objects.all()
	posts = Post.objects.all().order_by('-adddate')[:20]
	# 取出最新的评论
	comments = Comment.objects.filter(type = 'blog').order_by('-adddate')[:10]
	links = Link.objects.all()
	return render_to_response('blog/blog_index.html', {'categories': categories, 'posts': posts, 'comments': comments, 'links': links})

def blog_detail(request, blog_id):
	# 取出分类信息
	categories = Category.objects.all()
	posts = Post.objects.get(pk = blog_id)
	posts.viewcount += 1
	posts.save()
	comments = Comment.objects.filter(type = 'blog', typeid = blog_id)
	links = Link.objects.all()
	return render_to_response('blog/blog_detail.html', {'categories': categories, 'posts': posts, 'type': 'blog', 'typeid': blog_id, 'comments': comments, 'links': links});

def blog_category(request, category_id, page):
	from django.core.paginator import Paginator
	categories = Category.objects.all()
	post_list = Post.objects.filter(category = category_id).order_by('-adddate')
	pageSize = 10
	paginator = Paginator(post_list, pageSize)
	try:
		page = int(page)
	except ValueError:
		page = 1
	try:
		posts = paginator.page(page)
	except:
		posts = paginator.page(paginator.num_pages)
	typeids = []
	for item in post_list:
	    typeids.append(item.pk)

	comments = Comment.objects.filter(type = 'blog', typeid__in = typeids).order_by('-adddate')[:10]
	links = Link.objects.all()
	return render_to_response('blog/blog_index.html', {
														'paginator': paginator,
														'is_paginated': paginator.num_pages > 1,
														'has_next': paginator.num_pages > page+1,
														'has_previous': page - 1 > 0,
														'current_page': page,
														'next_page': page + 1,
														'previous_page': page - 1,
														'pages': paginator.num_pages,
														'page_numbers': paginator.page_range,
														'categories': categories,
														'posts': posts.object_list,
														'category_id': category_id,
														'comments': comments,
														'links': links
														}
							)

def photo_index(request):
	# 取出专辑信息
	albums = Album.objects.all()
	# 取出最新的评论
	comments = Comment.objects.filter(type = 'photo').order_by('-adddate')[:10]
	links = Link.objects.all()
	return render_to_response('photo/photo_index.html', {'albums': albums, 'comments': comments, 'links': links})

def photo_album(request, album_id, page):
    from django.core.paginator import Paginator
    # 取出对应的专辑的信息
    album = Album.objects.get(pk = album_id)
    # 取出所有的相片列表
    photo_list = Photo.objects.filter(album = album_id)
    pageSize = 20
    paginator = Paginator(photo_list, pageSize)
    try:
    	page = int(page)
    except ValueError:
    	page = 1
    try:
    	photos = paginator.page(page)
    except:
    	photos = paginator.page(paginator.num_pages)
    comments = Comment.objects.filter(type = 'photo').order_by('-adddate')[:10]
    links = Link.objects.all()
    return render_to_response('photo/photo_list.html', {
														'paginator': paginator,
														'is_paginated': paginator.num_pages > 1,
														'has_next': paginator.num_pages > page+1,
														'has_previous': page - 1 > 0,
														'current_page': page,
														'next_page': page + 1,
														'previous_page': page - 1,
														'pages': paginator.num_pages,
														'page_numbers': paginator.page_range,
														'album_id': album_id,
														'photos': photos.object_list,
														'album': album,
														'comments': comments,
														'links': links
														})

def photo_detail(request, photo_id):
    photo = Photo.objects.get(pk = photo_id)
    photos = Photo.objects.filter(album = photo.album.pk)
    comments = Comment.objects.filter(type = 'photo', typeid = photo_id)
    return render_to_response('photo/photo_detail.html', {'comments': comments, 'photo': photo, 'photos': photos, 'type': 'photo', 'typeid': photo_id});\

def comment_add(request):
	comment = Comment(status = 2, content = request.POST['content'], nickname = request.POST['nickname'], ip = request.META['REMOTE_ADDR'], type = request.POST['type'], typeid = request.POST['typeid'])
	comment.save()
	url = '/%s/detail/%s' % (request.POST['type'], request.POST['typeid'])
	return HttpResponseRedirect(url)
