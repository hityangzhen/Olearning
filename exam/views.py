# -*- coding: utf-8 -*-
from .models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.db import transaction
import traceback
from django.core.serializers import serialize
from django.shortcuts import render_to_response,redirect,render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from .forms import ExerciseTypeForm,ExerciseForm,ExercisePaperForm
from course.models import Course
from django.db.models import Max,Min
from admin.models import Message
from django.conf import settings

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

#
def __exercisetypeListJsonResult(etlist,page,rows):
	d={}
	d['total']=len(etlist)

	lists=simplejson.loads(serialize('json',etlist[(page-1)*rows : page*rows]))
	d['rows']=lists
	return simplejson.dumps(d,ensure_ascii=False)

# return the exercisetype list-json
@csrf_exempt
def exercisetypeList(request):
	# param:page | rows
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		etlist=ExerciseType.objects.all()
		result=__exercisetypeListJsonResult(etlist,page,rows)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
		return HttpResponse(simplejson.dumps(result),mimetype='application/json')

@transaction.commit_on_success
def exercisetypeSave(request):
	result={}
	try:
		exerciseTypeForm=ExerciseTypeForm(request.POST)
		notice=exerciseTypeForm.save(commit=False)
		notice.save()
		result['status']='success'
		result['tip']='保存成功'

	except Exception,e:
		result['status']='failured'
		result['tip']='保存失败'
		result['error']=traceback.format_exc()
	return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')

@transaction.commit_on_success
def exercisetypeUpdate(request):
	result={}
	try:
		instance=ExerciseType.objects.get(pk=int(request.POST.get('id')))
		exerciseTypeForm=ExerciseTypeForm(request.POST,instance=instance)
		exerciseTypeForm.save()
		result['status']='success'
		result['tip']='保存成功'

	except Exception,e:
		result['status']='failured'
		result['tip']='保存失败'
		result['error']=traceback.format_exc()
	return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')


def __exerciseGeneralListJson(clist,page,rows):
	d={}
	lists=[]
	d['total']=len(clist)
	new_clist=clist[(page-1)*rows : page*rows]

	print 'teacher course is %d' % len(new_clist)

	# add course info-(name and id)
	for c in new_clist:
		course={'course_id':c.id,'course_name':c.course_name}

		exercise=Exercise.objects.filter(exercise_course=c.id)
		judge=len(exercise.filter(exercisetype__id=1))
		single=len(exercise.filter(exercisetype__id=2))
		statement=len(exercise.filter(exercisetype__id=3))
		
		course['exercise_general']='单选题 %d 道 | 判断题 %d 道 | 陈述题 %d 道' %(judge,single,statement)
		lists.append(course)
		# waiting to add exercise general info
	d['rows']=lists
	return simplejson.dumps(d,ensure_ascii=False)


# return teacher's course info and exerciseinfo
def exerciseGeneralList(request,id):
	result={}
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		clist=Course.objects.filter(teacher__id=id).filter(course_ischecked=True).filter(course_status=True)
		result=__exerciseGeneralListJson(clist,page,rows)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
	return HttpResponse(simplejson.dumps(result),mimetype='application/json')


# return the exercise-list json
def __exerciseListJsonResult(elist,page,rows):
	d={}
	d['total']=len(elist)

	lists=simplejson.loads(serialize('json',elist[(page-1)*rows : page*rows]))
	for l in lists:
		# update coursetype info
		et=ExerciseType.objects.get(pk=int(l['fields']['exercisetype']))
		# remove `[` and `]`
		l['fields']['exercisetype']=simplejson.loads(serialize('json',[et])[1:-1])
	d['rows']=lists
	return simplejson.dumps(d,ensure_ascii=False)

# return exercise list
def exerciseList(request,id):
	result={}
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		elist=Exercise.objects.filter(exercise_course=id)
		result=__exerciseListJsonResult(elist,page,rows)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
	return HttpResponse(simplejson.dumps(result),mimetype='application/json')

# return the exercisetype array-json
@csrf_exempt
def exercisetypeArray(request):
	try:
		etlist=ExerciseType.objects.filter(exercise_status=True)
		lists=[]
		for l in etlist:
			et={'exercisetype_name':l.exercise_name,'id':l.id}
			lists.append(et)
		result=simplejson.dumps(lists,ensure_ascii=False)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
		return HttpResponse(simplejson.dumps(result),mimetype='application/json')

# add the exercise
@transaction.commit_on_success
def exerciseAdd(request,id):
	result={}
	try:

		exercisetype=ExerciseType.objects.get(pk=int(request.POST.get('exercisetype')))
		exerciseForm=ExerciseForm(request.POST)
		if exerciseForm.is_valid():
			exercise=exerciseForm.save(commit=False)
			
			exercise.exercisetype=exercisetype
			exercise.exercise_course=id

			exercise.save()
			result['status']='success'
			result['tip']='保存成功'
		else:
			result['status']='faliured'
			result['tip']='验证失败'
			result['error']=exerciseForm.errors

	except Exception,e:
		result['status']='failured'
		result['tip']='保存失败'
		result['error']=traceback.format_exc()

	finally:
		return HttpResponse(simplejson.dumps(result),mimetype='application/json')

# update the exercise
@transaction.commit_on_success
def exerciseUpdate(request,course_id,id):
	result={}
	try:
		
		exercise=Exercise.objects.get(pk=id)
		exerciseForm=ExerciseForm(request.POST,instance=exercise)
		if exerciseForm.is_valid():
			exercise=exerciseForm.save(commit=False)
			exercise.save()
			result['status']='success'
			result['tip']='保存成功'
		else:
			result['status']='faliured'
			result['tip']='验证失败'
			result['error']=exerciseForm.errors

	except Exception,e:
		result['status']='failured'
		result['tip']='保存失败'
		result['error']=traceback.format_exc()

	finally:
		return HttpResponse(simplejson.dumps(result),mimetype='application/json')


def __exercisePaperGeneralListJson(clist,page,rows):
	d={}
	lists=[]
	d['total']=len(clist)
	new_clist=clist[(page-1)*rows : page*rows]
	# add course info-(name and id)
	for c in new_clist:
		course={'course_id':c.id,'course_name':c.course_name}

		exercise_paper=ExercisePaper.objects.filter(course__id=c.id)

		course['exercisepaper_general']='共有 %d 套练习' %(len(exercise_paper))
		lists.append(course)
		# waiting to add exercise general info
	d['rows']=lists
	return simplejson.dumps(d,ensure_ascii=False)


# return teacher's course info and exercisepaperinfo
def exercisePaperGeneralList(request,id):
	result={}
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		clist=Course.objects.filter(teacher__id=id).filter(course_ischecked=True).filter(course_status=True)
		result=__exercisePaperGeneralListJson(clist,page,rows)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
	return HttpResponse(simplejson.dumps(result),mimetype='application/json')
# 
def __exercisePaperListJson(eplist,page,rows):
	d={}
	d['total']=len(eplist)
	new_eplist=simplejson.loads(serialize('json',eplist[(page-1)*rows : page*rows]))
	d['rows']=new_eplist
	return simplejson.dumps(d,ensure_ascii=False)

# exercisepaper list info
def exercisePaperList(request,id):
	result={}
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		eplist=ExercisePaper.objects.filter(course__id=id)
		result=__exercisePaperListJson(eplist,page,rows)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
	return HttpResponse(simplejson.dumps(result),mimetype='application/json')
# 
def __studentExercisePaperListJson(request,eplist,page,rows):
	d={}
	d['total']=len(eplist)
	new_eplist=simplejson.loads(serialize('json',eplist[(page-1)*rows : page*rows]))

	for ep in new_eplist:
		examList=Exam.objects.filter(student__id=request.session['user'].id).filter(exercisepaper__id=int(ep['pk']))
		ep['exercise_haveexamedtimes']=len(examList)
	d['rows']=new_eplist
	return simplejson.dumps(d,ensure_ascii=False)

# return student exercisepaper list
def studentExercisePaperList(request,id):
	result={}
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		eplist=ExercisePaper.objects.filter(course__id=id)
		result=__studentExercisePaperListJson(request,eplist,page,rows)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
	return HttpResponse(simplejson.dumps(result),mimetype='application/json')


# add exercise paper
@transaction.commit_on_success
def exercisePaperAdd(request,id):
	result={}
	try:
		exercisePaperForm=ExercisePaperForm(request.POST)
		course=Course.objects.get(pk=id)
		if exercisePaperForm.is_valid():
			exercisePaper=exercisePaperForm.save(commit=False)
			exercisePaper.course=course
			# save and publish
			if request.POST.get('publish')=='1':
				exercisePaper.exercise_ischecked=0

			exercisePaper.save()

			idset=request.POST.get('addedExerciseIdSet').split(',')[:-1]

			for exercise_id in idset:
				exercise=Exercise.objects.get(pk=int(exercise_id))
				ExercisePaperDetail(exercise=exercise,exercisepaper=exercisePaper).save()

			result['status']='success'
			result['tip']='保存成功'
		else:
			result['status']='faliured'
			result['tip']='验证失败'
			result['error']=exercisePaperForm.errors
	except Exception,e:
		result['status']='failured'
		result['tip']='保存失败'
		result['error']=traceback.format_exc()

	finally:
		return HttpResponse(simplejson.dumps(result),mimetype='application/json')

# update exercise paper
@transaction.commit_on_success
def exercisePaperUpdate(request,id,exercisepaper_id):
	result={}
	try:
		ep=ExercisePaper.objects.get(pk=exercisepaper_id)
		exercisePaperForm=ExercisePaperForm(request.POST,instance=ep)
		if exercisePaperForm.is_valid():
			exercisePaper=exercisePaperForm.save(commit=False)
			# save and publish
			if request.POST.get('publish')=='1':
				exercisePaper.exercise_ischecked=0
			exercisePaper.save()

			idset=request.POST.get('addedExerciseIdSet').split(',')[:-1]

			# must clear original binded exercises
			exercisePaper.exercisepaperdetails.clear()

			for exercise_id in idset:
				exercise=Exercise.objects.get(pk=int(exercise_id))
				ExercisePaperDetail(exercise=exercise,exercisepaper=exercisePaper).save()

			result['status']='success'
			result['tip']='保存成功'
		else:
			result['status']='faliured'
			result['tip']='验证失败'
			result['error']=exercisePaperForm.errors
	except Exception,e:
		result['status']='failured'
		result['tip']='保存失败'
		result['error']=traceback.format_exc()

	finally:
		return HttpResponse(simplejson.dumps(result),mimetype='application/json')


@transaction.commit_on_success
def exercisePaperDelete(request,id,exercisepaper_id):
	result={}
	try:
		exercisePaper=ExercisePaper.objects.get(pk=exercisepaper_id)
		# clear exercisepaperdetails
		exercisePaper.exercisepaperdetails.clear()
		exercisePaper.delete()

		result['status']='success'
		result['tip']='删除成功'
	except Exception,e:

		result['status']='faliured'
		result['tip']='删除失败'
		result['error']=traceback.format_exc()
	finally:
		return HttpResponse(simplejson.dumps(result),mimetype='application/json')

@transaction.commit_on_success
def exercisePaperPublish(request,id,exercisepaper_id):
	result={}
	try:
		exercisePaper=ExercisePaper.objects.get(pk=exercisepaper_id)
		exercisePaper.exercise_ischecked=0
		exercisePaper.save()
		result['status']='success'
		result['tip']='发布成功，等待审核'
	except Exception,e:

		result['status']='faliured'
		result['tip']='发布失败'
		result['error']=traceback.format_exc()
	finally:
		return HttpResponse(simplejson.dumps(result),mimetype='application/json')

# return exercisepaper's exercise 
def exercisePaperAddedExerciseList(request,exercisepaper_id):
	result={}
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		elist=ExercisePaper.objects.get(pk=exercisepaper_id).exercisepaperdetails.all()
		result=__exerciseListJsonResult(elist,page,rows)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
	return HttpResponse(simplejson.dumps(result),mimetype='application/json')

# initialize the exam
# default strategy is that exam a student can only test one times

def __initializeExam(request,exercisepaper):

	exam=Exam()
	exam.student=Student.objects.get(pk=request.session['user'].id)
	exam.exam_scores=0
	exam.exercisepaper=exercisepaper
	
	exam.exam_status=True

	exam.exam_markingstatus=False
	exam.exam_ispassed=False
	exam.save()

	return exam

@transaction.commit_on_success
def studentExam(request,object_id):
	try:
		exercisepaper=ExercisePaper.objects.get(pk=object_id)
		exam=__initializeExam(request,exercisepaper)
	except Exception,e:
		return render_to_response('500.html',context_instance=RequestContext(request))
	finally:
		return render_to_response('exam/exam.html',{'exercisepaper':exercisepaper,'exam':exam},context_instance=RequestContext(request))

# resolve the string answers from client
# answers data format:
# 	|<- judge  ->||<-single->||<-  statement  ->|
#  `{1:A,2:B,3:A,}#{8:A,9:C,}#{10:xxxxxxxxxxxx,}#`
# 
# null data format:
# 	`judge:{}#single:{}#statement:{}#`

def __resloveAnswer(answers):
	array=answers.split('#')
	judge_answer_array=[]
	single_answer_array=[]
	statement_answer_array=[]
	if array[0].strip('{}')!='':
		judge_answer_array=array[0].strip('{}').split(',')[:-1]
		print judge_answer_array
	if array[1].strip('{}')!='':
		single_answer_array=array[1].strip('{}').split(',')[:-1]
		print single_answer_array
	if array[2].strip('{}')!='':
		statement_answer_array=array[2].strip('{}').split(',')[:-1]
		print statement_answer_array

	result={}
	result['judge']=judge_answer_array
	result['single']=single_answer_array
	result['statement']=statement_answer_array
	return result

# update single or judge answer
def __updateJudgeOrSingle(item,exam):
	ed=ExamDetail()
	ed.exam=exam
	ed.exercise=Exercise.objects.get(pk=int(item[0]))
	ed.examdetail_answeritem=item[1]
	if item[1]==ed.exercise.exercise_correctitem:
		ed.examdetail_iscorrect=True
		ed.examdetail_answerscore=ed.exercise.exercisetype.exercise_score
	else:
		ed.examdetail_iscorrect=False
		ed.examdetail_answerscore=0
	ed.save()
# update statement
def __updateStatement(item,exam):
	ed=ExamDetail()
	ed.exam=exam
	ed.exercise=Exercise.objects.get(pk=int(item[0]))
	ed.examdetail_answercontent=item[1]
	ed.save()

# update the student exam answer 
def __updateAnswer(array,exam):

	# indicate tha student can directly view scores
	flag=True

	# update judge answer
	if array['single']:
		for s in array['single']:
			item=s.split(':')
			__updateJudgeOrSingle(item,exam)
		print 'judge success'
	if array['judge']:
		for s in array['judge']:
			item=s.split(':')
			__updateJudgeOrSingle(item,exam)
		print 'single success'
	if array['statement']:
		flag=False
		for s in array['statement']:
			item=s.split(':')
			__updateStatement(item,exam)
		print 'statement success'

	return flag
# 
def __examScores(exam):
	edList=ExamDetail.objects.filter(exam=exam)
	sum=0
	for ed in edList:
		sum += ed.examdetail_answerscore
	return sum

# student online exam finish
@transaction.commit_manually
def studentExamFinish(request,id):
	try:
		exam=Exam.objects.get(pk=int(request.POST.get('exam')))
		flag=__updateAnswer(__resloveAnswer(request.POST.get('answers')),exam)
		# exercisepaper only have objective exercises
		if flag:
			exam.exam_markingstatus=True
			exam.exam_scores=__examScores(exam)
			if exam.exam_scores >= exam.exercisepaper.exercisepaper_passedscore:
				exam.exam_ispassed=True
			else:
				exam.exam_ispassed=False
			exam.save()

		transaction.commit()
		if not flag:
			return render_to_response('exam/exam_result.html',context_instance=RequestContext(request))
		else:
			return render_to_response('exam/exercisepaper_result.html',
			{'exercisepaper':exam.exercisepaper,'exam':exam},context_instance=RequestContext(request))
	except Exception,e:
		transaction.rollback()
		return render_to_response('500.html',{'stackinfo':traceback.format_exc()},context_instance=RequestContext(request))


# student online exam result
def studentExamResult(request,id):
	try:
		exam=Exam.objects.get(pk=id)
		exercisepaper=exam.exercisepaper
	except Exception,e:
		return render_to_response('500.html',{'stackinfo':traceback.format_exc()},context_instance=RequestContext(request))
	else:
		return render_to_response('exam/exercisepaper_result.html',
			{'exercisepaper':exercisepaper,'exam':exam},context_instance=RequestContext(request))


# 
def __studentGeneralExamListJson(request,examList,page,rows):
	d={}
	eplist=[]
	for exam in examList:
		if exam.exercisepaper not in eplist:
			eplist.append(exam.exercisepaper)

	d['total']=len(eplist)
	new_eplist=simplejson.loads(serialize('json',eplist[(page-1)*rows : page*rows]))

	for ep in new_eplist:
		examList=Exam.objects.filter(student__id=request.session['user'].id,exercisepaper__id=int(ep['pk']))
		ep['examed_times']=examList.count()
		ep['exam_hightestscore']=examList.aggregate(exam_hightestscore=Max('exam_scores'))['exam_hightestscore']
		ep['exam_lowestscore']=examList.aggregate(exam_lowestscore=Min('exam_scores'))['exam_lowestscore']

		# add group name
		ep['course']=Course.objects.get(pk=int(ep['fields']['course'])).course_name

	d['rows']=new_eplist
	return simplejson.dumps(d,ensure_ascii=False)


# return student's general participated exam list info
def studentGeneralExamList(request):
	result={}
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))
		examList=Exam.objects.filter(student__id=request.session['user'].id)

		result=__studentGeneralExamListJson(request,examList,page,rows)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
	return HttpResponse(simplejson.dumps(result),mimetype='application/json')

# 
def __studentDetailExamListJson(examList,page,rows):
	d={}
	d['total']=len(examList)
	new_examList=simplejson.loads(serialize('json',examList[(page-1)*rows : page*rows]))
	for exam in new_examList:
		e=Exam.objects.get(pk=int(exam['pk']))
		exam['exam_timelength']=(e.exam_endtime-e.exam_starttime).total_seconds()
	d['rows']=new_examList
	return simplejson.dumps(d,ensure_ascii=False)


# return student's detail participated exam list info
def studentDetailExamList(request,exercisepaper_id):
	result={}
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))
		examList=Exam.objects.filter(student__id=request.session['user'].id,exercisepaper__id=exercisepaper_id)

		result=__studentDetailExamListJson(examList,page,rows)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
	return HttpResponse(simplejson.dumps(result),mimetype='application/json')


def __teacherExamVerifyListJson(examList,page,rows):
	d={}
	d['total']=len(examList)
	new_examList=simplejson.loads(serialize('json',examList[(page-1)*rows : page*rows]))
	for exam in new_examList:
		student=Student.objects.get(pk=int(exam['fields']['student']))
		exam['fields']['student']=simplejson.loads(serialize('json',[student])[1:-1])
		exercisepaper=ExercisePaper.objects.get(pk=int(exam['fields']['exercisepaper']))
		exam['fields']['exercisepaper']=simplejson.loads(serialize('json',[exercisepaper])[1:-1])

	d['rows']=new_examList
	return simplejson.dumps(d,ensure_ascii=False)


# need teacher's id
def teacherExamVerifyList(request):
	result={}
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))
		examList=Exam.objects.filter(exercisepaper__course__teacher__id=request.session['user'].id,exam_markingstatus=False)
		result=__teacherExamVerifyListJson(examList,page,rows)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
	return HttpResponse(simplejson.dumps(result),mimetype='application/json')

def teacherExamVerifyDetail(request,id):
	try:
		exam=Exam.objects.get(pk=id)
		exercisepaper=exam.exercisepaper
	except Exception,e:
		return render_to_response('500.html',{'stackinfo':traceback.format_exc()},context_instance=RequestContext(request))
	else:
		return render_to_response('exam/teacher_exam_verifydetail.html',
			{'exercisepaper':exercisepaper,'exam':exam},context_instance=RequestContext(request))


# update examdetail and exam status
def __teacherExamVerify(verifys,exam,request):

	for v in verifys:
		array=v.split(':')
		exercise=Exercise.objects.get(pk=int(array[0]))
		ed=ExamDetail.objects.filter(exercise=exercise,exam=exam)
		# this exercise answer is null
		if not ed:
			continue 
		ed[0].examdetail_answerscore=int(array[1])
		if ed[0].examdetail_answerscore < ed[0].exercise.exercisetype.exercise_score:
			ed[0].examdetail_iscorrect=False
		else:
			ed[0].examdetail_iscorrect=True

		ed[0].save()

	# after finish ,should update the exam
	exam.exam_markingstatus=True
	exam.exam_scores= __examScores(exam)
	if exam.exam_scores >= exam.exercisepaper.exercisepaper_passedscore:
		exam.exam_ispassed=True
	else:
		exam.exam_ispassed=False
	exam.save()

	# send message to student
	m=Message(message_type=settings.EXAMMSG,message_ishandlered=False,
		message_senderid=request.session['user'].id,message_sendertype=request.session['user'].usertype)
	m.message_content=exam.exercisepaper.exercisepaper_name+'-已审阅完成'
	m.message_receiverid=exam.student.id
	m.message_receivertype=0
	m.save()


# save the verifys
@transaction.commit_manually
@csrf_exempt
def teacherExamVerifysSave(request,id):
	result={}
	try:
		exam=Exam.objects.get(pk=id)
		verifys=request.POST.get('verifys').split(',')[:-1]
		__teacherExamVerify(verifys,exam,request)

		transaction.commit()

		result['status']='success'
		result['tip']='审阅完成'
	except Exception,e:
		transaction.rollback()
		result['status']='faliured'
		result['tip']='审阅失败'
		result['error']=traceback.format_exc()
	finally:
		return HttpResponse(simplejson.dumps(result),mimetype='application/json')

# return administrator waiting to check exercisepaper list
def waitingAdminCheckExercisepaperList(request):
	result={}
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		eplist=ExercisePaper.objects.exclude(exercise_ischecked=None)
		result=__waitingAdminCheckExercisepaperListJson(request,eplist,page,rows)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
	return HttpResponse(simplejson.dumps(result),mimetype='application/json')


# 
def __waitingAdminCheckExercisepaperListJson(request,eplist,page,rows):
	d={}
	d['total']=len(eplist)
	new_eplist=simplejson.loads(serialize('json',eplist[(page-1)*rows : page*rows]))

	for ep in new_eplist:
		ep['course']=Course.objects.get(pk=int(ep['fields']['course'])).course_name

	d['rows']=new_eplist
	return simplejson.dumps(d,ensure_ascii=False)

def checkExercisePaper(request,id):
	result={}
	try:
		ep=ExercisePaper.objects.get(pk=id)
		ep.exercise_ischecked=True
		ep.save()
		result['status']='success'
		result['tip']='审核成功'
	except Exception,e:
		transaction.rollback()
		result['status']='faliured'
		result['tip']='审核失败'
		result['error']=traceback.format_exc()
	finally:
		return HttpResponse(simplejson.dumps(result),mimetype='application/json')





		














