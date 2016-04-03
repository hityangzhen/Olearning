# -*- coding: utf-8 -*-
from admin.models import Teacher,Administrator,Student
from olearning.models import user
from django.core.exceptions import ObjectDoesNotExist

def authenticate(username,userpwd,usertype):
	try:
		if usertype==0:
			s=Student.objects.get(student_username=username)
			if s.student_userpwd==userpwd:
				u=user(username,userpwd,usertype)
				u.status=s.student_status
				u.realname=s.student_realname
				u.id=s.id
				return u
			else:
				return None
		elif usertype==1:
			t=Teacher.objects.get(teacher_username=username)
			if t.teacher_userpwd==userpwd:
				u=user(username,userpwd,usertype)
				u.status=t.teacher_status
				u.realname=t.teacher_realname
				u.id=t.id
				return u
			else:
				return None
		else:
			a=Administrator.objects.get(administrator_username=username)
			if a.administrator_userpwd==userpwd:
				u=user(username,userpwd,usertype)
				u.status=a.administrator_status
				u.realname=a.administrator_realname
				u.id=a.id
				return u
			else:
				return None
	except ObjectDoesNotExist,e:
		print 'user does not exist'
		return None













