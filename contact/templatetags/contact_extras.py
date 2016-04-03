# -*- coding: utf-8 -*-
# extra tags and filter for template

from django import template
from contact.models import *
from admin.models import *

register = template.Library()

@register.filter(name='answerByType')
def answerByType(queryset,t):
    return queryset.filter(answerquestion_usertype=t)


@register.filter(name='answername')
def answername(id,t):
	if t==0:
		return Student.objects.get(pk=id).student_username
	elif t==1:
		return Teacher.objects.get(pk=id).teacher_username
	else:
		return Administrator.objects.get(pk=id).administrator_username

@register.filter(name='replyername')
def replyername(id,t):
	return answername(id,t)


@register.filter(name='answernums')
def answernums(question):
	return AnswerQuestion.objects.filter(question=question).count()

@register.filter(name='replynums')
def replynums(topic):
	return TopicReply.objects.filter(topic=topic,topicreply_replyid__gt=0).count()

@register.filter(name='answerlasttime')
def answerlasttime(question):
	aqList=AnswerQuestion.objects.filter(question=question).order_by('-answerquestion_time')
	if aqList:
		aq=aqList[0]
		return aq.answerquestion_time
	else:
		return ''

@register.filter(name='answerlastname')
def answerlastname(question):
	aqList=AnswerQuestion.objects.filter(question=question).order_by('-answerquestion_time')
	if aqList:
		aq=aqList[0]
		return answername(aq.answerquestion_userid,aq.answerquestion_usertype)
	else:
		return ''


@register.filter(name='headportrait')
def headportrait(id,t):
	if t==0:
		return Student.objects.get(pk=id).student_head_portrait.url
	elif t==1:
		return Teacher.objects.get(pk=id).teacher_head_portrait.url
	else:
		return None


@register.filter(name='replyername2')
def replyername2(id):
	topicReply=TopicReply.objects.get(pk=id)
	return replyername(topicReply.topicreply_userid,topicReply.topicreply_usertype)


@register.filter(name='replylasttime')
def replylasttime(topic):
	trList=TopicReply.objects.filter(topic=topic).order_by('-topicreply_time')
	if trList:
		return trList[0].topicreply_time
	else:
		return ''

@register.filter(name='topicshield')
def topicshield(info,trid):
	tr=TopicReply.objects.get(pk=trid)
	if not tr.topicreply_status:
		return '<code style="color:#c7254e;padding: 2px 4px;font-size: 16px;">此信息已被管理员屏蔽</code>'
	else:
		return info

@register.filter(name='questionshield')
def questionshield(info,aq):
	# aq=AnswerQuestion.objects.get(pk=aqid)
	if not aq.answerquestion_status:
		return '<code style="color:#c7254e;padding: 2px 4px;font-size: 16px;">此信息已被管理员屏蔽</code>'
	else:
		return info




