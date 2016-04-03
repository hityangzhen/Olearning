# -*- coding: utf-8 -*-

from django import forms
class LoginForm(forms.Form):
	username=forms.CharField(
		required=True,
		max_length=20,
		label='用户名',
		error_messages={'required':'请输入用户名'}
	)

	userpwd=forms.CharField(
		required=True,
		max_length=20,
		label='密码',
		error_messages={'required':'请输入密码'}
	)

	usertype=forms.IntegerField(
		required=True
	)