#coding=utf-8
from django.db import models
'''日志存档的MODEL定义'''
class Archive(models.Model):
	title = models.CharField(max_length = 50, verbose_name = "档案名称")
	date = models.CharField(max_length = 10, verbose_name = "档案时间")
	postcount = models.IntegerField(verbose_name = "日志数量")

	objects = models.Manager()
	def get_absolute_url(self):
		return "/blog/archive/%s_1" % (self.pk)
	def __unicode__(self):
		return self.title
	class Meta:
	    verbose_name_plural = "存档"

'''日志分类的MODEL定义'''
class Category(models.Model):
	title = models.CharField(max_length = 200, verbose_name = '标题')
	description = models.CharField(max_length = 200, verbose_name = '描述')
	postcount = models.IntegerField(default = 0, verbose_name = '日志数量')

	objects = models.Manager()
	def get_absolute_url(self):
		return '/blog/category/' + str(self.pk) + '_1'
	def __unicode__(self):
		return '%s(%s)' % (self.title, self.postcount)
	class Meta:
		verbose_name_plural = '分类'

'''日志的MODEL定义'''
class Post(models.Model):
	title = models.CharField(max_length = 200, verbose_name = '标题')
	content = models.TextField(verbose_name = '内容')
	adddate = models.DateTimeField(auto_now_add = True, verbose_name = '发布时间')
	category = models.ForeignKey(Category, verbose_name = '日志分类')
	viewcount = models.IntegerField(default = 0, verbose_name = '浏览数量')
	archive = models.ForeignKey(Archive, verbose_name = "存档目录")

	objects = models.Manager()
	def get_comment_count(self):
	    return len(Comment.objects.filter(type = 'blog', typeid = self.pk, status = 2))
	def get_absolute_url(self):
		return '/blog/detail/' + str(self.pk)
	def save(self):
		# 增加日志分类的日志数量
		if self.pk == None :
			category = Category.objects.get(pk = self.category.pk)
			category.postcount += 1
			category.save()
			# 设定日志存档，首先检查存档是否存在
			import time
			# 取得时间的元组
			stime = time.localtime()
			dates = "%d%d" % (stime[0], stime[1])
			try :
				archive = Archive.objects.get(date = dates)
				archive.postcount += 1
				archive.save()
				self.archive = archive
			except:
				# 存档不存在，首先插入一条存档
				archive1 = Archive()
				archive1.title = "%d年%d月" % (stime[0], stime[1])
				archive1.date = dates
				archive1.postcount = 1
				archive1.save()
				self.archive = archive1
		super(Post, self).save()

	def delete(self):
		category = Category.objects.get(pk = self.category.pk)
		category.postcount -= 1
		category.save()
		super(Post, self).delete()

	def __unicode__(self):
		return self.title
	class Meta:
		verbose_name_plural = '日志'

'''标签MODEL的定义'''
class Tag(models.Model):
	title = models.CharField(max_length = 100, verbose_name = "标签名称")
	usecount = models.IntegerField(default = 1, verbose_name = "使用次数")
	def get_absolute_url(self):
		return '/blog/tag/' + str(self.pk) + '_1'
	def __unicode__(self):
		return '%s' % (self.title)
	class Meta:
		verbose_name_plural = '标签'


'''评论的数据模型定义，只显示正常的条目'''
VIEWABLE_STATUS = [2, 3]
class CommentManager(models.Manager):
	def get_query_set(self):
		default_queryset = super(CommentManager, self).get_query_set()
		return default_queryset.filter(status__in = VIEWABLE_STATUS)

'''评论的MODEL定义'''
class Comment(models.Model):
	STATUS_CHOICES = (
		(1, '需要审核'),
		(2, '正常')
	)
	content = models.TextField(verbose_name = '评论内容')
	adddate = models.DateTimeField(auto_now_add = True, verbose_name = '添加时间')
	status = models.IntegerField(choices = STATUS_CHOICES, default = 1)
	nickname = models.CharField(max_length = 20, verbose_name = "昵称")
	ip = models.IPAddressField(verbose_name = 'IP地址')
	email = models.EmailField(verbose_name = '邮件地址')
	type = models.CharField(max_length = 20, verbose_name = '应用类型')
	typeid = models.IntegerField(verbose_name = '应用ID')

	admin_objects = models.Manager()
	objects = CommentManager()
	def get_comic_title(self):
		from comic.models import Comic
		comics = Comic.objects.get(pk = self.typeid)
		return comics.title
	def __unicode__(self):
		return self.nickname
	class Meta:
		ordering = ['adddate']
		verbose_name_plural = '评论'

'''友情链接的MODEL定义'''
class Link(models.Model):
	title = models.CharField(max_length = 200, verbose_name = '标题')
	description = models.CharField(max_length = 50, verbose_name = '描述')
	url = models.URLField(verbose_name = '链接地址')
	def __unicode__(self):
		return '%s' % (self.title)
	class Meta:
		verbose_name_plural = '友情链接'

'''相册的MODEL定义'''
class Album(models.Model):
    title = models.CharField(max_length = 50, verbose_name = '标题')
    description = models.CharField(max_length = 200, verbose_name = '描述')
    adddate = models.DateTimeField(auto_now_add = True)
    photocount = models.IntegerField(default = 0, verbose_name = '照片数量')

    objects = models.Manager()
    def __unicode__(self):
        return '%s(%s)' % (self.title, self.photocount)
    def get_absolute_url(self):
        return '/photo/album/' + str(self.pk) + '_1'
    def get_cover(self):
        photos = Photo.objects.filter(album = self.pk)[:1]
        if len(photos) > 0:
            return '/static/%s' % (photos[0].photopath)
        return '/media/img/photo/default_cover.gif'
    class Meta:
        verbose_name_plural = '相册'
        unique_together = ['title']

'''相片的MODEL定义'''
class Photo(models.Model):
    title = models.CharField(max_length = 50, verbose_name = '标题')
    description = models.CharField(max_length = 200, verbose_name = '描述')
    photopath = models.FileField(upload_to = 'img/upload/photo/%Y/%m/%d', verbose_name = '上传照片')
    adddate = models.DateTimeField(auto_now_add = True)
    album = models.ForeignKey(Album, verbose_name = '相册')

    objects = models.Manager()
    def get_absolute_url(self):
        return '/photo/detail/' + str(self.pk)
    def get_thumb_url(self):
        return '/static/%s' % (self.photopath)
    def save(self):
        if self.pk == None:
            album = Album.objects.get(id = self.album.id)
            album.photocount += 1
            album.save()
        super(Photo, self).save()

    def delete(self):
        album = Album.objects.get(id = self.album.id)
        album.photocount -= 1
        album.save()
        super(Photo, self).delete()

    def __unicode__(self):
        return self.title
    class Meta:
        verbose_name_plural = '照片'
