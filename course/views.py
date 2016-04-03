# -*- coding: utf-8 -*-
from admin.models import *
from course.models import Course,Resource,CourseNotice,CourseNote,CourseComment
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.db import transaction
import traceback
from django.core.serializers import serialize
from course.forms import *
from django.shortcuts import render_to_response,redirect,render
from django.template import RequestContext
from django.conf import settings
from sae.storage import Bucket

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


# return the course list-json
@csrf_exempt
def courseList(request):
	# param:page | rows
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		ctlist=Course.objects.all().exclude(course_ischecked=None)
		result=listJsonResult(ctlist,page,rows)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
		return HttpResponse(simplejson.dumps(result),mimetype='application/json')

@csrf_exempt
def courseListByCourseType(request,coursetype_id):
	# param:page | rows
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		ctlist=Course.objects.filter(coursetype__id=coursetype_id,course_ischecked=True,course_status=True)
		result=listJsonResult(ctlist,page,rows)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
		return HttpResponse(simplejson.dumps(result),mimetype='application/json')


# include foreign key teacher and coursetype
def listJsonResult(clist,page,rows):
	d={}
	d['total']=len(clist)

	lists=simplejson.loads(serialize('json',clist[(page-1)*rows : page*rows]))

	for l in lists:
		# update coursetype info
		ct=CourseType.objects.get(pk=int(l['fields']['coursetype']))
		# remove `[` and `]`
		l['fields']['coursetype']=simplejson.loads(serialize('json',[ct])[1:-1])
		# update teacher info
		tc=Teacher.objects.get(pk=int(l['fields']['teacher']))
		l['fields']['teacher']=simplejson.loads(serialize('json',[tc])[1:-1])
	d['rows']=lists
	return simplejson.dumps(d,ensure_ascii=False)

# save the course info
@transaction.commit_manually
def courseSave(request):
	result={}
	try:
		courseForm=CourseForm(request.POST,request.FILES)
		if courseForm.is_valid() :
			course=courseForm.save(commit=False)
			course.coursetype=CourseType.objects.get(pk=int(request.POST.get('coursetype')))
			course.teacher=Teacher.objects.get(pk=request.session['user'].id)
			# add 2014-4-7
			course.course_status=True
			# end add

			# add 2014-4-22
			course.course_lessonnum=0
			# end add			

			course.save()
			result['status']='success'
			result['tip']='保存成功'
			result['course_name']=course.course_name
			result['id']=course.id
			transaction.commit()
		else:
			result['status']='faliured'
			result['tip']='验证失败'
			result['error']=courseForm.errors
	except Exception,e:
		transaction.rollback()
		result['status']='failured'
		result['tip']='添加失败'
		result['error']=traceback.format_exc()
		
	else:
		pass
	finally:
		return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')

# show course's courseware
@csrf_exempt
def courseResourceList(request,id):
	course=Course.objects.get(pk=id)
	return render(request,'course/courseadddetail.html',{'course':course})

@csrf_exempt
@transaction.commit_manually
def courseDelete(request,id):
	result={}
	try:
		Course.objects.get(pk=id).delete()
		result['status']='success'
		result['tip']='删除成功'
		transaction.commit()
	except Exception,e:
		transaction.rollback()
		result['status']='faliured'
		result['tip']='删除失败'
		result['error']=traceback.format_exc()

	return HttpResponse(simplejson.dumps(result),mimetype='application/json')

# --------------------------------------------update 2014-3-27----------------------------------------------------
# save the resource
@transaction.commit_on_success
def resourceAdd(request):
	result={}
	try:
		course=Course.objects.all().get(pk=int(request.POST.get('course')))
		# course has published,couldn't add courseware
		if course.course_ischecked!=None and request.POST.get('resource_iscourseware')=='True':
			result['status']='failured'
			result['tip']='课程已发布，不能添加课件，当前只限于添加资料'
		else:
			resourceForm=ResourceForm(request.POST,request.FILES)
			if resourceForm.is_valid() :
				
				courseware=resourceForm.save(commit=False)
				# if sesssion is enabled ,need to update
				courseware.resource_uploader=request.session['user'].realname
				# 
				courseware.course=course
				courseware.resource_viewtimes=0
				courseware.resource_downloadtimes=0
				courseware.resource_status=True
				
				courseware.save()
				# 2014-4-22 added
				if courseware.resource_iscourseware:
					course.course_lessonnum += courseware.resource_standardtime
					course.save()
				# end added

				result['status']='success'
				result['tip']='保存成功'
			else:
				result['status']='faliured'
				result['tip']='验证失败'
				result['error']=resourceForm.errors
	except Exception,e:
		result['status']='failured'
		result['tip']='添加失败'
		result['error']=traceback.format_exc()
	else:
		pass
	finally:
		return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')

# --------------------------------------------add 2014-3-26----------------------------------------------------
# show the course detail info
def courseShowDetail(request,id):
	try:
		course=Course.objects.get(pk=id)
	except Course.DoesNotExist:
		raise Exception
	return render_to_response('course/coursedetail.html', {'course':course},context_instance=RequestContext(request))

# course list owned by teacher
@csrf_exempt
def courseListByTeacher(request,id):
	# param:page | rows | id
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))
		ctlist=Course.objects.all().filter(teacher__id=id)
		result=listJsonResult(ctlist,page,rows)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
	return HttpResponse(simplejson.dumps(result),mimetype='application/json')

# --------------------------------------------add 2014-3-27----------------------------------------------------	
# show resource list
@csrf_exempt
def resourceList(request,id):
	# param:page | rows
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		rlist=Resource.objects.filter(course__id=id)
		result=listJsonResult2(rlist,page,rows)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
		return HttpResponse(simplejson.dumps(result),mimetype='application/json')

@transaction.commit_manually
def resourceUpdate(request):
	result={}
	try:
		resource=Resource.objects.get(pk=int(request.POST.get('resource_id')))

		
		if resource.resource_iscourseware:
			course=resource.course
			course.course_lessonnum -= resource.resource_standardtime

		# delete the orginal files
		if request.FILES and resource.resource_path:
			resource.resource_path.storage.delete(resource.resource_path.name)
		resource.resource_candownload=True
		resource.resource_status=True
		resourceForm=ResourceForm(request.POST,request.FILES,instance=resource)

		if resourceForm.is_valid() :
			resourceForm.save()
			if resource.resource_iscourseware:
				course.course_lessonnum += int(request.POST.get('resource_standardtime'))
				course.save()

			result['status']='success'
			result['tip']='保存成功'
			transaction.commit()
		else:
			result['status']='faliured'
			result['tip']='验证失败'
			result['error']=resourceForm.errors
	except Exception,e:
		transaction.rollback()
		result['status']='failured'
		result['tip']='添加失败'
		result['error']=traceback.format_exc()
		
	else:
		pass
	finally:
		return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')


# include foreign key course and coursetype
def listJsonResult2(rlist,page,rows):
	d={}
	d['total']=len(rlist)
	lists=simplejson.loads(serialize('json',rlist[(page-1)*rows : page*rows]))

	for l in lists:
		# update course info
		c=Course.objects.get(pk=int(l['fields']['course']))
		# remove `[` and `]`
		l['fields']['course']=simplejson.loads(serialize('json',[c])[1:-1])
	d['rows']=lists
	return simplejson.dumps(d,ensure_ascii=False)

# return course info
def courseById(request,id):
	result={}
	try:
		course=Course.objects.get(pk=id)
		result=course.toSIMPLEDICT()
	except Exception,e:
		result['error']=traceback.format_exc()
	return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')

# update course info
@transaction.commit_manually
def courseUpdate(request,id):
	result={}
	try:
		course=Course.objects.get(pk=id)
		# delete the orginal files
		if request.FILES and course.course_icon:
			course.course_icon.storage.delete(course.course_icon.name)
		courseForm=CourseForm(request.POST,request.FILES,instance=course)

		if courseForm.is_valid() :
			courseForm.save()
			result['status']='success'
			result['tip']='保存成功'
			transaction.commit()
		else:
			result['status']='faliured'
			result['tip']='验证失败'
			result['error']=courseForm.errors
	except Exception,e:
		transaction.rollback()
		result['status']='failured'
		result['tip']='添加失败'
		result['error']=traceback.format_exc()
	else:
		pass
	finally:
		return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')

@csrf_exempt
@transaction.commit_manually
def resourceDelete(request,id):
	result={}
	try:
		resource=Resource.objects.get(pk=id)
		resource.delete()

		if resource.resource_iscourseware:
			course=resource.course
			course.course_lessonnum -= resource.resource_standardtime
			course.save()
			
		result['status']='success'
		result['tip']='删除成功'
		transaction.commit()
	except Exception,e:
		transaction.rollback()
		result['status']='faliured'
		result['tip']='删除失败'
		result['error']=traceback.format_exc()
		
	return HttpResponse(simplejson.dumps(result),mimetype='application/json')

# --------------------------------------------add 2014-4-6----------------------------------------------------
# return the group of unchecked course list json info
def __uncheckedCourseListJsonResult(clist,page,rows):
	d={}
	d['total']=len(clist)

	lists=simplejson.loads(serialize('json',clist[(page-1)*rows : page*rows]))

	for l in lists:
		# update coursetype info
		ct=CourseType.objects.get(pk=int(l['fields']['coursetype']))
		# remove `[` and `]`
		l['fields']['coursetype']=simplejson.loads(serialize('json',[ct])[1:-1])
		# update teacher info
		tc=Teacher.objects.get(pk=int(l['fields']['teacher']))
		l['fields']['teacher']=simplejson.loads(serialize('json',[tc])[1:-1])
		# store teacher's groupname(id+'#'+teacher_realname)
		# unsupport long `+` str
		l['model']=str(tc.id)+'#'+tc.teacher_realname

	d['rows']=lists
	return simplejson.dumps(d,ensure_ascii=False)

@csrf_exempt
def uncheckedCourseList(request):
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		clist=Course.objects.filter(course_ischecked=False)
		result=__uncheckedCourseListJsonResult(clist,page,rows)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
		return HttpResponse(simplejson.dumps(result),mimetype='application/json')

# --------------------------------------------add 2014-4-7----------------------------------------------------
@csrf_exempt
@transaction.commit_on_success
def checkCourse(request,id):
	result={}
	try:
		# course_ischecked=bool(request.POST.get('course_ischecked'))
		course_ischecked=True
		course_checkedReply=request.POST.get('course_checkedReply')
		course=Course.objects.get(pk=id)
		course.course_ischecked=course_ischecked
		course.course_checkedReply=course_checkedReply
		# unpassed 
		if course_checkedReply.split('##')[0]=='0':
			course.course_status=False
			
		course.save()
		result['status']='success'
		result['tip']='审核成功'
	except Exception,e:
		result['status']='faliured'
		result['tip']='审核失败'
		result['error']=traceback.format_exc()
		
	return HttpResponse(simplejson.dumps(result),mimetype='application/json')

# whether the course having at least one courseware
@csrf_exempt
def canPublish(request,id):
	result={}
	try:
		course=Course.objects.get(pk=id)
		resource=Resource.objects.filter(course=course).filter(resource_iscourseware=True)
		# course is unpublish and have courseware
		if course.course_ischecked==None and resource:
			result['status']='success'
			result['canpublish']='yes'
			result['tip']='能够发布'
		elif course.course_ischecked==None and (not resource):
			result['status']='failured'
			result['canpublish']='no'
			result['tip']='请添加至少一个课件'
		else:
			result['status']='failured'
			result['canpublish']='no'
			result['tip']='已发布，不能重复发布'

	except Exception,e:
		result['status']='failured'
		result['canpublish']='no'
		result['error']=traceback.format_exc()

	return HttpResponse(simplejson.dumps(result),mimetype='application/json')

# publish course
def coursePublish(request,id):
	result={}
	try:
		course=Course.objects.get(pk=id)
		course.course_ischecked=False
		result['status']='success'
		result['tip']='发布成功，等待审核'
		course.save()

	except Exception,e:
		result['status']='failured'
		result['tip']='发布失败'
		result['error']=traceback.format_exc()

	return HttpResponse(simplejson.dumps(result),mimetype='application/json')


def __noticeListJsonResult(nlist,page,rows):
	d={}
	d['total']=len(nlist)
	lists=simplejson.loads(serialize('json',nlist[(page-1)*rows : page*rows]))
	d['rows']=lists
	return simplejson.dumps(d,ensure_ascii=False)


@csrf_exempt
def noticeList(request,id):
	result={}
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))
		nlist=CourseNotice.objects.filter(course__id=id)
		result=__noticeListJsonResult(nlist,page,rows)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
		return HttpResponse(simplejson.dumps(result),mimetype='application/json')

# --------------------------------------------add 2014-4-8----------------------------------------------------
@transaction.commit_on_success
def noticeSave(request,id):
	result={}
	try:
		courseNoticeForm=CourseNoticeForm(request.POST)
		notice=courseNoticeForm.save(commit=False)
		course=Course.objects.get(pk=id)
		notice.course=course
		notice.teacher=course.teacher.teacher_username
		notice.save()

		# send message to course's students
		sList=Student.objects.filter(student_positionid=course.coursetype.coursetype_positionid)

		for s in sList:
			m=Message(message_type=settings.COURSEMSG,message_ishandlered=False,
			message_receiverid=s.id,message_receivertype=0,
			message_senderid=request.session['user'].id,message_sendertype=request.session['user'].usertype)
		
			m.message_content='您的课程-'+course.course_name+'有新的公告'
			m.save()

		result['status']='success'
		result['tip']='保存成功'

	except Exception,e:
		result['status']='failured'
		result['tip']='保存失败'
		result['error']=traceback.format_exc()
	return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')

@transaction.commit_on_success
def noticeUpdate(request,id):
	result={}
	try:
		instance=CourseNotice.objects.get(pk=int(request.POST.get('id')))
		courseNoticeForm=CourseNoticeForm(request.POST,instance=instance)
		courseNoticeForm.save()
		result['status']='success'
		result['tip']='保存成功'

	except Exception,e:
		result['status']='failured'
		result['tip']='保存失败'
		result['error']=traceback.format_exc()
	return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')

@transaction.commit_on_success
	
def noticeDelete(request,id):
	result={}
	idset=request.POST.get('id').split(',')[:-1]
	try:
		for id in idset:
			CourseNotice.objects.get(pk=int(id)).delete()
		result['status']='success'
		result['tip']='删除成功'
	except Exception,e:
		result['status']='failured'
		result['tip']='删除失败'
		result['error']=traceback.format_exc()
	finally:
		return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')

# return note list info
def noteList(request):
	try:
		student_id=int(request.GET.get('studentid','0'))
		course_id=int(request.GET.get('courseid','0'))

		if student_id:
			noteList=CourseNote.objects.filter(student__id=student_id)
		else:
			noteList=CourseNote.objects.all()

		if course_id:
			noteList=noteList.filter(course__id=course_id)


	except Exception,e:
		
		return render_to_response('500.html', {'stackinfo':traceback.format_exc()},
    		context_instance=RequestContext(request))
	finally:
		return render_to_response('course/note.html',{'note_list':noteList},context_instance=RequestContext(request))

# save the note
@transaction.commit_on_success
def noteSave(request,id):
	result={}
	try:
		# update note
		if int(id)>0:
			note=CourseNote.objects.get(pk=id)
			courseNoteForm=CourseNoteForm(request.POST,instance=note)
			if courseNoteForm.is_valid():
				note=courseNoteForm.save(commit=False)
			else:
				raise Exception(courseNoteForm.errors)
		# add note
		else:
			courseNoteForm=CourseNoteForm(request.POST)

			if courseNoteForm.is_valid():
				note=courseNoteForm.save(commit=False)
			else:
				raise Exception(courseNoteForm.errors)

			student_id=int(request.GET.get('studentid','0'))
			course_id=int(request.GET.get('courseid','0'))

			student=Student.objects.get(pk=student_id)
			course=Course.objects.get(pk=course_id)

			note.student=student
			note.course=course
		
		note.coursenote_viewtimes += 1
		note.coursetype_ispublic=False
		note.coursetype_status=True

		note.save()

		result['status']='success'
		result['tip']='保存成功'

	except Exception,e:
		result['status']='failured'
		result['tip']='保存失败'
		result['error']=traceback.format_exc()
	return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')


# course's comments
def courseComments(request,id):
	try:
		cList=CourseComment.objects.filter(course__id=id).filter(coursecomment_status=True)
	except Exception,e:
		cList=None
	finally:
		return render_to_response('course/comment.html',{'comment_list':cList},context_instance=RequestContext(request))

@transaction.commit_on_success
def commentSave(request,id):
	result={}
	try:
		if request.POST.get('commentid')=='0':
			courseCommentForm=CourseCommentForm(request.POST)
		else:
			cc=CourseComment.objects.get(pk=int(request.POST.get('commentid')))
			courseCommentForm=CourseCommentForm(request.POST,instance=cc)
		if courseCommentForm.is_valid():
			courseComment=courseCommentForm.save(commit=False)
			courseComment.coursecomment_status=True
			courseComment.course=Course.objects.get(pk=id)
			courseComment.save()
			result['status']='success'
			result['tip']='保存成功'

		else:
			result['status']='faliured'
			result['tip']='验证失败'
			result['error']=courseCommentForm.errors

	except Exception,e:
		result['status']='failured'
		result['tip']='保存失败'
		result['error']=traceback.format_exc()
	return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')


@transaction.commit_on_success
def commentDelete(request,courseid,id):
	result={}
	try:
		CourseComment.objects.get(pk=id).delete()
		result['status']='success'
		result['tip']='删除成功'
	except Exception,e:
		result['status']='failured'
		result['tip']='删除失败'
		result['error']=traceback.format_exc()
	finally:
		return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')

# return the resources student can access
def studentResourceList(request,id):
	# param:page | rows
	try:
		rows=int(request.GET.get('rows',5))
		page=int(request.GET.get('page',1))

		rlist=Resource.objects.filter(course__id=id,resource_iscourseware=False,resource_status=True)
		result=listJsonResult2(rlist,page,rows)
		return HttpResponse(result, mimetype='application/json')
	except Exception,e:
		result={"total":0,"rows":[],"error":traceback.format_exc()}
		return HttpResponse(simplejson.dumps(result),mimetype='application/json')

def __readLocalFile(fn, buf_size=262144):
	f = open(fn, "rb")
	while True:
		c = f.read(buf_size)
		if c:
			yield c
		else:
			break
	f.close()

def __readStorageFile(fn):
	bucket = Bucket('resources')
	chunks = bucket.get_object_contents(fn,chunk_size=1024*1024)
	return chunks

# resource download
def resourceDownload(request,id):
	try:
		resource=Resource.objects.get(pk=id)

		if settings.DEBUG:
			response=HttpResponse(__readLocalFile(settings.MEDIA_ROOT+resource.resource_path.name),mimetype='application/octet-stream')
		else:
			response=HttpResponse(__readStorageFile(resource.resource_path.name),mimetype='application/octet-stream')			
		response['Content-Disposition'] = 'attachment; filename=%s' %resource.resource_path.name.strip('/')
		return response

	except Exception,e:
		return render_to_response('500.html',{'stackinfo':traceback.format_exc()},context_instance=RequestContext(request))

# 
@transaction.commit_on_success
def resourceViewOrDownload(request):
	result={}
	try:
		resource=Resource.objects.get(pk=int(request.GET.get('id')))
		viewordownload=request.GET.get('type')
		if viewordownload=='viewtime':
			resource.resource_viewtimes += 1
		else:
			resource.resource_downloadtimes += 1

		resource.save()
		
		result['status']='success'
		result['tip']='更新成功'
	except Exception,e:
		result['status']='failured'
		result['tip']='更新失败'
		result['error']=traceback.format_exc()
	finally:
		return HttpResponse(simplejson.dumps(result,ensure_ascii=False),mimetype='application/json')



# def resourceDownloadTest(request):
# 	try:
# 		response=HttpResponse(__readStorageFile('resource/工程投资项目管理系统文档.doc'),mimetype='application/octet-stream')			
# 		response['Content-Disposition'] = 'attachment; filename=%s' %('工程投资项目管理系统文档.doc')
# 		return response

# 	except Exception,e:
# 		return render_to_response('500.html',{'stackinfo':traceback.format_exc()},context_instance=RequestContext(request))


















































