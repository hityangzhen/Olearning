	# -*- coding: utf-8 -*-
from django.db import models
from admin.models import CourseType,Teacher,Student
from tools.MyFile import SAEFileField
# from django.dispatch import receiver
import os
from django.db.models.signals import pre_save,post_delete
from tools.MyStorage import FileStorage


# 课程 model
class Course(models.Model):
	course_name=models.CharField(verbose_name='课程名称',max_length=100)
	course_description=models.CharField(verbose_name='课程简介',max_length=500)
	course_tags=models.CharField(verbose_name='课程标签',max_length=50)
	course_icon=models.FileField(verbose_name='课程图标',upload_to='photo/course',storage=FileStorage())
	teacher=models.ForeignKey(Teacher,blank=True)
	course_lessonnum=models.IntegerField(verbose_name='课程课时数',null=True,blank=True)
	course_outline=models.CharField(verbose_name='课程大纲',max_length=500,null=True,blank=True)
	course_credit=models.IntegerField(verbose_name='课程学分')
	course_learner=models.CharField(verbose_name='课程对象',max_length=50,null=True,blank=True)
	course_status=models.BooleanField(verbose_name='课程状态',default=True,blank=True)
	coursetype=models.ForeignKey(CourseType)
	# update 2014-4-7
	course_ischecked=models.NullBooleanField(verbose_name='课程是否审核',blank=True)
	# end update
	course_checkedReply=models.CharField(max_length=200,verbose_name='课程审核意见',null=True,blank=True)

	def delete(self, using=None):
		try:
			print 'delete course ' 
			self.course_icon.storage.delete(self.course_icon.name)
		except Exception, e:
			raise Exception('delete course failured')
		super(Course, self).delete(using=using)

	#-------------------------------------------add 2014-3-27---------------------------------------
	def toSIMPLEDICT(self):
		d={}
		d['course_name']=getattr(self,'course_name')
		d['course_description']=getattr(self,'course_description')
		d['course_tags']=getattr(self,'course_tags')
		d['course_credit']=getattr(self,'course_credit')
		d['course_learner']=getattr(self,'course_learner')
		d['coursetype']=self.coursetype.id
		d['course_outline']=getattr(self,'course_outline')
		return d

	def __str__(self):
		return self.course_name

# # @receiver(models.signals.post_delete, sender=Course)
# def after_delete_course(sender, **kwargs):
#     """Deletes file from filesystem
#     when corresponding `MediaFile` object is deleted.
#     """
#     instance=kwargs['instance']
#     if instance.course_icon:
#     	print 'delete course'
#         # if os.path.isfile(instance.course_icon.path):
#         #     os.remove(instance.course_icon.path)
#         instance.course_icon.storage.delete( instance.course_icon.name)

# # signal after course.delete()
# post_delete.connect(after_delete_course, sender=Course)

# # @receiver(models.signals.pre_save, sender=Course)
# def before_save_course(sender, **kwargs):
#     """Deletes file from filesystem
#     when corresponding `MediaFile` object is changed.
#     """
#     instance=kwargs['instance']
#     if not instance.pk:
#         return False

#     try:
#         old_course_icon = Course.objects.get(pk=instance.pk).course_icon
#     except Course.DoesNotExist:
#     	return False

#     new_course_icon = instance.course_icon
#     if not new_course_icon == old_course_icon:
#         if os.path.isfile(old_course_icon.path):
#             os.remove(old_course_icon.path)
# # signal bofore the course.save()
# pre_save.connect(before_save_course, sender=Course)


# 资料 model
class Resource(models.Model):
	resource_name=models.CharField(verbose_name='资源名称',max_length=100)
	resource_size=models.DecimalField(verbose_name='资源大小',max_digits=5,decimal_places=2,null=True,blank=True)
	resource_uploader=models.CharField(verbose_name='资源上传者',max_length=30,blank=True)
	course=models.ForeignKey(Course)
	resource_iscourseware=models.BooleanField(verbose_name='是否为课件')
	resource_candownload=models.BooleanField(verbose_name='是否可下载')
	resource_tags=models.CharField(verbose_name='资源标签',max_length=50)
	resource_standardtime=models.IntegerField(verbose_name='课件达标时长',null=True,blank=True)
	resource_viewtimes=models.IntegerField(verbose_name='资源浏览次数',default=0,blank=True)
	resource_downloadtimes=models.IntegerField(verbose_name='资源下载次数',default=0,blank=True)
	resource_status=models.BooleanField(verbose_name='资源状态',default=True,blank=True)
	resource_path=models.FileField(verbose_name='资源路径',upload_to='resource',storage=FileStorage())

	def delete(self, using=None):
		try:
			print 'delete resource'
			self.resource_path.storage.delete(self.resource_path.name)
		except Exception, e:
			raise Exception('delete resource failured')
		super(Resource, self).delete(using=using)
		

def after_delete_resource(sender, **kwargs):
    """Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    instance=kwargs['instance']
    if instance.resource_path:
        if os.path.isfile(instance.resource_path.path):
        	print 'exist file : %s' % (instance.resource_path.path)
        	os.remove(instance.resource_path.path)
# signal after course.delete()
post_delete.connect(after_delete_resource, sender=Resource)

# def before_save_resource(sender, **kwargs):
#     """Deletes file from filesystem
#     when corresponding `MediaFile` object is changed.
#     """
#     instance=kwargs['instance']
#     if not instance.pk:
#         return False

#     try:
#         old_resource_path = Resource.objects.get(pk=instance.pk).resource_path
#     except Resource.DoesNotExist:
#     	return False

#     new_resource_path = instance.resource_path
#     if not new_resource_path == old_resource_path:
#         if os.path.isfile(old_resource_path.path):
#             os.remove(old_resource_path.path)
# # signal bofore the course.save()
# pre_save.connect(before_save_resource, sender=Resource)



# 课程公告 model
class CourseNotice(models.Model):
	course=models.ForeignKey(Course)
	coursenotice_title=models.CharField(verbose_name='公告标题',max_length=100)
	coursenotice_content=models.CharField(verbose_name='公告内容',max_length=500)
	coursenotice_status=models.BooleanField(verbose_name='公告状态',default=True)
	teacher=models.CharField(null=True,blank=True,max_length=50)
	coursenotice_time=models.DateTimeField(verbose_name='公告发布时间',auto_now=True)

# 课程评论 model
class CourseComment(models.Model):
	coursecomment_userid=models.IntegerField(verbose_name='评论用户编号')
	coursecomment_usertype=models.IntegerField(verbose_name='评论用户类型')
	coursecomment_score=models.IntegerField(verbose_name='评论分数',null=True,blank=True)
	coursecomment_content=models.CharField(verbose_name='评论内容',max_length=500)
	coursecomment_status=models.BooleanField(verbose_name='评论状态',default=True)
	course=models.ForeignKey(Course)
	coursecomment_time=models.DateTimeField(verbose_name='评论时间',auto_now=True)

# 课程笔记 model
class CourseNote(models.Model):
	course=models.ForeignKey(Course)
	coursenote_title=models.CharField(verbose_name='笔记标题',max_length=100)
	coursenote_content=models.CharField(verbose_name='笔记内容',max_length=500)
	student=models.ForeignKey(Student)
	coursenote_status=models.BooleanField(verbose_name='笔记状态',default=True)
	coursenote_ispublic=models.BooleanField(verbose_name='是否公开',default=False)
	coursenote_viewtimes=models.IntegerField(verbose_name='笔记浏览次数',default=0)
	coursenote_time=models.DateTimeField(verbose_name='笔记记载时间',auto_now=True)



































