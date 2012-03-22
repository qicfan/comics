#coding=utf8
from django.template import Library
from django.template.defaultfilters import stringfilter
import re
register = Library()
@stringfilter
def truncatehanzi(value, arg):
	value = re.sub(r"<(.+?)>", r"", value)
	try:
		bits = []
		for x in arg.split(u':'):
		    if len(x) == 0:
		        bits.append(None)
		    else:
		        bits.append(int(x))
		if int(x) < len(value):
		    return value[slice(*bits)] + '...'
		return value[slice(*bits)]
	except (ValueError, TypeError):
		return value # Fail silently.
@stringfilter
def STATUS_CHOICE(value):
	if value == "1":
		return "已完结"
	else:
		return "<font color=\"red\">连载中</font>"

def timestamp(value):
	import time
	return value
	create_second = time.mktime(time.localtime(value))

	current_second = time.time()

	second = current_second - create_second
	if second > 518400:
		return value
	else :
		if second > 86400:
			return "%d天前" % (second // 86400)
		else :
			if second > 3600:
				return "%d小时前" % (second // 3600)
			else:
				if second > 60:
					return "%d分钟前" % (second // 60)
				else:
					if second > 1:
						return "%d秒前" % (second)
					else:
						return "刚刚"

STATUS_CHOICE.is_safe = True
register.filter('timestamp', timestamp)
register.filter('truncatehanzi', truncatehanzi)
register.filter('STATUS_CHOICE', STATUS_CHOICE)
