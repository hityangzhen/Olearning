from django.conf.urls import patterns, url
from django.views.generic.simple import direct_to_template
from django.views.generic import list_detail
from .models import Course,CourseNote

# prefix is `course/`
urlpatterns = patterns('course.views',
	url(r'^$',direct_to_template,{'template':'course/course.html'}),
	url(r'^list/$','courseList'),
	url(r'^list/bycoursetype/(?P<coursetype_id>\d+)/$','courseListByCourseType'),
	url(r'^detail/(?P<id>\d+)/$','courseShowDetail'),
	url(r'^(?P<id>\d+)/$','courseById'),
	url(r'^canpublish/(?P<id>\d+)/$','canPublish'),
	url(r'^publish/(?P<id>\d+)/$','coursePublish'),
)

# for teacher
urlpatterns += patterns('course.views',
	url(r'^teacher/$',direct_to_template,{'template':'course/teacher_course.html'}),
	url(r'^teacher/list/(?P<id>\d+)/$','courseListByTeacher'),
	url(r'^update/(?P<id>\d+)/$','courseUpdate'),
	url(r'^add/',direct_to_template,{'template':'course/courseadd.html'}),
	url(r'^addinfo/$','courseSave'),
	url(r'^delete/(?P<id>\d+)/$','courseDelete'),
)
# for resource
urlpatterns += patterns('course.views',
	url(r'^resource/(?P<id>\d+)/$','courseResourceList'),
	url(r'^resource/list/(?P<id>\d+)/','resourceList'),
	url(r'^resource/add/$','resourceAdd'),
	url(r'^resource/update/$','resourceUpdate'),
	url(r'^resource/delete/(?P<id>\d+)/$','resourceDelete'),
	url(r'^student/show_resource/(?P<id>\d+)/$',direct_to_template,{'template':'course/student_resource.html'}),
	url(r'^student/resource/(?P<id>\d+)/list/$','studentResourceList'),
	# id-repensent resource's id
	url(r'^student/resource/(?P<id>\d+)/download/$','resourceDownload'),
	url(r'^resource/viewordownload/$','resourceViewOrDownload'),
)

course_check_detail_info={
	'queryset':Course.objects.all(),
    'template_name':'course/course_check_detail.html',
    'template_object_name':'course',
}

# for course check
urlpatterns += patterns('course.views',
	url(r'^showuncheck/$',direct_to_template,{'template':'course/course_check.html'}),
	url(r'^uncheck/$','uncheckedCourseList'),
	url(r'^showcheckdetail/(?P<object_id>\d+)/$',list_detail.object_detail,course_check_detail_info),
	url(r'^checked/(?P<id>\d+)/$','checkCourse'),
)

#for course's notice
urlpatterns += patterns('course.views',
	url(r'^(?P<id>\d+)/notice/$',direct_to_template,{'template':'course/notice.html'}),
	url(r'^(?P<id>\d+)/generalnotice/$',direct_to_template,{'template':'course/student_notice.html'}),
	url(r'^(?P<id>\d+)/generalnotice/list/$','noticeList'),
	url(r'^(?P<id>\d+)/notice/list/$','noticeList'),
	url(r'^(?P<id>\d+)/notice/add/$','noticeSave'),
	url(r'^(?P<id>\d+)/notice/update/$','noticeUpdate'),
	url(r'^(?P<id>\d+)/notice/delete/$','noticeDelete'),
)

#for course's note 
note_info={
	'queryset':CourseNote.objects.all(),
    'template_name':'course/notedetail.html',
    'template_object_name':'note',
}

urlpatterns += patterns('course.views',
	# course's id
	url(r'^note/$','noteList'),
	url(r'^note/(?P<object_id>\d+)/$',list_detail.object_detail,note_info),
	url(r'^note/(?P<object_id>\d+)/edit/$',list_detail.object_detail,note_info),
	url(r'^note/edit/$',direct_to_template,{'template':'course/notedetail.html'}),
	url(r'^note/save/(?P<id>\d+)/$','noteSave'),
)

#for course's comment
urlpatterns += patterns('course.views',
	url(r'^comment/(?P<id>\d+)/$','courseComments'),
	url(r'^comment/(?P<id>\d+)/save/$','commentSave'),
	url(r'^comment/(?P<courseid>\d+)/delete/(?P<id>\d+)/$','commentDelete'),
)
