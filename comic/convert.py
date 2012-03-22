#!/usr/bin/python
# -*- coding: cp936 -*-

import sys
import re
import string
import os

class CConvert:
	def __init__(self):
		"Load data table"
		settings_path = os.path.abspath(os.path.dirname(__file__))
		try:
			fp=open(os.path.join(settings_path, "convert.txt"))
		except IOError:
			pass
		else:
			self.data=fp.read()
			fp.close()
	
	def convert(self, strIn):
		"Convert GBK to PinYin"
		length, strOutKey, strOutValue, i=len(strIn), "", "", 0
		while i<length:
			if i==length-1:
				strOutKey+=strIn[i:i+1]+" "
				strOutValue+=strIn[i:i+1]+" "
				break
			code1, code2=ord(strIn[i:i+1]), ord(strIn[i+1:i+2])
			if code1>=0x81 and code1<=0xFE and code2>=0x40 and code2<=0xFE and code2!=0x7F:
				strTemp=self.getIndex(strIn[i:i+2])
				strLength=len(strTemp)
				if strLength<2:strLength=2
				strOutKey+=string.center(strIn[i:i+2], strLength)+" "
				strOutValue+=string.center(strTemp, strLength)+" "
				i+=1;
			else:
				strOutKey+=strIn[i:i+1]+" "
				strOutValue+=strIn[i:i+1]+" "
			i+=1
		return [strOutValue, strOutKey]
	
	def getIndex(self, strIn):
		"Convert single GBK to PinYin from index"
		pos=re.search("^%s([0-9a-zA-Z]+)" % (strIn), self.data, re.M)
		if pos==None:
			return strIn
		else:
			return pos.group(1)