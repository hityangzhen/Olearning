# -*- coding: utf-8 -*-
import xlrd
import traceback
import os
import string
from admin.models import Student,Teacher
from django.conf import settings
import sae
import sae.storage



# student excel columns:
# 
#   student_username | student_email | student_tele | student_department | student_position |
#   student_gender | student_age | student_identity | student_realname | student_positionid |
# 	student_remark 
# 
STUDENT_NCOLS=11

def studentModel(row):

	# if there is a student in db as the `[]`,return None
	if Student.objects.filter(student_identity=row[7]):
		return None

	s=Student()
	s.student_username=row[0].encode('utf-8')
	s.student_email=row[1]
	if type(row[2])==float:
		s.student_tele=str(long(row[2]))
	else:
		s.student_tele=str(row[2])
	s.student_department=row[3].encode('utf-8')
	s.student_position=row[4].encode('utf-8')
	if(row[5].encode('utf-8')=='男'):
		s.student_gender=True
	else:
		s.student_gender=False
	s.student_age=int(row[6])
	s.student_identity=row[7]
	s.student_realname=row[8].encode('utf-8')
	s.student_positionid=row[9]
	s.student_remark=row[10].encode('utf-8')
	# required attr
	s.student_status=True
	s.student_ischecked=False
	# default pwd is the endest 6 numbers
	s.student_userpwd=((row[7][::-1])[0:6])[::-1]
	return s

# teacher excel columns:
# 
#   teacher_username | teacher_email | teacher_tele | teacher_department | teacher_gender |
#   teacher_age | teacher_identity | teacher_realname | teacher_remark 
# 
TEACHER_NCOLS=9

def teacherModel(row):
	# if there is a teacher in db as the `[]`,return None
	if Teacher.objects.filter(teacher_identity=row[6]):
		return None

	t=Teacher()
	t.teacher_username=row[0].encode('utf-8')
	t.teacher_email=row[1]
	if type(row[2])==float:
		t.teacher_tele=str(long(row[2]))
	else:
		t.teacher_tele=str(row[2])
	t.teacher_department=row[3].encode('utf-8')
	if(row[4].encode('utf-8')=='男'):
		t.teacher_gender=True
	else:
		t.teacher_gender=False
	t.teacher_age=int(row[5])
	t.teacher_identity=row[6]
	t.teacher_realname=row[7].encode('utf-8')
	t.teacher_remark=row[8].encode('utf-8')
	# required attr
	t.teacher_status=True
	t.teacher_ischecked=False
	# default pwd is the endest 6 numbers
	t.teacher_userpwd=((row[6][::-1])[0:6])[::-1]
	return t

getModel={'0':studentModel,'1':teacherModel}

# insert|update the userinfo
def executeImport(table,tp):
	mlist=[]
	result={}
	result['count'] = 0
	result['existed']=0
	result['sum']=table.nrows-1
	result['usernames']=''

	for index in range(1,table.nrows):
		row=table.row_values(index)
		m=getModel[str(tp)](row)
		if m:
			mlist.append(m)
		else:
			result['existed'] += 1
			result['usernames'] += row[0].encode('utf-8')+' | '

	for model in mlist: 
		model.save()
		result['count'] += 1	
	
	print 'save success'
	return result

# from excel to database
from sae.storage import Bucket
def exportImport(filename,tp):
	result={}
	# for client debug
	if settings.DEBUG:
		data = xlrd.open_workbook(settings.MEDIA_ROOT+filename)
	# for sae
	else:
		bucket = Bucket('resources')
		obj = bucket.get_object_contents(filename)
		data=xlrd.open_workbook(file_contents=obj)
	table = data.sheets()[0]
	# check the column
	ncols=table.ncols
	nrows=table.nrows
	# for student
	if (tp==0 and (not ncols==11)) or (tp==1 and (not ncols==9)):
		result['status']='failured'
		result['tip']='excel列数不对'
	elif nrows<2:
		result['status']='failured'
		result['tip']='至少需要一条记录'
	else:
		statistic=executeImport(table,tp)
		result['status']='success'
		result['tip']='导入成功，共 %d 人，成功导入 %d 人，跳过 %d 人' \
		% (statistic['sum'],statistic['count'],statistic['existed'])
		result['usernames']=statistic['usernames']
	# delete the uploaded temp file
	#  for client debug
	if settings.DEBUG:
		os.remove(settings.MEDIA_ROOT+filename)
	#  for sae
	else:
		bucket.delete_object(filename)
	return result






