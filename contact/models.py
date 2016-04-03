# -*- coding: utf-8 -*-
from django.db import models
from admin.models import Student
from course.models import Course

# 疑问 model
class Question(models.Model):
	question_title=models.CharField(verbose_name='疑问标题',max_length=100)
	student=models.ForeignKey(Student)
	question_starttime=models.DateTimeField(verbose_name='提问时间',auto_now_add=True)
	question_status=models.BooleanField(verbose_name='疑问状态',default=True)
	question_content=models.CharField(verbose_name='疑问内容',max_length=500)
	course=models.ForeignKey(Course)
	question_viewtimes=models.IntegerField(verbose_name='浏览次数',default=0)

# 答疑 model
class AnswerQuestion(models.Model):
	answerquestion_content=models.CharField(verbose_name='答疑内容',max_length=500)
	answerquestion_userid=models.IntegerField(verbose_name='答疑用户编号')
	answerquestion_usertype=models.IntegerField(verbose_name='答疑用户类型')
	answerquestion_time=models.DateTimeField(verbose_name='答疑时间',auto_now=True)
	answerquestion_status=models.BooleanField(verbose_name='答疑状态',default=True)
	question=models.ForeignKey(Question)

# 话题表
class Topic(models.Model):
	topic_title=models.CharField(verbose_name='话题标题',max_length=100)
	topic_content=models.CharField(verbose_name='话题内容',max_length=500)
	topic_userid=models.IntegerField(verbose_name='话题用户编号')
	topic_status=models.BooleanField(verbose_name='话题状态',default=True)
	course=models.ForeignKey(Course)
	topic_usertype=models.IntegerField(verbose_name='话题用户类型')
	topic_viewtimes=models.IntegerField(verbose_name='浏览次数',default=0)
	topic_starttime=models.DateTimeField(verbose_name='话题时间',auto_now_add=True)

# 话题回复
class TopicReply(models.Model):
	topicreply_title=models.CharField(verbose_name='回复标题',max_length=200)
	topicreply_isreply=models.BooleanField(verbose_name='是否为回复')
	topicreply_content=models.CharField(verbose_name='话题回复内容',max_length=500)
	topicreply_referencecontent=models.CharField(verbose_name='话题引用内容',max_length=500,null=True)
	topicreply_replyid=models.IntegerField(verbose_name='话题回复/引用编号')
	topicreply_userid=models.IntegerField(verbose_name='话题回复用户')
	topicreply_status=models.BooleanField(verbose_name='话题回复状态')
	topicreply_time=models.DateTimeField(verbose_name='话题回复时间',auto_now_add=True)
	topic=models.ForeignKey(Topic)
	topicreply_usertype=models.IntegerField(verbose_name='话题回复用户类型')







































































