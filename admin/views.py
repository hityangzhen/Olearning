# -*- coding: utf-8 -*-
# Create your views here.
from .forms import *
from .models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.db import transaction
import traceback
import os
from django.conf import settings
from django.core.serializers import serialize
from django import forms
from tools.MyExcel import exportImport
import sae
import sae.storage
from olearning.views import islogin
from course.models import Course
from learn.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext


import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# return the coursetype list-json
@csrf_exempt
def coursetypeList(request):
	# param:page | rows
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		ctlist=CourseType.objects.all()
		rawJson={"total":len(ctlist),"rows":toListByPageAndRows(ctlist,page,rows)}
		result=simplejson.dumps(rawJson,ensure_ascii=False)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
		return HttpResponse(simplejson.dumps(result),mimetype='application/json')
# return the coursetype array-json
@csrf_exempt
def coursetypeArray(request):
	try:
		ctlist=CourseType.objects.filter(coursetype_status=True)
		result=simplejson.dumps(toList(ctlist),ensure_ascii=False)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
		return HttpResponse(simplejson.dumps(result),mimetype='application/json')

# to list
def toListByPageAndRows(lists,page,rows):
	newlist=[]
	limitlists=lists[(page-1)*rows:page*rows]
	for item in limitlists:
		newlist.append(item.toDICT())
	return newlist

# to list
def toList(lists):
	newlist=[]
	for item in lists:
		newlist.append(item.toDICT())
	return newlist


# add the coursetype
@transaction.commit_on_success
@islogin
def coursetypeAdd(request):
	# param:coursetype_name | coursetype_positionid | coursetype_status
	result={}
	try:
		coursetype=CourseTypeForm(request.POST)
		# form validate is essential
		if coursetype.is_valid():
			coursetype.save()
			result['status']='success'
			result['tip']='添加成功'
		else:
			result['status']='faliured'
			result['tip']='验证失败'
	except Exception,e:
		# transaction.rollback()
		result['status']='failured'
		result['tip']='添加失败'
		result['error']=traceback.format_exc()
	# else:
	# 	transaction.commit()
	finally:
		return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')

# update the coursetype
@transaction.commit_on_success
def coursetypeUpdate(request):
	# param:id | coursetype_name | coursetype_positionid | coursetype_status
	result={}
	try:
		coursetype=CourseTypeForm(request.POST,instance=CourseType.objects.get(pk=int(request.POST.get('id'))))
		# form validate is essential
		if coursetype.is_valid():
			coursetype.save()
			result['status']='success'
			result['tip']='保存成功'
		else:
			result['status']='faliured'
			result['tip']='验证失败'
	except Exception,e:
		result['status']='failured'
		result['tip']='保存失败'
		result['error']=traceback.format_exc()
	# else:
	# 	transaction.commit()
	finally:
		return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')

@transaction.commit_manually
@csrf_exempt
def coursetypeDelete(request):
	# param:id
	result={}
	idset=request.POST.get('id').split(',')[:-1]
	try:
		for id in idset:
			CourseType.objects.get(pk=int(id)).delete()
		result['status']='success'
		result['tip']='删除成功'
	except Exception,e:
		transaction.rollback()
		result['status']='failured'
		result['tip']='删除失败'
		result['error']=traceback.format_exc()
	else:
		transaction.commit()
	finally:
		return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')


# find the coursetype by id
def coursetypeFindById(request,id):
	# param:id
	coursetype=CourseType.objects.get(pk=id)
	return HttpResponse(simplejson.dumps(coursetype.toDICT(),ensure_ascii=False),mimetype='application/json')

#--------------------------------------------------2014-3-31 add----------------------------------------------

# default list json
def listJsonResult(modellist,page,rows):
	d={}
	d['total']=len(modellist)
	lists=simplejson.loads(serialize('json',modellist[(page-1)*rows : page*rows]))
	d['rows']=lists
	return simplejson.dumps(d,ensure_ascii=False)

# return student list
def studentList(request):
	# param:page | rows
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		studentlist=Student.objects.all()
		result=listJsonResult(studentlist,page,rows)
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
	finally:
		return HttpResponse(result,mimetype='application/json')

#--------------------------------------------------2014-4-1 add----------------------------------------------
# return teacher list

def teacherList(request):
	# param:page | rows
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		teacherlist=Teacher.objects.all()
		result=listJsonResult(teacherlist,page,rows)
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
	finally:
		return HttpResponse(result,mimetype='application/json')

def handle_uploaded_file(f):
	# for client debug
	if settings.DEBUG:
		destination = open(settings.MEDIA_ROOT+'temp/'+f.name, 'wb+')
		for chunk in f.chunks():
			destination.write(chunk)
		destination.close() 
	# for sae
	else:
		s = sae.storage.Client()
		ob = sae.storage.Object(f.read())
		url =s.put('resources','temp/'+f.name, ob)
	return f

# import userinfo
@csrf_exempt
def userImport(request,tp):
	# param:type
	result={}
	try:
		f=handle_uploaded_file(request.FILES['userfile'])
		result=exportImport('temp/'+f.name,int(tp))
	except Exception,e:
		result['status']='error'
		result['tip']=traceback.format_exc()
	finally:
		print result
		return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')


#--------------------------------------------------2014-4-2 add----------------------------------------------
# save the student
@transaction.commit_manually
def studentAdd(request):
	result={}
	try:
		studentForm=StudentForm(request.POST,request.FILES)
		if studentForm.is_valid():

			student_identity=request.POST.get('student_identity')
			if Student.objects.filter(student_identity=student_identity):
				result['status']='failured'
				result['tip']='此学员已存在'
			else:	
				student=studentForm.save(commit=False)
				student.student_ischecked=False
				student.student_status=True
				# set the userpwd
				if request.POST.get('student_userpwd'):
					student.student_userpwd=request.POST.get('student_userpwd')
				else:
					student.student_userpwd=((request.POST.get('student_identity')[::-1])[0:6])[::-1]

				student.save()
				result['status']='success'
				result['tip']='保存成功'
				
		else:
			result['status']='faliured'
			result['tip']='验证失败'
			result['error']=studentForm.errors
	except Exception,e:
		transaction.rollback()
		result['status']='failured'
		result['tip']='保存失败'
		result['error']=traceback.format_exc()
	else:
		transaction.commit()
	finally:
		return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')

# delete the student
@transaction.commit_manually
@csrf_exempt
def studentDelete(request):
	result={}
	try:
		student_idset=request.POST.get('student_idset')
		idset=student_idset.split(',')
		for i in range(0,len(idset)-1):
			Student.objects.get(pk=int(idset[i])).delete()

		result['status']='success'
		result['tip']='删除成功'
		transaction.commit()
	except Exception,e:
		transaction.rollback()
		result['status']='faliured'
		result['tip']='删除失败'
		result['error']=traceback.format_exc()
	finally:
		return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')

# update the student
@transaction.commit_manually
def studentUpdate(request,id):
	result={}
	try:
		instance=Student.objects.get(pk=id)
		if request.FILES and instance.student_head_portrait :
			instance.student_head_portrait.storage.delete(instance.student_head_portrait.name)

		studentForm=StudentForm(request.POST,request.FILES,instance=instance)
		if studentForm.is_valid():
			student=studentForm.save()
			# set the userpwd
			if request.POST.get('student_userpwd'):
				student.student_userpwd=request.POST.get('student_userpwd')
			else:
				student.student_userpwd=((request.POST.get('student_identity')[::-1])[0:6])[::-1]
			student.save()
			result['status']='success'
			result['tip']='保存成功'
			transaction.commit()
		else:
			result['status']='faliured'
			result['tip']='验证失败'
			result['error']=studentForm.errors
	except Exception,e:
		transaction.rollback()
		result['status']='failured'
		result['tip']='保存失败'
		result['error']=traceback.format_exc()
	finally:
		return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')

# save the teacher
@transaction.commit_manually
def teacherAdd(request):
	result={}
	try:
		teacherForm=TeacherForm(request.POST,request.FILES)
		if teacherForm.is_valid():

			teacher_identity=request.POST.get('teacher_identity')
			print teacher_identity
			if Teacher.objects.filter(teacher_identity=teacher_identity):
				result['status']='failured'
				result['tip']='此教师已存在'
			else:	
				teacher=teacherForm.save(commit=False)
				teacher.teacher_ischecked=False
				teacher.teacher_status=True

				# set the userpwd
				if request.POST.get('teacher_userpwd'):
					teacher.teacher_userpwd=request.POST.get('teacher_userpwd')
				else:
					teacher.teacher_userpwd=((request.POST.get('teacher_identity')[::-1])[0:6])[::-1]
				teacher.save()
				result['status']='success'
				result['tip']='保存成功'
				
		else:
			result['status']='faliured'
			result['tip']='验证失败'
			result['error']=teacherForm.errors
	except Exception,e:
		transaction.rollback()
		result['status']='failured'
		result['tip']='保存失败'
		result['error']=traceback.format_exc()
	else:
		transaction.commit()
	finally:
		return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')

# delete the teacher
@transaction.commit_manually
@csrf_exempt
def teacherDelete(request):
	result={}
	try:
		teacher_idset=request.POST.get('teacher_idset')
		idset=teacher_idset.split(',')
		for i in range(0,len(idset)-1):
			Teacher.objects.get(pk=int(idset[i])).delete()

		result['status']='success'
		result['tip']='删除成功'
		transaction.commit()
	except Exception,e:
		transaction.rollback()
		result['status']='faliured'
		result['tip']='删除失败'
		result['error']=traceback.format_exc()
	finally:
		return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')

# update the teacher
@transaction.commit_manually
def teacherUpdate(request,id):
	result={}
	try:
		# delete the original head_portrait
		instance=Teacher.objects.get(pk=id)
		if request.FILES and instance.teacher_head_portrait :
			instance.teacher_head_portrait.storage.delete(instance.teacher_head_portrait.name)

		teacherForm=TeacherForm(request.POST,request.FILES,instance=instance)
		if teacherForm.is_valid():
			teacher=teacherForm.save()
			# set the userpwd
			if request.POST.get('teacher_userpwd'):
				teacher.teacher_userpwd=request.POST.get('teacher_userpwd')
			else:
				teacher.teacher_userpwd=((request.POST.get('teacher_identity')[::-1])[0:6])[::-1]

			teacher.save()
			result['status']='success'
			result['tip']='保存成功'
			transaction.commit()
		else:
			result['status']='faliured'
			result['tip']='验证失败'
			result['error']=teacherForm.errors
	except Exception,e:
		transaction.rollback()
		result['status']='failured'
		result['tip']='保存失败'
		result['error']=traceback.format_exc()
	finally:
		return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')


#--------------------------------------------------2014-4-14 add----------------------------------------------
# add the task
@transaction.commit_on_success
def taskAdd(request):
	result={}
	try:
		taskForm=TaskForm(request.POST)
		if taskForm.is_valid():
			coursetype_id=request.POST.get('coursetype_id')
			coursetype=CourseType.objects.get(pk=int(coursetype_id))
			task=taskForm.save(commit=False)
			task.coursetype=coursetype

			if request.POST.get('publish')=='1':
				task.task_ispublished=True


			task.save()
			result['status']='success'
			result['tip']='保存成功'
		else:
			result['status']='faliured'
			result['tip']='验证失败'
			result['error']=taskForm.errors
	except Exception,e:
		transaction.rollback()
		result['status']='failured'
		result['tip']='保存失败'
		result['error']=traceback.format_exc()
	finally:
		return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')

# task list json
def __taskListJsonResult(tlist,page,rows):
	d={}
	d['total']=len(tlist)
	lists=simplejson.loads(serialize('json',tlist[(page-1)*rows : page*rows]))

	for l in lists:
		# add coursetype info
		ct=CourseType.objects.get(pk=int(l['fields']['coursetype']))
		l['fields']['coursetype']=simplejson.loads(serialize('json',[ct])[1:-1])

		# add course info
		courseidset=l['fields']['task_courseids'].split(',')
		course=''
		for id in courseidset[:-1]:
			course += '%s    |    ' % (Course.objects.get(pk=int(id)).course_name)
		l['fields']['task_courseids']=course

	d['rows']=lists
	return simplejson.dumps(d,ensure_ascii=False)

# return task list
def taskList(request):
	result={}
	# param:page | rows
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		tlist=Task.objects.all()
		result=__taskListJsonResult(tlist,page,rows)
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
	finally:
		return HttpResponse(result,mimetype='application/json')

#--------------------------------------------------2014-4-15 add----------------------------------------------
@transaction.commit_on_success
def taskUpdate(request,id):
	result={}
	try:
		task=Task.objects.get(pk=id)
		taskForm=TaskForm(request.POST,instance=task)
		if taskForm.is_valid():
			task=taskForm.save(commit=False)

			if request.POST.get('publish')=='1':
				task.task_ispublished=True

			task.save()
			result['status']='success'
			result['tip']='保存成功'
		else:
			result['status']='faliured'
			result['tip']='验证失败'
			result['error']=taskForm.errors
	except Exception,e:
		transaction.rollback()
		result['status']='failured'
		result['tip']='保存失败'
		result['error']=traceback.format_exc()
	finally:
		return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')

@transaction.commit_on_success
def taskDelete(request,id):
	result={}
	try:
		task=Task.objects.get(pk=id)
		task.delete()
		result['status']='success'
		result['tip']='删除成功'

	except Exception,e:
		transaction.rollback()
		result['status']='faliured'
		result['tip']='删除失败'
		result['error']=traceback.format_exc()
	finally:
		return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')


@transaction.commit_on_success
def taskPublish(request,id):
	result={}
	try:
		task=Task.objects.get(pk=id)
		task.task_ispublished=True
		task.save()

		result['status']='success'
		result['tip']='发布成功'
		
	except Exception,e:
		transaction.rollback()
		result['status']='faliured'
		result['tip']='发布失败'
		result['error']=traceback.format_exc()
	finally:
		return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')

#--------------------------------------------------2014-4-18 add----------------------------------------------
# return student's task json list
def studentTaskList(request,id):
	result={}
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))
		# match the task and the student by positionid
		student=Student.objects.get(pk=id)
		tlist=Task.objects.filter(coursetype__coursetype_positionid=student.student_positionid)
		result=__studentTaskListJsonResult(tlist,page,rows,request.session['user'].id)
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
	finally:
		return HttpResponse(result,mimetype='application/json')

# student task list json
def __studentTaskListJsonResult(tlist,page,rows,student_id):
	d={}
	d['total']=len(tlist)
	lists=simplejson.loads(serialize('json',tlist[(page-1)*rows : page*rows]))

	for l in lists:
		# add coursetype info
		ct=CourseType.objects.get(pk=int(l['fields']['coursetype']))
		l['fields']['coursetype']=simplejson.loads(serialize('json',[ct])[1:-1])

		# add course info
		courseidset=l['fields']['task_courseids'].split(',')
		course=''
		for id in courseidset[:-1]:
			course += '%s    |    ' % (Course.objects.get(pk=int(id)).course_name)
		l['fields']['task_courseids']=course

		tlList=TaskLearning.objects.filter(student__id=student_id).filter(task__id=l['pk'])

		l['task_precent']=0
		l['task_status']=0

		if tlList:
			l['task_precent']=tlList[0].tasklearning_rate
			l['task_status']=tlList[0].tasklearning_status

	d['rows']=lists
	return simplejson.dumps(d,ensure_ascii=False)

import learn.views
def showStudentTaskDetailList(request,id):
	courseidset=Task.objects.get(pk=id).task_courseids.split(',')[:-1]
	for courseid in courseidset:
		# if first accept the task ,should initial learn
		coursewareidset=Resource.objects.filter(course__id=int(courseid),resource_iscourseware=True)
		for cw in coursewareidset:
			learn.views.learnInitial(request,id,int(courseid),cw.id)
		
	return render_to_response('admin/student_taskdetail.html',context_instance=RequestContext(request))

#--------------------------------------------------2014-4-23 add----------------------------------------------
# return student's task course learn detail info
def studentTaskDetailList(request,id):
	result={}
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		student=Student.objects.get(pk=request.session['user'].id)

		clList=CourseLearning.objects.filter(task__id=id).filter(student=student)
		result=__studentTaskDetailListJsonResult(clList,page,rows)
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
	finally:
		return HttpResponse(result,mimetype='application/json')
		
# 
def __studentTaskDetailListJsonResult(cllist,page,rows):
	d={}
	d['total']=len(cllist)
	lists=simplejson.loads(serialize('json',cllist[(page-1)*rows : page*rows]))

	for l in lists:
		# add course info
		c=Course.objects.get(pk=int(l['fields']['course']))
		l['fields']['course']=simplejson.loads(serialize('json',[c])[1:-1])

	d['rows']=lists
	return simplejson.dumps(d,ensure_ascii=False)

# return student's task courseware learn info
def studentTaskCoursewareList(request,taskid,courseid):
	result={}
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		lList=[]
		cwList=Resource.objects.filter(course__id=courseid,resource_iscourseware=True)

		for cw in cwList:
			l=Learn.objects.filter(resource=cw,student__id=request.session['user'].id)
			if l:
				lList.append(l[0])
			else:
				lList.append(Learn(resource=cw,learn_status=0,learn_timelength=0,learn_rate=0))

		result=__studentTaskCoursewareListJsonResult(lList,page,rows)

	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
	finally:
		return HttpResponse(result,mimetype='application/json')

def __studentTaskCoursewareListJsonResult(lList,page,rows):
	d={}
	d['total']=len(lList)
	lists=simplejson.loads(serialize('json',lList[(page-1)*rows : page*rows]))

	for l in lists:
		# add resource info
		r=Resource.objects.get(pk=int(l['fields']['resource']))
		l['fields']['resource']=simplejson.loads(serialize('json',[r])[1:-1])
	d['rows']=lists
	return simplejson.dumps(d,ensure_ascii=False)


# return message info
def messageList(request):
	result={}
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))
		msgtype=int(request.GET.get('type'))
		mList=Message.objects.filter(message_type=msgtype,message_receiverid=request.session['user'].id,
			message_receivertype=request.session['user'].usertype).order_by('-message_starttime')
		result=__messageListJson(mList,page,rows)

	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
	finally:
		return HttpResponse(result,mimetype='application/json')


def __messageListJson(mList,page,rows):
	d={}
	d['total']=len(mList)
	lists=simplejson.loads(serialize('json',mList[(page-1)*rows : page*rows]))

	for l in lists:
		# add sender user info
		usertype=int(l['fields']['message_sendertype'])
		userid=int(l['fields']['message_senderid'])
		if usertype == 0:
			username=Student.objects.get(pk=userid).student_username
		elif usertype == 1:
			username='教师-'+Teacher.objects.get(pk=userid).teacher_username
		else:
			username='管理员-'+Administrator.objects.get(pk=userid).administrator_username

		l['fields']['message_sender']=username
	d['rows']=lists
	return simplejson.dumps(d,ensure_ascii=False)

# handler the message
def messageHandler(request,id):
	result={}
	try:
		msg=Message.objects.get(pk=id)
		msg.message_ishandlered=True
		msg.save()

		result['status']='success'
		result['tip']='处理成功'
		
	except Exception,e:
		transaction.rollback()
		result['status']='faliured'
		result['tip']='处理失败'
		result['error']=traceback.format_exc()
	finally:
		return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')


MSGINFO=('','系统消息','任务消息','课程消息','练习消息','讨论消息','学习消息')

def __messageInfo(mList):
	info=''
	count=0

	for i in range(1,len(MSGINFO)):
		count=mList.filter(message_type=i).count()
		if count>0:
			info +='您有 <font color="red">%d</font> 条 %s 未处理\n' %(count,MSGINFO[i])

	return info
# 
def hasUnhandleredMsg(request):
	result={}
	try:
		msg=Message.objects.filter(message_receiverid=request.session['user'].id,
			message_receivertype=request.session['user'].usertype,message_ishandlered=False)

		if msg:
			result['status']='success'
			result['tip']=__messageInfo(msg)
		else:
			result['status']='failure'
			result['tip']='无任何未处理的消息'
		
	except Exception,e:

		result['status']='faliured'
		result['tip']='查询失败'
		result['error']=traceback.format_exc()
	finally:
		return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')	










