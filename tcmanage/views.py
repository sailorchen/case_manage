from django.shortcuts import render,redirect,get_object_or_404
from .models import TcVersion,TcModule,TcUser,TcCase
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import LoginForm,RegForm,CaseForm


# Create your views here.
#获取所有的版本
def get_version(request):
	context = {}
	version_list = TcVersion.objects.all()
	context['version_list'] = version_list
	return render(request,'versions.html',context)

#添加版本
def add_version(request):
	context = {}
	if request.method == 'GET':		
		return render(request,'add_version.html',context)
	elif request.method =='POST':
		version_name = request.POST.get('version_name',"")
		if version_name:
			context['version_name'] = version_name
			add_version = TcVersion()
			add_version.version_name=version_name
			add_version.save()
			return redirect('versions')
#获取所有的模块
def get_module(request):
	context = {}
	module_list = TcModule.objects.all()
	context['module_list'] = module_list
	return render(request,'models.html',context)

#添加模块
def add_module(request):
	context = {}
	if request.method == 'GET':		
		return render(request,'add_module.html',context)
	elif request.method =='POST':
		module_name = request.POST.get('module_name',"")
		if module_name:
			context['module_name'] = module_name
			add_module = TcModule()
			add_module.module_name=module_name
			add_module.save()
			return redirect('models')

#获取所有的测试用例
def get_testcase(request):
	context = {}
	case_list = TcCase.objects.all()
	context['case_list'] = case_list
	return render(request,'testcases.html',context)

def version_list(request):
	r = [('', '----')]
	for obj in TcVersion.objects.all():
		r = r + [(obj.id, obj.version_name)]
	return r


#添加用例
def add_testcase(request):
	if request.method == 'POST':
		case_form = CaseForm(request.POST)
		if case_form.is_valid():
			casename = case_form.cleaned_data['casename']
			casestyle = case_form.cleaned_data['casestyle']
			caselevel = case_form.cleaned_data['caselevel']
			case_presetting = case_form.cleaned_data['case_presetting']
			case_steps = case_form.cleaned_data['case_steps']
			case_module = TcModule.objects.get(id=case_form.cleaned_data['case_module'])
			case_version = TcVersion.objects.get(id=case_form.cleaned_data['case_version'])
			case_result = case_form.cleaned_data['case_result']
			case_assign = case_form.cleaned_data['case_assign']
			case_comment = case_form.cleaned_data['case_comment']
			#实例添加用例
			case = TcCase.objects.create(case_name=casename,tc_style=casestyle,tc_level=caselevel,tc_presetting=case_presetting,\
				tc_steps=case_steps,tc_module=case_module,tc_version=case_version,tc_except_result=case_result,\
				tc_comment=case_comment,tc_user=case_assign)
			case.save()
			return redirect(request.GET.get('from', reverse('testcases')))

	else:
		case_form = CaseForm()
	context = {}
	context['case_form'] = case_form
	return render(request,'add_testcase.html',context)

#查看用例详情
def get_case_detail(request,case_id):
	context = {}
	context['case_detail'] =get_object_or_404(TcCase,pk=case_id)
	return render(request,'case_detail.html',context)

#登录
def login(request):
	if request.method == 'POST':
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			user = login_form.cleaned_data['user']
			auth.login(request,user)
			return redirect(request.GET.get('from', reverse('versions')))
	else:
		login_form = LoginForm()
	context = {}
	context['login_form'] = login_form
	return render(request,'login.html',context)


#注册
def register(request):
	if request.method == 'POST':
		reg_form = RegForm(request.POST)
		if reg_form.is_valid():
		    username = reg_form.cleaned_data['username']
		    phone = reg_form.cleaned_data['phone']
		    password = reg_form.cleaned_data['password']
		    # 创建用户
		    user = User.objects.create_user(username, phone, password)
		    user.save()
		    # 登录用户
		    user = auth.authenticate(username=username, password=password)
		    auth.login(request, user)
		    return redirect(request.GET.get('from', reverse('versions')))
	else:
	    reg_form = RegForm()
	context = {}
	context['reg_form'] = reg_form
	return render(request, 'register.html', context)
