# -*- coding: utf-8 -*-
class user(object):
	"""user info"""

	def __init__(self,username,userpwd,usertype):
		self.username=username
		self.userpwd=userpwd
		self.usertype=usertype
		self.status=True
		self.realname=None
		self.id=None

	def is_active(self):
		return self.status
		


