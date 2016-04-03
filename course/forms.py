from django.forms import ModelForm
from course.models import *

# model form
class CourseForm(ModelForm):
	class Meta:
		model=Course
		exclude=('coursetype','teacher')

class ResourceForm(ModelForm):
	class Meta:
		model=Resource
		exclude=('course','teacher','resource_viewtimes','resource_downloadtimes')

class CourseNoticeForm(ModelForm):
	class Meta:
		model=CourseNotice
		exclude=('course','coursenotice_time')

class CourseNoteForm(ModelForm):
	class Meta:
		model=CourseNote
		exclude=('course','student','coursenote_status','coursenote_ispublic','coursenote_time')

class CourseCommentForm(ModelForm):
	class Meta:
		model=CourseComment
		exclude=('course','coursecomment_status','coursecomment_time')
