# -*- coding: utf-8 -*-
from django.db import models
from tools.MyStorage import FileStorage

# Create your models here.
# 课程类型 model
class CourseType(models.Model):
	coursetype_name = models.CharField(max_length = 20)
	coursetype_positionid = models.CharField(max_length = 20)
	coursetype_status = models.BooleanField(default=True)

	# dict attributes
	def toDICT(self):
		fields=[]
		for field in self._meta.fields:
			fields.append(field.name)
		d={}
		for attr in fields:
			d[attr]=getattr(self,attr)
		return d
# 管理员 model
class Administrator(models.Model):
	administrator_username=models.CharField(verbose_name='管理员用户名',max_length=20)
	administrator_userpwd=models.CharField(verbose_name='管理员密码',max_length=20)
	administrator_email=models.EmailField(verbose_name='管理员邮箱',max_length=40)
	administrator_realname=models.CharField(verbose_name='管理员姓名',max_length=20)
	administrator_tele=models.CharField(verbose_name='管理员联系方式',max_length=11)
	administrator_status=models.BooleanField(verbose_name='管理员状态',default=True)

# 学员 model
class Student(models.Model):
	student_username=models.CharField(verbose_name='学员用户名',max_length=20)
	student_userpwd=models.CharField(verbose_name='学员密码',max_length=20,blank=True)
	student_email=models.EmailField(verbose_name='学员邮箱',max_length=40)
	student_tele=models.CharField(verbose_name='学员联系方式',max_length=11)
	student_department=models.CharField(verbose_name='学员部门',max_length=30)
	student_position=models.CharField(verbose_name='学员职位',max_length=30)
	student_gender=models.BooleanField(verbose_name='学员性别')
	student_age=models.IntegerField(verbose_name='学员年龄',default=0)
	student_head_portrait=models.FileField(verbose_name='学员头像',upload_to='photo/student',null=True,blank=True,storage=FileStorage())
	student_identity=models.CharField(verbose_name='学员身份证',max_length=18)
	student_remark=models.CharField(verbose_name='学员备注',max_length=500,null=True,blank=True)
	student_status=models.BooleanField(verbose_name='学员状态',default=True)
	student_positionid=models.CharField(verbose_name='学员职位编号',max_length=20)
	student_ischecked=models.BooleanField(verbose_name='是否审核',default=False)
	# 2014-3-31 add
	student_realname=models.CharField(verbose_name='学员真实姓名',max_length=50,null=True)

	def toDICT(self):
		d={}
		d['student_username']=getattr(self,'student_username')
		d['student_email']=getattr(self,'student_email')
		d['student_tele']=getattr(self,'student_tele')
		d['student_department']=getattr(self,'student_department')
		d['student_position']=getattr(self,'student_position')
		d['student_gender']=getattr(self,'student_gender')
		d['student_status']=getattr(self,'student_status')
		return d

	def delete(self, using=None):
		try:
			print 'delete student' 
			if self.student_head_portrait:
				self.student_head_portrait.storage.delete(self.student_head_portrait.name)
		except Exception, e:
			raise Exception('delete student failured')
		super(Student, self).delete(using=using)
	
# 教师表
class Teacher(models.Model):
	teacher_username=models.CharField(verbose_name='教师用户名',max_length=20)
	teacher_userpwd=models.CharField(verbose_name='教师密码',max_length=20,blank=True)
	teacher_email=models.EmailField(verbose_name='教师邮箱',max_length=40)
	teacher_tele=models.CharField(verbose_name='教师联系方式',max_length=11)
	teacher_department=models.CharField(verbose_name='教师部门',max_length=30)
	teacher_identity=models.CharField(verbose_name='教师身份证',max_length=18)
	teacher_realname=models.CharField(verbose_name='教师姓名',max_length=30)
	teacher_gender=models.BooleanField(verbose_name='教师性别',default=True)
	teacher_age=models.IntegerField(verbose_name='教师年龄',default=0)
	teacher_head_portrait=models.FileField(verbose_name='教师头像',upload_to='photo/teacher',null=True,blank=True,storage=FileStorage())
	teacher_remark=models.CharField(verbose_name='教师备注',max_length=500,null=True,blank=True)
	teacher_status=models.BooleanField(verbose_name='教师状态',default=True)
	teacher_ischecked=models.BooleanField(verbose_name='是否审核',default=False)

	# dict attributes
	def toDICT(self):
		fields=[]
		for field in self._meta.fields:
			fields.append(field.name)
		d={}
		for attr in fields:
			d[attr]=getattr(self,attr)
		return d

	# simple dict sttributes
	# include `id` and `teacher_realname`
	def toSIMPLEDICT(self):
		d={}
		d['id']=getattr(self,'id')
		d['teacher_realname']=getattr(self,'teacher_realname')
		return d

	def delete(self, using=None):
		try:
			print 'delete teacher' 
			if self.teacher_head_portrait:
				self.teacher_head_portrait.storage.delete(self.teacher_head_portrait.name)
		except Exception, e:
			raise Exception('delete teacher failured')
		super(Teacher, self).delete(using=using)

# 学习任务表
class Task(models.Model):
	task_name=models.CharField(verbose_name='任务名称',max_length=50)
	coursetype=models.ForeignKey(CourseType)
	task_courseids=models.CharField(verbose_name='任务课程编号',max_length=50)
	task_exercisepaperids=models.CharField(verbose_name='任务练习编号',max_length=100,null=True,blank=True)
	task_starttime=models.DateTimeField(verbose_name='任务开始时间')
	task_endtime=models.DateTimeField(verbose_name='任务结束时间')
	task_status=models.BooleanField(verbose_name='任务状态',default=True)
	task_ispublished=models.NullBooleanField(verbose_name='是否发布',default=False)

class Message(models.Model):
	message_content=models.CharField(verbose_name='消息内容',max_length=100,null=True)
	message_type=models.IntegerField(verbose_name='消息类型',default=0)
	message_ishandlered=models.BooleanField(verbose_name='消息是否处理',default=False)
	message_receiverid=models.IntegerField(verbose_name='消息接受用户编号')
	message_receivertype=models.IntegerField(verbose_name='消息接受用户类型')
	message_senderid=models.IntegerField(verbose_name='消息发送用户编号')
	message_sendertype=models.IntegerField(verbose_name='消息发送用户类型')
	message_starttime=models.DateTimeField(verbose_name='消息产生时间',auto_now_add=True)


