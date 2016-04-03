# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from .forms import LoginForm
from django.shortcuts import render_to_response,redirect,render
from django.template import RequestContext
from tools.MyAuthenticate import authenticate
from django.forms.util import ErrorList
from django.utils import simplejson
from admin.models import *
import traceback
from django.core.mail import send_mail
import sae.mail

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# override the render_to_response
def __response(template,d,request):
	if not d:
		d={}
	return render_to_response(template,d,context_instance=RequestContext(request))



def server_error404(request):
	return render_to_response('404.html',{'request':request})

def server_error500(request):
	return render_to_response('500.html',{'request':request})

def login(request):
	if request.method=='GET':
		form=LoginForm()
		return render_to_response('login.html',context_instance=RequestContext(request))
	else:
		form=LoginForm(request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			userpwd=form.cleaned_data['userpwd']
			usertype=form.cleaned_data['usertype']

			user=authenticate(username,userpwd,usertype)
			if user:
				if user.is_active():
					request.session['user']=user
					return HttpResponseRedirect(settings.MAIN_URLS[usertype])
				else:
					error_msg=['用户没有激活']
					form.errors['user'] = ErrorList(error_msg)
			else:
				error_msg=['用户名或密码不正确']
				form.errors['login'] = ErrorList(error_msg)
			form.login_username=username
			return render_to_response('login.html', {'form':form},context_instance=RequestContext(request))
		else:
			return render_to_response('login.html', {'form':form},context_instance=RequestContext(request))

def logout(request):
	del request.session['user']
	return HttpResponseRedirect('/index/')


# decorator
def islogin(func):
	def __checkSession(request):
		if ('user' in request.session) and request.session['user']:
			return func(request)
		else:
			# ajax request
			if request.is_ajax():
				result={'status':'nosession','tip':'请重新登录'}
				return HttpResponse(simplejson.dumps(result),mimetype='application/json')
			else:
				return HttpResponseRedirect('/index/')
	return __checkSession


# 
def __sendPasswordToUserMail(user,email):
	pwd=''
	if isinstance(user,Student):
		pwd=user.student_userpwd
	elif isinstance(user,Teacher):
		pwd=user.teacher_userpwd
	else:
		pwd=user.administrator_userpwd

	if settings.DEBUG:
		send_mail('学习系统找回密码','请牢记您的密码:\n'+pwd, settings.EMAIL_HOST_USER,[email], fail_silently=False)
	else:
		sae.mail.send_mail(email,'学习系统找回密码','请牢记您的密码:\n'+pwd,
			(settings.EMAIL_HOST, 25, settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD, False))		



# 
def findPwd(request):
	try:
		usertype=int(request.POST.get('usertype'))
		username=request.POST.get('username')
		email=request.POST.get('email')

		if usertype==0:
			user=Student.objects.filter(student_username=username,student_email=email)
		elif usertype==1:
			user=Teacher.objects.filter(teacher_username=username,teacher_email=email)
		else:
			user=Administrator.objects.filter(administrator_username=username,administrator_email=email)
		result={}

		if user:
			result['status']='success'
			result['tip']='邮件已发送,请登陆邮箱取回密码'
			result['email']=email
			__sendPasswordToUserMail(user[0],email)
			return __response('findpwd_result.html',{'result':result},request)
		else:
			result['status']='failure'
			result['tip']='用户名或邮箱错误'
			return __response('forgetpwd.html',{'result':result},request)

	except Exception,e:
		return __response('500.html',{'stackinfo':traceback.format_exc()},request)







