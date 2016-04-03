# -*- coding: utf-8 -*-
from django.db import models
from admin.models import Student,Task
from course.models import Course,Resource

# 学习基本信息 model
class Learn(models.Model):
	course=models.ForeignKey(Course)
	resource=models.ForeignKey(Resource)
	student=models.ForeignKey(Student)
	learn_times=models.IntegerField(verbose_name='课件学习次数',default=0)
	learn_rate=models.IntegerField(verbose_name='课件学习进度',default=0)
	learn_status=models.IntegerField(verbose_name='课件学习状态',default=0)
	# added 2014-4-21
	learn_timelength=models.IntegerField(verbose_name='课件学习时长',default=0)
	learn_standardtimelength=models.IntegerField(verbose_name='课件达标学习时长',default=0)
	# endadded

# 学习信息详细 model
class LearnDetail(models.Model):
	learn=models.ForeignKey(Learn)
	learn_starttime=models.DateTimeField(verbose_name='开始时间',auto_now_add=True)
	learn_endtime=models.DateTimeField(verbose_name='结束时间',auto_now=True,blank=True)
	learn_timelength=models.IntegerField(verbose_name='学习时长',default=0,blank=True)

# 学员课程学习 model
class CourseLearning(models.Model):
	course=models.ForeignKey(Course)
	courselearning_status=models.IntegerField(verbose_name='课程学习状态',default=0)
	courselearning_credit=models.IntegerField(verbose_name='课程获得学分',default=0)
	courselearning_rate=models.IntegerField(verbose_name='课程进度',default=0)
	# added 2014-4-21
	courselearning_timelength=models.IntegerField(verbose_name='课程学习时长',default=0)
	courselearning_standardtimelength=models.IntegerField(verbose_name='课程达标学习时长',default=0)
	# end added
	student=models.ForeignKey(Student)
	task=models.ForeignKey(Task)

# 学员任务状态 model
class TaskLearning(models.Model):
	student=models.ForeignKey(Student)
	tasklearning_status=models.IntegerField(verbose_name='学员任务状态',default=0)
	tasklearning_score=models.IntegerField(verbose_name='学员任务获得学分',default=0)
	task=models.ForeignKey(Task)
	tasklearning_rate=models.IntegerField(verbose_name='学员任务进度',default=0)
	# added 2014-4-21
	tasklearning_timelength=models.IntegerField(verbose_name='任务学习时长',default=0)
	tasklearning_standardtimelength=models.IntegerField(verbose_name='任务达标学习时长',default=0)
	# end added




