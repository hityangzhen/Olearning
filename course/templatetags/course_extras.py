# -*- coding: utf-8 -*-
# extra tags and filter for template

from django import template
register = template.Library()
from course.models import Course,CourseComment
from admin.models import Teacher,Student,Administrator

@register.filter(name='split')
def split(value, arg):
	if value:
		return value.split(arg)
	return ''

@register.filter(name='courseNameSet')
def courseNameSet(value,arg):
	if value:
		idset=value.split(arg)
		return [Course.objects.get(pk=int(id)) for id in idset[:-1]]

	return ''


@register.filter(name='commentusername')
def commentusername(userid,t):
	if t==0:
		return Student.objects.get(pk=int(userid)).student_username
	elif t==1:
		return Teacher.objects.get(pk=int(userid)).teacher_username
	else:
		return Administrator.objects.get(pk=int(userid)).administrator_username

@register.filter(name='iscommentted')
def iscommentted(comment,user):
	if comment.coursecomment_userid==user.id and comment.coursecomment_usertype==user.usertype:
		return True
	else:
		return False

@register.filter(name='coursewholecomment')
def coursewholecomment(cList):
	if not cList:
		return 0
	whole=0
	for c in cList:
		whole += c.coursecomment_score

	return '%.1f' % (whole/len(cList))

@register.filter(name='coursecommentlist')
def coursecommentlist(courseid):
	return CourseComment.objects.filter(course__id=int(courseid))


		


