from django.conf.urls import patterns, url
from django.views.generic.simple import direct_to_template
from django.views.generic import list_detail
from admin.models import Student,Teacher,Task

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

# url prefix `is admin/`
urlpatterns = patterns('admin.views',
    # Examples:
    url(r'^$', direct_to_template,{'template':'main/admin-main.html'}),
    # url(r'^olearning/', include('olearning.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

# coursetype mod url
urlpatterns += patterns('admin.views',
	url(r'^coursetype/$',direct_to_template,{'template':'admin/coursetype.html'}),
    url(r'^coursetype/list','coursetypeList'),
    url(r'^coursetype/array','coursetypeArray'),
    url(r'^coursetype/add','coursetypeAdd'),
    url(r'^coursetype/update','coursetypeUpdate'),
    url(r'^coursetype/(?P<id>\d+)/$','coursetypeFindById'),
    url(r'^coursetype/delete','coursetypeDelete'),
    url(r'^userimport/$',direct_to_template,{'template':'admin/userimport.html'}),
    url(r'^userimport/(?P<tp>[01])/$','userImport'),
)

# 2014-3-31 add
# student mod url
student_detail_info={
    'queryset':Student.objects.all(),
    'template_name':'admin/student_detail.html',
    'template_object_name':'student',
}
student_edit_info={
    'queryset':Student.objects.all(),
    'template_name':'admin/student_edit.html',
    'template_object_name':'student',
}
urlpatterns += patterns('admin.views',
    url(r'^student/$',direct_to_template,{'template':'admin/student.html'}),
    url(r'^student/list/$','studentList'),
    url(r'^student/(?P<object_id>\d+)/$',list_detail.object_detail,student_detail_info),
    url(r'^student/showadd/$',direct_to_template,{'template':'admin/student_edit.html'}),
    url(r'^student/add/$','studentAdd'),
    url(r'^student/delete/$','studentDelete'),
    url(r'^student/showupdate/(?P<object_id>\d+)/$',list_detail.object_detail,student_edit_info),
    url(r'^student/update/(?P<id>\d+)/$','studentUpdate'),
)

# for message
urlpatterns += patterns('admin.views',
    url(r'^message/$',direct_to_template,{'template':'admin/message.html'}),
    url(r'^message/list/$','messageList'),
    url(r'^message/handler/(?P<id>\d+)/$','messageHandler'),
    url(r'^message/hasunhandleredmsg/$','hasUnhandleredMsg'),

)

# 2014-4-1 add
# teacher mod url
teacher_detail_info={
    'queryset':Teacher.objects.all(),
    'template_name':'admin/teacher_detail.html',
    'template_object_name':'teacher',
}
teacher_edit_info={
    'queryset':Teacher.objects.all(),
    'template_name':'admin/teacher_edit.html',
    'template_object_name':'teacher',
}

urlpatterns += patterns('admin.views',
    url(r'^teacher/$',direct_to_template,{'template':'admin/teacher.html'}),
    url(r'^teacher/list/$','teacherList'),
    url(r'^teacher/(?P<object_id>\d+)/$',list_detail.object_detail,teacher_detail_info),
    url(r'^teacher/showadd/$',direct_to_template,{'template':'admin/teacher_edit.html'}),
    url(r'^teacher/add/$','teacherAdd'),
    url(r'^teacher/delete/$','teacherDelete'),
    url(r'^teacher/showupdate/(?P<object_id>\d+)/$',list_detail.object_detail,teacher_edit_info),
    url(r'^teacher/update/(?P<id>\d+)/$','teacherUpdate'),
)

# for task
task_info={
    'queryset':Task.objects.all(),
    'template_name':'admin/task_add.html',
    'template_object_name':'task',
}
urlpatterns += patterns('admin.views',
    url(r'^task/$',direct_to_template,{'template':'admin/task.html'}),
    url(r'^task/showadd/$',direct_to_template,{'template':'admin/task_add.html'}),
    url(r'^task/add/$','taskAdd'),
    url(r'^task/list/$','taskList'),
    url(r'^task/showupdate/(?P<object_id>\d+)/$',list_detail.object_detail,task_info),
    url(r'^task/update/(?P<id>\d+)/$','taskUpdate'),
    url(r'^task/delete/(?P<id>\d+)/$','taskDelete'),
    url(r'^task/publish/(?P<id>\d+)/$','taskPublish'),
    url(r'^task/showstudent_task/$',direct_to_template,{'template':'admin/student_task.html'}),
    url(r'^task/student_task/(?P<id>\d+)/$','studentTaskList'),
    url(r'^task/showstudent_taskdetail/(?P<id>\d+)/','showStudentTaskDetailList'),
    # id-taskid
    url(r'^task/student_taskdetail/(?P<id>\d+)/$','studentTaskDetailList'),
    url(r'^task/showstudent_taskcourseware/',direct_to_template,{'template':'admin/student_taskcourseware.html'}),
    url(r'^task/student_taskcourseware/(?P<taskid>\d+)/(?P<courseid>\d+)/$','studentTaskCoursewareList'),
)

# for system message
urlpatterns += patterns('admin.views',
    url(r'^showsystem_message/$',direct_to_template,{'template':'admin/system_message.html'}),
)

