# -*- coding: utf-8 -*-
# extra tags and filter for template

from django import template
from exam.models import *

register = template.Library()

@register.filter(name='timeformat')
def timeformat(date, delimiter):
    if date:
	   return str(date.month)+delimiter+str(date.day)+delimiter+str(date.year)
    return ''

@register.filter(name='simpletimeformat')
def simpletimeformat(date,delimiter):
    if date:
	   return str(date.year)+delimiter+str(date.month)+delimiter+str(date.day)
    return ''

@register.filter(name='fulltimeformat')
def fulltimeformat(datetime):
    if datetime:
        date=datetime.date()
        time=datetime.time()
        return '%d-%d-%d %d:%d:%d' % (date.year,date.month,date.day,time.hour,time.minute,time.second)
    return ''

# timelength is minutes
@register.filter(name='timeingformat')
def timeingformat(timelength):
    if timelength:
        minute=int(timelength)
        hour=minute/60
        minute-=hour*60 
        return '%02d:%02d:%02d' % (hour,minute,0)

    return '00:00:00'

@register.filter(name='exercisesByType')
def exercisesByType(queryset,t):
	return queryset.filter(exercisetype__id=t)

@register.filter(name='exerciseScore')
def exerciseScore(queryset,t):
	return queryset[0].exercisetype.exercise_score * len(queryset.filter(exercisetype__id=t))

@register.filter(name='exerciseiscorrect')
def exerciseiscorrect(exercise,exam):
    ed=ExamDetail.objects.filter(exercise=exercise).filter(exam=exam)
    if ed:
        if ed[0].examdetail_iscorrect:
            return '正确'
        else:
            return '错误'
    else:
        return '错误，此题未做'

@register.filter(name='exercisescore')
def exercisescore(exercise,exam):
    ed=ExamDetail.objects.filter(exercise=exercise).filter(exam=exam)
    if ed:
        return ed[0].examdetail_answerscore
    else:
        return 0

@register.filter(name='examispassed')
def examispassed(exam):
    if exam.exam_ispassed:
        return '通过'
    else:
        return '没有通过，下次努力'

@register.filter(name='radioanswer')
def radioanswer(exercise,exam):
    ed=ExamDetail.objects.filter(exercise=exercise,exam=exam)
    if ed:
        return ExamDetail.objects.filter(exercise=exercise,exam=exam)[0].examdetail_answeritem
    else:
        return '此题未答'

@register.filter(name='statementanswer')
def statementanswer(exercise,exam):
    ed=ExamDetail.objects.filter(exercise=exercise,exam=exam)
    if ed:
        return ExamDetail.objects.filter(exercise=exercise,exam=exam)[0].examdetail_answercontent
    else:
        return '此题未答'        




# set variable tags
class SetVarNode(template.Node):
    '''
    usage
    {% set <var_name> = <var_value> %}
    For example
    {% set count = 1 %}
    '''

    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value=''
        context[self.var_name] = value
        return u""

def set_var(parser, token):
    """
        {% set <var_name>  = <var_value> %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form:  {% set <var_name>  = <var_value> %}")
    return SetVarNode(parts[1], parts[3])

register.tag('set', set_var)

# ---------- increment tag ----------

def increment_var(parser, token):

    parts = token.split_contents()
    if len(parts) < 2:
        raise template.TemplateSyntaxError("'increment' tag must be of the form:  {% increment <var_name> %}")
    return IncrementVarNode(parts[1])

register.tag('++', increment_var)

class IncrementVarNode(template.Node):
    '''
    usage
    {% ++ <var_name> %}
    For example
    {% ++ a %}
    '''

    def __init__(self, var_name):
        self.var_name = var_name

    def render(self,context):
        try:
            value = context[self.var_name]
            context[self.var_name] = value + 1
            return u""
        except:
            raise template.TemplateSyntaxError("The variable does not exist.")





    