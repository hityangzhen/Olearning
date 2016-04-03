from django.conf.urls import patterns, url
from django.views.generic.simple import direct_to_template
from django.views.generic import list_detail
from .models import *


urlpatterns = patterns('contact.views',
	# id-represent courseid
	url(r'^ask_question/(?P<id>\d+)/list/$','askQuestionList'),
	url(r'^ask_question/detail/(?P<id>\d+)/$','askQuestionAnswer'),
	url(r'^ask_question/add/$','saveQuestion'),
	url(r'^ask_question/(?P<id>\d+)/answer/$','answerQuestion'),
	url(r'^ask_question/delete/(?P<id>\d+)/$','deleteQuestion'),
	url(r'^ask_question/answer/delete/(?P<aq_id>\d+)/$','deleteAnswerQuestion'),
)

urlpatterns += patterns('contact.views',
	url(r'^question/$',direct_to_template,{'template':'contact/question.html'}),
	url(r'^question/list/$','courseQuestionGeneralList'),
	url(r'^question/(?P<id>\d+)/show_detail/$',direct_to_template,{'template':'contact/question_detail.html'}),
	url(r'^question/(?P<id>\d+)/detail/list/$','courseQuestionDetailList'),
	url(r'^question/(?P<id>\d+)/delete/$','ajaxDeleteQuesiton'),
	url(r'^answerquestion/(?P<id>\d+)/list/$','answerQuestionList'),
	url(r'^answerquestion/(?P<id>\d+)/shield/$','answerQuestionShield'),
	url(r'^answerquestion/(?P<id>\d+)/delete/$','answerQuestionDelete'),
)

urlpatterns += patterns('contact.views',
	url(r'^launch_topic/(?P<id>\d+)/list/$','launchTopicList'),
	url(r'^launch_topic/add/$','saveTopic'),
	url(r'^launch_topic/detail/(?P<id>\d+)/$','launchTopicReply'),
	url(r'^launch_topic/(?P<id>\d+)/reply/$','replyTopic'),
	url(r'^launch_topic/delete/(?P<id>\d+)/$','deleteTopic'),
)

urlpatterns += patterns('contact.views',
	url(r'^topic/$',direct_to_template,{'template':'contact/topic.html'}),
	url(r'^topic/list/$','courseTopicGeneralList'),
	url(r'^topic/(?P<id>\d+)/show_detail/$',direct_to_template,{'template':'contact/topic_detail.html'}),
	url(r'^topic/(?P<id>\d+)/detail/list/$','courseTopicDetailList'),
	url(r'^topic/(?P<id>\d+)/delete/$','ajaxDeleteTopic'),
	url(r'^replytopic/(?P<id>\d+)/list/$','replyTopicList'),
	url(r'^replytopic/(?P<id>\d+)/shield/$','replyTopicShield'),
)

