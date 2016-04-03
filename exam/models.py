# -*- coding: utf-8 -*-
from django.db import models
from admin.models import Student
from course.models import Course

# 习题类型 model
class ExerciseType(models.Model):
	exercise_name=models.CharField(verbose_name='习题类型名称',max_length=20)
	exercise_score=models.IntegerField(verbose_name='习题分值')
	exercise_status=models.BooleanField(verbose_name='习题状态',default=True)

# 习题 model
class Exercise(models.Model):
	exercisetype=models.ForeignKey(ExerciseType)
	exercise_title=models.CharField(verbose_name='习题标题',max_length=200)
	exercise_itema=models.CharField(verbose_name='习题选项1',max_length=100,null=True,blank=True)
	exercise_itemb=models.CharField(verbose_name='习题选项2',max_length=100,null=True,blank=True)
	exercise_itemc=models.CharField(verbose_name='习题选项3',max_length=100,null=True,blank=True)
	exercise_itemd=models.CharField(verbose_name='习题选项4',max_length=100,null=True,blank=True)
	exercise_correctitem=models.CharField(verbose_name='习题正确答案',max_length=50,null=True,blank=True)
	exercise_resolution=models.CharField(verbose_name='习题解析',max_length=200,null=True,blank=True)
	exercise_status=models.BooleanField(verbose_name='习题状态',default=True)
	exercise_course=models.IntegerField(verbose_name='课程编号',blank=True,null=True)

	def save(self, *args, **kwargs):
		# for judge exercise
		if self.exercisetype.id==1:
			self.exercise_itema='正确'
			self.exercise_itemb='错误'
		super(Exercise,self).save(*args,**kwargs)

# 试卷基本信息
class ExercisePaper(models.Model):
	exercisepaper_name=models.CharField(verbose_name='试卷名称',max_length=50)
	exercisepaper_allscore=models.IntegerField(verbose_name='试卷总分',null=True,blank=True)
	exercisepaper_passedscore=models.IntegerField(verbose_name='通过分数',null=True,blank=True)
	exercisepaper_lasttime=models.IntegerField(verbose_name='考试时长')
	exercise_starttime=models.DateTimeField(verbose_name='考试开始时间')
	exercise_endtime=models.DateTimeField(verbose_name='考试截止时间')
	exercise_status=models.BooleanField(verbose_name='试卷状态',default=True)
	exercise_ischecked=models.IntegerField(verbose_name='是否审核',null=True,blank=True)
	course=models.ForeignKey(Course)
	exercise_exercisecount=models.IntegerField(verbose_name='题目总数',null=True,blank=True)
	exercise_examtimes=models.IntegerField(verbose_name='可参加次数',null=True,blank=True)
	exercisepaperdetails=models.ManyToManyField(Exercise,through='ExercisePaperDetail')
	exercisepaper_checkedreply=models.CharField(verbose_name='审核意见',null=True,blank=True,max_length=200)

# 试卷详细信息
class ExercisePaperDetail(models.Model):
	exercise=models.ForeignKey(Exercise)
	exercisepaper=models.ForeignKey(ExercisePaper)


# 考试基本信息
class Exam(models.Model):
	student=models.ForeignKey(Student)
	exam_scores=models.IntegerField(verbose_name='考试得分',default=0)
	exercisepaper=models.ForeignKey(ExercisePaper)
	exam_starttime=models.DateTimeField(verbose_name='考试开始时间',auto_now_add=True)
	exam_endtime=models.DateTimeField(verbose_name='考试结束时间',auto_now=True)
	exam_status=models.BooleanField(verbose_name='考试状态',default=True)
	exam_markingstatus=models.BooleanField(verbose_name='考试批改状态',default=False)
	exam_remark=models.CharField(verbose_name='阅卷评语',max_length=500,null=True,blank=True)
	exam_ispassed=models.NullBooleanField(verbose_name='是否通过',blank=True)

# 考试详细信息
class ExamDetail(models.Model):
	exam=models.ForeignKey(Exam)
	exercise=models.ForeignKey(Exercise)
	examdetail_answeritem=models.CharField(verbose_name='考题答案选项',max_length=10,null=True,blank=True)
	examdetail_answercontent=models.CharField(verbose_name='考题答案陈述',max_length=500,null=True,blank=True)
	examdetail_iscorrect=models.NullBooleanField(verbose_name='考题答案是否正确')
	examdetail_answerscore=models.IntegerField(verbose_name='考题得分',null=True)

# 考试情况
class ExamSituation(models.Model):
	exam=models.ForeignKey(Exam)
	examsituation_times=models.IntegerField(verbose_name='考试次数')
	examsituation_ispassed=models.BooleanField(verbose_name='考试是否通过',default=False)
	examsituation_highestscore=models.IntegerField(verbose_name='考试最高分',null=True,blank=True)




























