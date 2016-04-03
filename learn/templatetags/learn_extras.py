# -*- coding: utf-8 -*-
# extra tags and filter for template
from learn.models import Learn,LearnDetail,CourseLearning
from django import template

register = template.Library()

@register.filter(name='timelength')
def timelength(second):

	if not second:
		return '0 秒'
	second=int(second)
	hour=second/3600
	minite=(second%3600)/60
	second=(second%3600)%60

	timestr=''
	if hour:
		timestr += '%d 小时' %(hour)
	if minite:
		timestr += '%d 分' %(minite)
	if second:
		timestr += '%d 秒' %(second)
	return timestr

@register.filter(name='timesum')
def timesum(learn):
	ldList=LearnDetail.objects.filter(learn=learn)
	s=0
	for ld in ldList:
		s += ld.learn_timelength
	return s

@register.filter(name='courselearn')
def courselearn(courseid):
	return CourseLearning.objects.filter(course__id=courseid)