from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from .models import TcVersion,TcModule

class LoginForm(forms.Form):
	username = forms.CharField(label='用户名',max_length=20,error_messages={'required': 'Please enter your name'})
	password = forms.CharField(label='密码',max_length=20)

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']

		user = auth.authenticate(username=username, password=password)
		if user is None:
			raise forms.ValidationError('用户名或密码不正确')
		else:
			self.cleaned_data['user'] = user
		return self.cleaned_data



class RegForm(forms.Form):
	username = forms.CharField(label='用户名',max_length=20)
	phone = forms.CharField(label='手机号',max_length=11)
	password = forms.CharField(label='密码',max_length=20)
	password_again = forms.CharField(label='再次输入密码',max_length=20)


	def clean_username(self):
	    username = self.cleaned_data['username']
	    if User.objects.filter(username=username).exists():
	        raise forms.ValidationError('用户名已存在')
	    return username

	def clean_password_again(self):
	    password = self.cleaned_data['password']
	    password_again = self.cleaned_data['password_again']
	    if password != password_again:
	        raise forms.ValidationError('两次输入的密码不一致')
	    return password_again


class CaseForm(forms.Form):	

	def version_list():
		r = []
		for obj in TcVersion.objects.all():
			r = r + [(obj.id, obj.version_name)]
		return r

	def module_list():
		r = []
		for obj in TcModule.objects.all():
			r = r + [(obj.id, obj.module_name)]
		return r

	casename = forms.CharField(label='用例名称',max_length=20)
	style = [('UI','UI'),('Function','功能'),('Perfermance','性能')]
	casestyle = forms.ChoiceField(label='用例类型',widget=forms.Select,choices=style)
	level = [('SMOKING','冒烟'),('Function','LEVEL0'),('LEVEL1','LEVEL1'),('LEVEL2','LEVEL2')]
	caselevel = forms.ChoiceField(label='用例等级',choices=level,widget=forms.Select)
	case_presetting = forms.CharField(label='前置条件',widget=forms.Textarea,required=False)
	case_steps = forms.CharField(label='测试步骤',widget=forms.Textarea)
	module = module_list()
	case_module = forms.ChoiceField(label='所属模块',widget=forms.Select,choices=module)
	version =version_list()
	case_version = forms.ChoiceField(label='所属版本',widget=forms.Select,choices=version)
	case_result = forms.CharField(label='期望结果',widget=forms.Textarea)	
	case_assign = forms.CharField(label='指派人')
	case_comment = forms.CharField(label='备注',widget=forms.Textarea,required=False)





