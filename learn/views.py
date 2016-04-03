from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.db import transaction
import traceback
from django.core.serializers import serialize
from django.shortcuts import render_to_response,redirect,render
from django.template import RequestContext
from django.http import HttpResponseRedirect

from course.models import Course,Resource
from .models import *
from admin.models import Student,Task
from datetime import *

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# courseware learn initial
def coursewareLearnInitial(request,courseware):
	learn=Learn()
	learn.student=Student.objects.get(pk=request.session['user'].id)
	learn.resource=courseware
	learn.course=courseware.course
	learn.status=learn.learn_rate=learn.learn_times=learn.learn_timelength=learn.learn_standardtimelength=0
	learn.save()

	return learn

# course learn initial 
def courseLearningInitial(learn,task_id):

	courseLearning=CourseLearning()
	courseLearning.course=learn.course
	courseLearning.student=learn.student
	courseLearning.task=Task.objects.get(pk=task_id)
	courseLearning.courselearning_status=True
	courseLearning.courselearning_credit=courseLearning.courselearning_rate=0
	courseLearning.courselearning_timelength=courseLearning.courselearning_standardtimelength=0
	courseLearning.save()

# task learn initial
def taskLearningInitial(learn,task_id):
	taskLearning=TaskLearning()
	taskLearning.student=learn.student
	taskLearning.task=Task.objects.get(pk=task_id)
	taskLearning.tasklearning_status=False
	taskLearning.tasklearning_score=taskLearning.tasklearning_rate=0
	taskLearning.tasklearning_timelength=taskLearning.tasklearning_standardtimelength=0

	taskLearning.save()

# integrate above three initial
def learnInitial(request,task_id,course_id,id):

	student_id=request.session['user'].id
	courseware=Resource.objects.get(pk=id)

	# whether to initial courseware learn base info
	lList=Learn.objects.filter(resource__id=id).filter(student__id=student_id)
	if not lList:
		learn=coursewareLearnInitial(request,courseware)
	else:
		learn=lList[0]

	# whether to initial course learn info
	lcList=CourseLearning.objects.filter(course__id=course_id).filter(student__id=student_id)
	if not lcList:
		courseLearningInitial(learn,task_id)

	# whether to initial task learn info
	tList=TaskLearning.objects.filter(task__id=task_id).filter(student__id=student_id)
	if not tList:
		taskLearningInitial(learn,task_id)

	return learn



# before learn resource
@transaction.commit_on_success
def coursewareView(request,task_id,course_id,id):
	try:
		courseware=Resource.objects.get(pk=id)
		# add courseware view times
		courseware.resource_viewtimes += 1
		courseware.save()

		# inital learn info
		learn=learnInitial(request,task_id,course_id,id)

		# initial learn detail info
		if learn:
			learnDetail=LearnDetail()
			learnDetail.learn=learn
			learnDetail.learn_timelength=0
			learnDetail.save()

		return render_to_response('learn/view.html',{'resource':courseware,'learnDetail':learnDetail},context_instance=RequestContext(request))
	except Exception,e:
		return render_to_response('500.html',{'stackinfo':traceback.format_exc()},context_instance=RequestContext(request))


# ---------- status code ----------
NONE=0
# courseware lean status
(CW_FIRSTLEARN,CW_LEARNING,CW_PASSING,CW_PASSED)=(1,2,3,4)
# course learn status
(CL_FIRSTLEARN,CL_LEARNING,CL_PASSING,CL_PASSED)=(5,6,7,8)
# task status
(TASK_FIRSTLEARN,TASK_LEARNING,TASK_PASSING,TASK_PASSED)=(9,10,11,12)


# after viewing the courseware
def __updateLearn(learnDetail):

	cw_status=NONE
	learn=learnDetail.learn
	standardtime_stamp=learn.resource.resource_standardtime*60-learn.learn_standardtimelength
	learn.learn_timelength += learnDetail.learn_timelength
	# 2014-4-23 add
	learn.learn_standardtimelength += learnDetail.learn_timelength
	# timestamp
	
	if learn.learn_standardtimelength >= learn.resource.resource_standardtime*60:
		learn.learn_standardtimelength=learn.resource.resource_standardtime*60
	else:
		standardtime_stamp=learnDetail.learn_timelength


	# this courseware has passed
	if learn.learn_status==2:
		learn.save()
		cw_status=CW_PASSED

	# update learn times and rate info
	learn.learn_times += 1
	learn.learn_rate = (learn.learn_standardtimelength*100)/(learn.resource.resource_standardtime*60)
	# first viewing the video(have timestamp)
	if learn.learn_timelength>0 and learn.learn_status==0:
		learn.learn_status=1
		cw_status=CW_FIRSTLEARN
	# passed the courseware's standardtime
	elif learn.learn_status==1 and learn.learn_rate>=100:
		learn.learn_status=2
		cw_status=CW_PASSING
	# learning but not passed
	elif learn.learn_status==1 and learn.learn_rate<100:
		cw_status=CW_LEARNING
	elif learn.learn_status==2:
		cw_status=CW_PASSED

	learn.save()
	return (learn,cw_status,standardtime_stamp)

# after update the learn
def __updateCourseLearning(learn,task_id,cw_status,time_length,standardtime_stamp):

	cl_status=NONE
	
	clList=CourseLearning.objects.filter(task__id=task_id) \
		.filter(student=learn.student).filter(course=learn.course)

	cl=clList[0]
	# update the added timelength
	cl.courselearning_timelength = cl.courselearning_timelength+time_length

	# course's all coursewares' standard timelength
	coursetime=learn.course.course_lessonnum
	# for courseware in Resource.objects.filter(course=learn.course):
	# 	if courseware.resource_standardtime:
	# 		coursetime += courseware.resource_standardtime

	cl.courselearning_standardtimelength += standardtime_stamp
	
	# percent
	cl.courselearning_rate=(cl.courselearning_standardtimelength*100)/(coursetime*60)

	# course first learn
	if cl.courselearning_status==0 and cw_status==CW_FIRSTLEARN:
		cl.courselearning_status=1
		cl_status=CL_FIRSTLEARN

	elif cl.courselearning_status==1 and (cw_status==CW_LEARNING or cw_status==CW_FIRSTLEARN 
		or cw_status==CW_PASSED):
		cl_status=CL_LEARNING

	# course is learning and one courseware is passing
	elif cl.courselearning_status==1 and cw_status==CW_PASSING:
		if cl.courselearning_rate>=100:
			cl.courselearning_status=2 #passing
			cl.courselearning_credit=cl.course.course_credit
			cl_status=CL_PASSING
		else:
			cl_status=CL_LEARNING

	elif cl.courselearning_status==2 and cw_status==CW_PASSED:
		cl_status==CL_PASSED

	cl.save()
	return (cl,cl_status)

# after update the course learn info
def __updateTaskLearning(courseLearn,cl_status,time_length,standardtime_stamp):

	task_status=NONE
	task_id=courseLearn.task.id
	student_id=courseLearn.student.id

	courseidset=Task.objects.get(pk=task_id).task_courseids.split(',')[:-1]
	cList=[]
	for courseid in courseidset:
		cList.append(Course.objects.get(pk=int(courseid)))

	tasktime=0
	# course_lessonnum presents course's standard time
	for course in cList:
		tasktime += course.course_lessonnum

	tlList=TaskLearning.objects.filter(student__id=student_id).filter(task__id=task_id)
	tl=tlList[0]

	tl.tasklearning_timelength += time_length
	tl.tasklearning_standardtimelength += standardtime_stamp

	tl.tasklearning_rate = (tl.tasklearning_standardtimelength*100)/(tasktime*60)

	if tl.tasklearning_status==0 and cl_status==CL_FIRSTLEARN:
		tl.tasklearning_status=1
		task_status=TASK_FIRSTLEARN
	elif tl.tasklearning_status==1 and (cl_status==CL_FIRSTLEARN or cl_status==CL_LEARNING or CL_PASSED):
		task_status=TASK_LEARNING
	elif tl.tasklearning_status==1 and cl_status==CL_PASSING:
		
		if tl.tasklearning_rate>=100:
			tl.tasklearning_status=2
			tl.tasklearning_credit += courseLearn.courselearning_credit
			task_status=TASK_PASSING
		else:
			task_status=TASK_LEARNING
	elif tl.tasklearning_status==2 and cl_status==CL_PASSED:
		task_status=TASK_PASSED

	tl.save()
	return (tl,task_status)

# complete viewing resource
@transaction.commit_on_success
def coursewareViewFinish(request,id):
	try:
		learnDetail=LearnDetail.objects.get(pk=id)
		learnDetail.learn_timelength=int(request.GET.get('timelength'))
		learnDetail.save()

		task_id=int(request.GET.get('taskid'))
		# update the learn info
		(learn,cw_status,standardtime_stamp)=__updateLearn(learnDetail)
		# update the course learn info
		(courseLearn,cl_status)=__updateCourseLearning(learn,task_id,cw_status,
			learnDetail.learn_timelength,standardtime_stamp)
		# update the task learn info
		(taskLearn,task_status)=__updateTaskLearning(courseLearn,cl_status,
			learnDetail.learn_timelength,standardtime_stamp)

		return render_to_response('learn/learn_result.html',{'learnDetail':learnDetail},context_instance=RequestContext(request))

	except Exception,e:
		return render_to_response('500.html',{'stackinfo':traceback.format_exc()},context_instance=RequestContext(request))


