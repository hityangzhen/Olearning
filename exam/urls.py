from django.conf.urls import patterns, url
from django.views.generic.simple import direct_to_template
from django.views.generic import list_detail
from .models import ExerciseType,Exercise,ExercisePaper
from django.views.generic import list_detail

# prefix is `exam/`

# for exercisetype
urlpatterns = patterns('exam.views',
	url(r'^exercisetype/$',direct_to_template,{'template':'exam/exercisetype.html'}),
	url(r'^exercisetype/list/$','exercisetypeList'),
	url(r'^exercisetype/add/$','exercisetypeSave'),
	url(r'^exercisetype/update/$','exercisetypeUpdate'),
	url(r'^exercisetype/array/$','exercisetypeArray'),
)

exercise_info={
    'queryset':Exercise.objects.all(),
    'template_name':'exam/exercise_add.html',
    'template_object_name':'exercise',
}

# for teacher exercise
urlpatterns += patterns('exam.views',
	url(r'^teacher_exercise/$',direct_to_template,{'template':'exam/teacher_exercise.html'}),
	# id --- teacher's pk
	url(r'^teacher_exercise/(?P<id>\d+)/generallist/$','exerciseGeneralList'),
	# id --- course's pk
	url(r'^teacher_exercise/(?P<id>\d+)/$',direct_to_template,{'template':'exam/exercise.html'}),
	url(r'^teacher_exercise/(?P<id>\d+)/list/$','exerciseList'),
	url(r'^teacher_exercise/(?P<id>\d+)/showadd/$',direct_to_template,{'template':'exam/exercise_add.html'}),
	url(r'^teacher_exercise/(?P<id>\d+)/add/$','exerciseAdd'),
	url(r'^teacher_exercise/(\d+)/showupdate/(?P<object_id>\d+)/$',list_detail.object_detail,exercise_info),
	url(r'^teacher_exercise/(?P<course_id>\d+)/update/(?P<id>\d+)/$','exerciseUpdate'),
)

exercisepaper_info={
    'queryset':ExercisePaper.objects.all(),
    'template_name':'exam/exercisepaper_add.html',
    'template_object_name':'exercisepaper',
}

# for teacher exercise paper
urlpatterns += patterns('exam.views',
	url(r'^teacher_exercisepaper/$',direct_to_template,{'template':'exam/teacher_exercisepaper.html'}),
	# id --- teacher's pk
	url(r'^teacher_exercisepaper/(?P<id>\d+)/generallist/$','exercisePaperGeneralList'),
	# id --- course's pk
	url(r'^teacher_exercisepaper/(?P<id>\d+)/$',direct_to_template,{'template':'exam/exercisepaper.html'}),
	url(r'^teacher_exercisepaper/(?P<id>\d+)/list/$','exercisePaperList'),
	url(r'^teacher_exercisepaper/(?P<id>\d+)/showadd/$',direct_to_template,{'template':'exam/exercisepaper_add.html'}),
	url(r'^teacher_exercisepaper/(\d+)/showupdate/(?P<object_id>\d+)/$',list_detail.object_detail,exercisepaper_info),
	url(r'^teacher_exercisepaper/(?P<id>\d+)/add/$','exercisePaperAdd'),
	url(r'^teacher_exercisepaper/(?P<id>\d+)/delete/(?P<exercisepaper_id>\d+)/$','exercisePaperDelete'),
	url(r'^teacher_exercisepaper/(?P<id>\d+)/update/(?P<exercisepaper_id>\d+)/$','exercisePaperUpdate'),
	url(r'^teacher_exercisepaper/(?P<id>\d+)/publish/(?P<exercisepaper_id>\d+)/$','exercisePaperPublish'),
	url(r'^teacher_exercisepaper/(\d+)/addedexercise/(?P<exercisepaper_id>\d+)/$','exercisePaperAddedExerciseList'),
	url(r'^teacher_exam/show_verify/$',direct_to_template,{'template':'exam/teacher_exam_verify.html'}),
	url(r'^teacher_exam/verify/list/$','teacherExamVerifyList'),
	url(r'^teacher_exam/verify/(?P<id>\d+)/$','teacherExamVerifyDetail'),
	url(r'^teacher_exam/verify/(?P<id>\d+)/save/$','teacherExamVerifysSave'),
)

#for administrator exercise paper
urlpatterns += patterns('exam.views',
	url(r'^admin_exercisepaper/show_check/$',direct_to_template,{'template':'exam/exercisepaper_check.html'}),
	url(r'^admin_exercisepaper/check/list/$','waitingAdminCheckExercisepaperList'),
	url(r'^admin_exercisepaper/check/(?P<id>\d+)/$','checkExercisePaper'),
)

# for student exercise paper
urlpatterns += patterns('exam.views',
	url(r'^student_exercisepaper/(?P<id>\d+)/$',direct_to_template,{'template':'exam/student_exercisepaper.html'}),
	url(r'^student_exercisepaper/(?P<id>\d+)/list/$','studentExercisePaperList')
)

exercisepaperpreview_info={
    'queryset':ExercisePaper.objects.all(),
    'template_name':'exam/exercisepreview.html',
    'template_object_name':'exercisepaper',
}

exam_info={
    'queryset':ExercisePaper.objects.all(),
    'template_name':'exam/exam.html',
    'template_object_name':'exercisepaper',
}
# for online exam
urlpatterns +=patterns('exam.views',
	url(r'^exercisepaperpreview/(?P<object_id>\d+)/$',list_detail.object_detail,exercisepaperpreview_info),
	url(r'^student/exam/(?P<object_id>\d+)/$','studentExam'),
	url(r'^student/exam/(?P<id>\d+)/finish/$','studentExamFinish'),
	# id-represent exam'is
	url(r'^student/exam/result/(?P<id>\d+)/$','studentExamResult'),
	url(r'^student/show_participated/$',direct_to_template,{'template':'exam/student_general_exam.html'}),
	url(r'^student/participated/list/$','studentGeneralExamList'),	
	url(r'^student/show_participated/(?P<exercisepaper_id>\d+)/$',direct_to_template,{'template':'exam/student_detail_exam.html'}),	
	url(r'^student/show_participated/(?P<exercisepaper_id>\d+)/list/$','studentDetailExamList'),	
)



