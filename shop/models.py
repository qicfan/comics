#coding=utf-8
from django.db import models
class Category(models.Model):
	title = models.CharField(max_length = 20, verbose_name = "分类标题")
	adddate = models.DateTimeField(auto_now_add = True, verbose_name = "添加时间")
	parent = models.ForeignKey("self", blank = True, null = False, default = 0, verbose_name = "上级分类")
	goodscount = models.IntegerField(default = 0, verbose_name = "商品数量")
	def __unicode__(self):
		return '%s(%s)' % (self.title, self.goodscount)
	class Meta:
	    verbose_name_plural = '商品分类'

class Goods(models.Model):
	title = models.CharField(max_length = 200, verbose_name = "商品名称")
	adddate = models.DateTimeField(auto_now_add = True, verbose_name = "添加时间")
	modifydate = models.DateTimeField(auto_now = True, verbose_name = "修改时间")
	price = models.FloatField(verbose_name = "商品价格")
	marketprice = models.FloatField(verbose_name = "市场价格")
	description = models.TextField(verbose_name = "商品描述")
	photo = models.ImageField(upload_to = 'img/upload/goods/%Y/%m/%d', verbose_name = "商品图片")
	count = models.IntegerField(default = 1, verbose_name = "库存数量")
	category = models.ForeignKey(Category, verbose_name = "商品分类")
	views = models.IntegerField(default = 1, verbose_name = "浏览次数")
	def __unicode__(self):
		return self.title
	class Meta:
		verbose_name_plural = '商品'
