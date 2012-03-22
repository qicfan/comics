#coding=utf-8
#!/usr/bin/env python
from django.db import models
from django.db import connection
import hashlib
import time


class MemberManager(models.Manager):
    def check_email(self, email_input):
        default_queryset = super(MemberManager, self).get_query_set()
        try:
            user = default_queryset.get(email = email_input)
            if user:
                return True
            else:
                return False
        except:
            return False

    def validate_save(self, request):
        post = request.POST
        if not post["email"]:
            return {'status': 0, 'msg': u'用户不能为空'}
        if not post["nickname"]:
            return {'status': -2, 'msg': u'昵称不能为空'}
        if not post["password"]:
            return {'status': -3, 'msg': u'密码不能为空'}
        if self.check_email(post["email"]):
            return {'status': -1, 'msg': u'用户已存在'}
        m1 = hashlib.md5(post["password"])
        password_md5 = m1.hexdigest()
        datetime = time.strftime("%Y-%m-%d %X")
        ip = request.META["REMOTE_ADDR"]
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO member_member SET email = '%s', password = '%s', nickname = '%s', regip = '%s', regdate = '%s', lastip = '%s', lastdate = '%s', birthday = '0000-00-00', city = ''" % (post["email"], password_md5, post["nickname"], ip, datetime, ip, datetime) )
        except Exception, e:
            return {'status': -4, 'msg': e}
        return {'status': 1, 'msg': u'注册成功'}
        
    def validate_login(self, request):
        if not request["email"]:
            return  {'status': -1, 'msg': u'账户不能为空'}
        if not request["password"]:
            return {'status': -2, 'msg': u'密码不能为空'}
        m1 = hashlib.md5(request["password"])
        password_md5 = m1.hexdigest()
        default_queryset = super(MemberManager, self).get_query_set()
        try:
            user = default_queryset.get(email = request["email"])
            if user.password == password_md5:
                return {'status': 1, 'msg': user}
            else:
                return {'status': -4, 'msg': u'用户密码错误'}
        except Exception, e:
            return {'status': -3, 'msg': u'该用户不存在'}
    
class Member(models.Model):
    email = models.CharField(max_length = 200, verbose_name = "邮件地址")
    password = models.CharField(max_length = 64, verbose_name = "密码")
    nickname = models.CharField(max_length = 12, verbose_name = "昵称")
    regip = models.IPAddressField(verbose_name = "注册IP")
    regdate = models.DateTimeField(auto_now_add = True, verbose_name = "注册时间")
    lastip = models.IPAddressField(verbose_name = "最后登陆IP")
    lastdate = models.DateTimeField(auto_now_add = True, verbose_name = "最后登陆时间")
    birthday = models.DateField(verbose_name = "生日")
    city = models.CharField(max_length = 50, verbose_name = "城市")
    secode = models.CharField(max_length = '6', verbose_name = "随机验证字符串")
    objects = MemberManager()
    class Meta:
        verbose_name_plural = "用户"
