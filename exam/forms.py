from django.forms import ModelForm
from .models import ExerciseType,Exercise,ExercisePaper

# model form
class ExerciseTypeForm(ModelForm):
	class Meta:
		model=ExerciseType

class ExerciseForm(ModelForm):
	class Meta:
		model=Exercise
		exclude=('exercisetype','exercise_course')

class ExercisePaperForm(ModelForm):
	class Meta:
		model=ExercisePaper
		exclude=('exercise_ischecked','course','exercisepaperdetails')
