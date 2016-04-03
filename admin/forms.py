from django.forms import ModelForm
from admin.models import CourseType,Student,Teacher,Task

# model form
class CourseTypeForm(ModelForm):
	class Meta:
		model=CourseType

class StudentForm(ModelForm):
	class Meta:
		model=Student
		exclude=('student_ischecked',)

class TeacherForm(ModelForm):
	class Meta:
		model=Teacher
		exclude=('teacher_ischecked',)

class TaskForm(ModelForm):
	class Meta:
		model=Task
		exclude=('coursetype',)

