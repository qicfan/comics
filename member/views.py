#coding=utf-8
#!/usr/bin/env python
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from models import *
from django.core.cache import cache
import random
def index(request):
    if request.COOKIES["uid"]:
        return HttpResponse("登录成功")
    return HttpResponse("登录失败")
def register(request):
    try:
        next = request.GET["next"]
    except:
        next = "/login/"
    if request.POST:
        # 提交了注册信息
        result = Member.objects.validate_save(request)
        if result["status"] == 1:
            return HttpResponse("var result = {'status': 1, 'msg': '注册成功', 'next': '%s'}" % next)
        else:
            return HttpResponse("var result = {'status': %s, 'msg': '%s', 'next': '/register/'}" % (result["status"], result["msg"]))
    return render_to_response("member/register.html", {"next": next})

def login(request):
    if request.POST:
        result = Member.objects.validate_login(request.POST)
        if result["status"] == 1:
            # 登录成功
            secode = ''.join(random.sample("abcdefghijklmnopqrstuvwxyz!#$^&*()", 6))
            httpres = HttpResponse()
            httpres.content = "var result = {'status': 1, 'msg': '登录成功'}"
            httpres.set_cookie("uid", '%s|%s|%s' % (result["msg"].id, result["msg"].email, secode))
            user = Member.objects.get(pk = result["msg"].id)
            user.secode = secode
            user.save()
            return httpres
        else:
            return HttpResponse("var result = {'status': %s, 'msg': '%s'}" % (result["status"], result["msg"]))
    return render_to_response("member/login.html")
    
def check_email_ajax(request):
    email = request.GET["email"]
    try:
        user = Member.objects.get(email = email)
        if user:
            return HttpResponse("var result = {'status': 0, 'msg': '用户已存在', 'next': '/register/'}")
        else:
            return HttpResponse("var result = {'status': 1, 'msg': '用户可以注册', 'next': ''}")
    except:
        return HttpResponse("var result = {'status': 1, 'msg': '用户可以注册', 'next': ''}")
        

def check_user_login():
    if request.COOKIES["uid"]:
        return HttpResponse("登录成功")
    return