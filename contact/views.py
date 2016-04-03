# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.db import transaction
import traceback
from django.core.serializers import serialize
from django.shortcuts import render_to_response,redirect,render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from course.models import Course
from .models import *
from datetime import *
from admin.models import Message
from django.conf import settings


import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def __fulltimeformat(datetime):
    if datetime:
        date=datetime.date()
        time=datetime.time()
        return '%d-%d-%d %d:%d:%d' % (date.year,date.month,date.day,time.hour,time.minute,time.second)
    return ''


# override the render_to_response
def __response(template,d,request):
	if not d:
		d={}
	return render_to_response(template,d,context_instance=RequestContext(request))

# return ask question list
def askQuestionList(request,id):
	try:
		qList=Question.objects.filter(course__id=id).order_by('-question_starttime')
	except Exception,e:
		return __response('500.html',{'stackinfo':traceback.format_exc()},request)
	else:
		return __response('contact/ask_question_list.html',{'qList':qList},request)

# add the question
@transaction.commit_on_success
def saveQuestion(request):
	try:
		course=Course.objects.get(pk=int(request.POST.get('courseid')))
		student=Student.objects.get(pk=request.session['user'].id)
		question=Question(question_status=True,question_viewtimes=0,course=course,student=student)
		question.question_title=request.POST.get('question_title')
		question.question_content=request.POST.get('question_content')
		question.save()


		# send message to course's teacher
		m=Message(message_type=settings.CONTACTMSG,message_ishandlered=False,
			message_receiverid=course.teacher.id,message_receivertype=1,
			message_senderid=request.session['user'].id,message_sendertype=request.session['user'].usertype)
		
		m.message_content='一位同学提出了关于您课程的新的疑问'
		m.save()

		url='/contact/ask_question/%d/list/' % course.id
	except Exception,e:
		return __response('500.html',{'stackinfo':traceback.format_exc()},request)
	else:
		return HttpResponseRedirect(url)

# return the question detail and the answers
def askQuestionAnswer(request,id):
	try:
		question=Question.objects.get(pk=id)
		# add viewtimes
		question.question_viewtimes += 1
		question.save()

		answerQuestion=AnswerQuestion.objects.filter(question=question).order_by('-answerquestion_time')
	except Exception,e:
		return __response('500.html',{'stackinfo':traceback.format_exc()},request)
	else:
		return __response('contact/ask_question_detail.html',
			{'question':question,'answerQuestion':answerQuestion},request)

# answer the question
@transaction.commit_on_success
def answerQuestion(request,id):
	try:
		question=Question.objects.get(pk=id)
		answerQuestion=AnswerQuestion(answerquestion_status=True,question=question)
		answerQuestion.answerquestion_content=request.POST.get('answerquestion_content')
		answerQuestion.answerquestion_userid=request.session['user'].id
		answerQuestion.answerquestion_usertype=request.session['user'].usertype
		answerQuestion.save()

		# send message to question owner
		m=Message(message_type=settings.CONTACTMSG,message_ishandlered=False,
			message_receiverid=question.student.id,message_receivertype=0,
			message_senderid=request.session['user'].id,message_sendertype=request.session['user'].usertype)

		if m.message_sendertype==0:
			m.message_content='一位同学回复了你的疑问-'+question.question_title
		else:
			m.message_content='一位教师回复了你的疑问-'+question.question_title
		m.save()

		url='/contact/ask_question/detail/%d/' % question.id
	except Exception,e:
		return __response('500.html',{'stackinfo':traceback.format_exc()},request)
	else:
		return HttpResponseRedirect(url)		

@transaction.commit_on_success
def deleteQuestion(request,id):
	try:
		question=Question.objects.get(pk=id)
		url='/contact/ask_question/%d/list/' % question.course.id
		question.delete()

	except Exception,e:
		return __response('500.html',{'stackinfo':traceback.format_exc()},request)
	else:
		return HttpResponseRedirect(url)

# 
@transaction.commit_on_success
def deleteAnswerQuestion(request,aq_id):
	try:
	
		aq=AnswerQuestion.objects.get(pk=aq_id)
		url='/contact/ask_question/detail/%d/' % aq.question.id
		aq.delete()

	except Exception,e:
		return __response('500.html',{'stackinfo':traceback.format_exc()},request)
	else:
		return HttpResponseRedirect(url)


def __courseQuestionGeneralListJson(cList,page,rows):
	d={}
	d['total']=len(cList)
	l=[]
	cl=cList[(page-1)*rows : page*rows]
	for c in cl:
		temp={}
		temp['course_name']=c.course_name
		temp['course_id']=c.id
		ql=c.question_set
		temp['question_nums']=ql.count()
		if temp['question_nums']==0:
			temp['question_lastanswer']=''
		else:
			time=ql.order_by('-question_starttime')[0].question_starttime

			temp['question_lastanswer']=__fulltimeformat(time)
		l.append(temp)

	d['rows']=l
	return simplejson.dumps(d,ensure_ascii=False)

# 
def courseQuestionGeneralList(request):
	# param:page | rows
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		cList=Course.objects.filter(course_status=True)
		result=__courseQuestionGeneralListJson(cList,page,rows)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
		return HttpResponse(simplejson.dumps(result),mimetype='application/json')

# return launch topic list
def launchTopicList(request,id):
	try:
		tList=Topic.objects.filter(course__id=id).order_by('-topic_starttime')

	except Exception,e:
		return __response('500.html',{'stackinfo':traceback.format_exc()},request)
	else:
		return __response('contact/launch_topic_list.html',{'tList':tList},request)

# add reply
@transaction.commit_manually
def saveTopic(request):
	try:
		course=Course.objects.get(pk=int(request.POST.get('courseid')))
		topic=Topic(topic_status=True,topic_viewtimes=0,course=course)
		topic.topic_title=request.POST.get('topic_title')
		topic.topic_content=request.POST.get('topic_content')
		topic.topic_userid=request.session['user'].id
		topic.topic_usertype=request.session['user'].usertype
		topic.save()

		# add self topic as the first reply
		topicReply=TopicReply(topicreply_title=topic.topic_title,topicreply_content=topic.topic_content,
			topicreply_replyid=0,topicreply_userid=topic.topic_userid,topicreply_usertype=topic.topic_usertype,
			topic=topic,topicreply_status=True,topicreply_isreply=True)

		topicReply.save()
		url='/contact/launch_topic/%d/list/' % course.id
		transaction.commit()
	except Exception,e:
		transaction.rollback()
		return __response('500.html',{'stackinfo':traceback.format_exc()},request)
	else:

		return HttpResponseRedirect(url)

# return topic replys info
@transaction.commit_on_success
def launchTopicReply(request,id):
	try:
		topic=Topic.objects.get(pk=id)
		# add viewtimes
		topic.topic_viewtimes += 1
		topic.save()

		topicReply=TopicReply.objects.filter(topic=topic).order_by('topicreply_time')

	except Exception,e:
		return __response('500.html',{'stackinfo':traceback.format_exc()},request)
	else:
		return __response('contact/launch_topic_detail.html',
			{'topic':topic,'topicReply':topicReply,'firstReply':topicReply[0]},request)

def __sendTopicReplyMessage(request,topicReply):

	parentTopicReply=TopicReply.objects.get(pk=topicReply.topicreply_replyid)

	# send message to parent topic reply
	m=Message(message_type=settings.CONTACTMSG,message_ishandlered=False,
		message_receiverid=parentTopicReply.topicreply_userid,
		message_receivertype=parentTopicReply.topicreply_usertype,
		message_senderid=request.session['user'].id,message_sendertype=request.session['user'].usertype)

	m.message_content='有人回复了你的留言-'+parentTopicReply.topicreply_content
	m.save()


# reply the topic
@transaction.commit_on_success
def replyTopic(request,id):
	try:
		topic=Topic.objects.get(pk=id)
		replyid=int(request.POST.get('replyid'))
		isreply=bool(int(request.POST.get('topicreply_isreply')))
		level=request.POST.get('level')

		if isreply:
			title='回复 %s #' % level
			referencecontent=''
		else:
			title='引用 %s #' % level
			referencecontent=TopicReply.objects.get(pk=replyid).topicreply_content

		topicReply=TopicReply(topicreply_title=title,topicreply_content=request.POST.get('topicreply_content'),
			topicreply_replyid=replyid,topicreply_userid=request.session['user'].id,
			topicreply_usertype=request.session['user'].usertype,topic=topic,topicreply_status=True,
			topicreply_isreply=isreply,topicreply_referencecontent=referencecontent)

		topicReply.save()

		# send message
		__sendTopicReplyMessage(request,topicReply)

		url='/contact/launch_topic/detail/%d/' % topic.id
	except Exception,e:
		return __response('500.html',{'stackinfo':traceback.format_exc()},request)
	else:
		return HttpResponseRedirect(url)	




# delete the topic
@transaction.commit_on_success
def deleteTopic(request,id):
	try:
		topic=Topic.objects.get(pk=id)
		url='/contact/launch_topic/%d/list/' % topic.course.id
		topic.delete()
	except Exception,e:
		return __response('500.html',{'stackinfo':traceback.format_exc()},request)
	else:

		return HttpResponseRedirect(url)


def __courseTopicGeneralListJson(cList,page,rows):
	d={}
	d['total']=len(cList)
	l=[]
	cl=cList[(page-1)*rows : page*rows]
	for c in cl:
		temp={}
		temp['course_name']=c.course_name
		temp['course_id']=c.id
		tl=c.topic_set
		temp['topic_nums']=tl.count()
		if temp['topic_nums']==0:
			temp['topic_lastreply']=''			
		else:
			time=tl.order_by('-topic_starttime')[0].topic_starttime

			temp['topic_lastreply']=__fulltimeformat(time)
		l.append(temp)

	d['rows']=l
	return simplejson.dumps(d,ensure_ascii=False)

# 
def courseTopicGeneralList(request):
	# param:page | rows
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		cList=Course.objects.filter(course_status=True)
		result=__courseTopicGeneralListJson(cList,page,rows)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
		return HttpResponse(simplejson.dumps(result),mimetype='application/json')

# administrator access
# return course question detail list
def courseQuestionDetailList(request,id):
	# param:page | rows
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		qList=Question.objects.filter(course__id=id)
		result=__courseQuestionDetailListJson(qList,page,rows)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
		return HttpResponse(simplejson.dumps(result),mimetype='application/json')


def __courseQuestionDetailListJson(qList,page,rows):
	d={}
	d['total']=len(qList)

	lists=simplejson.loads(serialize('json',qList[(page-1)*rows : page*rows]))

	for l in lists:
		aqList=AnswerQuestion.objects.filter(question__id=int(l['pk']))
		l['question_answernums']=aqList.count()
		l['question_lastanswer']=''
		if aqList:
			l['question_lastanswer']=__fulltimeformat(aqList.order_by('-answerquestion_time')[0].answerquestion_time)
	d['rows']=lists
	return simplejson.dumps(d,ensure_ascii=False)

# ajax request delete the question
@transaction.commit_on_success
def ajaxDeleteQuesiton(request,id):
	result={}
	try:
		question=Question.objects.get(pk=id)
		question.delete()

		# send message to question owner
		m=Message(message_type=settings.CONTACTMSG,message_ishandlered=False,
			message_receiverid=question.question_userid,message_receivertype=question.question_usertype,
			message_senderid=request.session['user'].id,message_sendertype=request.session['user'].usertype)
		
		m.message_content='管理猿删除了你的提问-'+question.question_title
		m.save()

		result['status']='success'
		result['tip']='删除成功'

	except Exception,e:
		result['status']='failured'
		result['tip']='删除失败'
		result['error']=traceback.format_exc()
	return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')


# return answer question list json
def __answerQuestionListJson(aqList,page,rows):
	d={}
	d['total']=len(aqList)

	lists=simplejson.loads(serialize('json',aqList[(page-1)*rows : page*rows]))

	d['rows']=lists
	return simplejson.dumps(d,ensure_ascii=False)

# administrator available
# return answer question list
def answerQuestionList(request,id):
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		question=Question.objects.get(pk=id)
		aqList=AnswerQuestion.objects.filter(question=question)

		result=__answerQuestionListJson(aqList,page,rows)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
		return HttpResponse(simplejson.dumps(result),mimetype='application/json')

# administrator available
# shield the answerquestion
@transaction.commit_on_success
def answerQuestionShield(request,id):
	result={}
	try:
		aq=AnswerQuestion.objects.get(pk=id)
		aq.answerquestion_status=False
		aq.save()

		# send message to answer
		m=Message(message_type=settings.CONTACTMSG,message_ishandlered=False,
			message_receiverid=aq.answerquestion_userid,message_receivertype=aq.answerquestion_usertype,
			message_senderid=request.session['user'].id,message_sendertype=request.session['user'].usertype)
		
		m.message_content='管理猿屏蔽了你对此提问的回复-'+aq.answerquestion_content
		m.save()

		result['status']='success'
		result['tip']='屏蔽成功'

	except Exception,e:
		result['status']='failured'
		result['tip']='屏蔽失败'
		result['error']=traceback.format_exc()
	return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')

# administrator available
# delete the answerquestion
@transaction.commit_on_success
def answerQuestionDelete(request,id):
	result={}
	try:
		aq=AnswerQuestion.objects.get(pk=id)
		aq.delete()
		result['status']='success'
		result['tip']='删除成功'

		# send message to answer
		m=Message(message_type=settings.CONTACTMSG,message_ishandlered=False,
			message_receiverid=aq.answerquestion_userid,message_receivertype=aq.answerquestion_usertype,
			message_senderid=request.session['user'].id,message_sendertype=request.session['user'].usertype)
		
		m.message_content='管理猿删除了你对此提问的回复-'+aq.answerquestion_content
		m.save()

	except Exception,e:
		result['status']='failured'
		result['tip']='删除失败'
		result['error']=traceback.format_exc()
	return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')



# administrator access
# return course topic detail list
def courseTopicDetailList(request,id):
	# param:page | rows
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		tList=Topic.objects.filter(course__id=id)
		result=__courseTopicDetailListJson(tList,page,rows)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
		return HttpResponse(simplejson.dumps(result),mimetype='application/json')


def __courseTopicDetailListJson(tList,page,rows):
	d={}
	d['total']=len(tList)

	lists=simplejson.loads(serialize('json',tList[(page-1)*rows : page*rows]))

	for l in lists:
		trList=TopicReply.objects.filter(topic__id=int(l['pk']))
		l['topic_replynums']=trList.filter(topicreply_replyid__gt=0).count()
		l['topic_lastreply']=''
		if trList:
			l['topic_lastreply']=__fulltimeformat(trList.order_by('-topicreply_time')[0].topicreply_time)
	d['rows']=lists
	return simplejson.dumps(d,ensure_ascii=False)


# return topic reply  list json
def __replyTopicListJson(trList,page,rows):
	d={}
	d['total']=len(trList)

	lists=simplejson.loads(serialize('json',trList[(page-1)*rows : page*rows]))

	d['rows']=lists
	return simplejson.dumps(d,ensure_ascii=False)

# administrator available
# return topic reply list
def replyTopicList(request,id):
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		topic=Topic.objects.get(pk=id)
		trList=TopicReply.objects.filter(topic=topic)

		result=__replyTopicListJson(trList,page,rows)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
		return HttpResponse(simplejson.dumps(result),mimetype='application/json')

# shield the replytopic
@transaction.commit_on_success
def replyTopicShield(request,id):
	result={}
	try:
		tr=TopicReply.objects.get(pk=id)
		tr.topicreply_status=False
		tr.save()

		# send message to replyer
		m=Message(message_type=settings.CONTACTMSG,message_ishandlered=False,
			message_receiverid=tr.topicreply_userid,message_receivertype=tr.topicreply_usertype,
			message_senderid=request.session['user'].id,message_sendertype=request.session['user'].usertype)
		
		m.message_content='管理猿屏蔽了你的回复-'+tr.topicreply_content

		m.save()

		result['status']='success'
		result['tip']='屏蔽成功'

	except Exception,e:
		result['status']='failured'
		result['tip']='屏蔽失败'
		result['error']=traceback.format_exc()
	return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')

# ajax request delete the topic
@transaction.commit_on_success
def ajaxDeleteTopic(request,id):
	result={}
	try:
		topic=Topic.objects.get(pk=id)
		topic.delete()

		# send message to topic owner
		m=Message(message_type=settings.CONTACTMSG,message_ishandlered=False,
			message_receiverid=topic.topic_userid,message_receivertype=topic.topic_usertype,
			message_senderid=request.session['user'].id,message_sendertype=request.session['user'].usertype)
		
		m.message_content='管理猿删除了你的话题-'+topic.topic_title
		m.save()


		result['status']='success'
		result['tip']='删除成功'

	except Exception,e:
		result['status']='failured'
		result['tip']='删除失败'
		result['error']=traceback.format_exc()
	return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')


