from django.conf.urls import patterns, url
from django.views.generic.simple import direct_to_template
from django.views.generic import list_detail
from course.models import Course,Resource


#for courseware's note 

resource_info={
	'queryset':Resource.objects.all(),
    'template_name':'learn/view.html',
    'template_object_name':'resource',
}

# for exercisetype
urlpatterns = patterns('learn.views',

	url(r'^view/(?P<task_id>\d+)/(?P<course_id>\d+)/(?P<id>\d+)/$','coursewareView'),
	url(r'^view/finish/(?P<id>\d+)/$','coursewareViewFinish'),
)
