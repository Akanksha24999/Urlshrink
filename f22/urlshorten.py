import random
import sys
import string
from f22.models import Post
from django.shortcuts import get_object_or_404

class ShortenURL:
	_charmap = '123456789abcdefghijklmnopqrstvwxyzABCDEFGHIJKLMNOPQRSTVWXYZ'
	_base = len(_charmap)
	def createurl(self, sid):
		string = ''
		while(sid > 0):
			string = self._charmap[sid % self._base] + string
			sid //= self._base
		return string

	def createsid(self, shortenedurl):
		number = 0
		for char in shortenedurl:
			number = number * self._base + self._charmap.index(char)
		return number
	def inserturl(self,url):
		short_id = self.get_short_code()
		b = Post(httpurl=url, short_id=short_id)
		b.save()
		return short_id
	def get_short_code(self):
		length = 6
		char =  string.digits
    # if the randomly generated short_id is used then generate next
		while True:
			short_id = ''.join(random.choice(char) for x in range(length))
			try:
				temp = Post.objects.get(pk=short_id)
			except:
				return short_id	
	def getoriurl(self,shortenedurl):
		sid=self.createsid(shortenedurl)
		url = get_object_or_404(Post, pk=sid)
		return str(url.httpurl)
