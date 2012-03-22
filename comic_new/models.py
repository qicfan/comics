#coding=utf-8
#!/usr/bin/env python
from django.db import models

class Category(models.Model):
	title = models.CharField(max_length = 20, verbose_name = "分类名称")
	create = models.DateTimeField(auto_now_add = True, verbose_name = "添加时间")
	description = models.CharField(max_length = 200, verbose_name = "描述")
	keyword = models.CharField(max_length = 200, verbose_name = "关键字")

	def get_absolute_url(self):
		return "/category/%d_1/" % (self.pk)
	def __unicode__(self):
		return self.title
	class Meta:
		verbose_name_plural = "漫画分类"

class Author(models.Model):
	title = models.CharField(max_length = 50, verbose_name = "作者名称")
	word = models.CharField(max_length = 2, verbose_name = "字母")
	
	def get_absolute_url(self):
		return "/author/%s_1/" % self.title
	def __unicode__(self):
		return self.title
	class Meta:
		ordering = ['word']
		verbose_name_plural = "作者"
		
class Comic(models.Model):
	STATUS_CHOICES = (
		(1, '已完结'),
		(0, '正在连载')
	)
	title = models.CharField(max_length = 100, verbose_name = "漫画名称")
	photo = models.ImageField(upload_to = "img/upload/comic/thumb/%Y/%m/%d", verbose_name ="图片")
	create = models.DateTimeField(auto_now_add = True, verbose_name = "添加时间")
	modify = models.DateTimeField(auto_now_add = True, verbose_name = "修改时间")
	update = models.DateField(verbose_name = "更新时间")
	author = models.ManyToManyField(Author, verbose_name = "作者")
	color = models.CharField(max_length = 10, verbose_name = "颜色")
	chapters = models.IntegerField(verbose_name = "总话数")
	pics = models.IntegerField(verbose_name = "总画数")
	description = models.TextField(verbose_name = "简介")
	status = models.IntegerField(choices = STATUS_CHOICES, default = 2, verbose_name = "状态")
	word = models.CharField(max_length = 1, verbose_name = "字母索引")
	hot = models.IntegerField(default = 1, verbose_name = "推荐值")
	category = models.ManyToManyField(Category, verbose_name = "所属分类")
	up = models.IntegerField(verbose_name = "支持")
	hit = models.IntegerField(verbose_name = "点击数量")

	def get_lasted_chapter(self):
		chapter = Chapter.objects.filter(comic = self.pk).order_by('id')[:1]
		return chapter[0]
	def get_absolute_url(self):
		return "/comic/%d/" % (self.pk)
	def __unicode__(self):
		return self.title
	class Meta:
		verbose_name_plural = "漫画"

class Chapter(models.Model):
	title = models.CharField(max_length = 100, verbose_name = "章节标题")
	create = models.DateTimeField(auto_now_add = True, verbose_name = "添加时间")
	comic = models.ForeignKey(Comic, verbose_name = "所属漫画")
	pics = models.IntegerField(verbose_name = "总画数")
	url = models.CharField(max_length = 100,verbose_name = "对方URL")
	def get_absolute_url(self):
		return "/display/%s/" % (self.pk)
	def __unicode__(self):
		return self.title
	class Meta:
		verbose_name_plural = "章节"

class Pic(models.Model):
	title = models.IntegerField(verbose_name = "标题")
	photo = models.ImageField(upload_to = "img/upload/comic/pic/%Y/%m/%d", verbose_name = "图片")
	create = models.DateTimeField(auto_now_add = True, verbose_name = "添加时间")
	chapter = models.ForeignKey(Chapter, verbose_name = "所属章节")
	url = models.CharField(max_length = 250,verbose_name = "对方URL")

	def get_absolute_url(self):
		return "/comic/%d/%d/%d/" % (self.comic.pk, self.chapter.pk, self.title)
	def __unicode__(self):
		return self.title
	class Meta:
		ordering = ['-title']
		verbose_name_plural = "漫画图片"