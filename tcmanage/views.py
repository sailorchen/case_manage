from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import LoginForm,RegForm,CaseForm
from .models import TcVersion,TcModule,TcUser,TcCase

# Create your views here.

#登录装饰器
def check_login(func):
	def wrapper(request,*args,**kwargs):
		is_login = request.session.get('is_login',False)
		if is_login:
			return func(request,*args,**kwargs)
		else:
			return redirect(request.GET.get('from', reverse('login')))
	return wrapper

#获取所有的版本,搜索版本,需要登录
def get_version(request):
	context = {}
	version_form = request.GET.get('version_name')
	if version_form:
		search_version = TcVersion.objects.filter(version_name=version_form)
		context['search_version'] = search_version
	else:
		version_list = TcVersion.objects.all()
		paginator = Paginator(version_list,10)  #每10条1页
		page_num = request.GET.get('page',1)  #获取第一页
		page_of_versions = paginator.get_page(page_num)
		current_page_num = page_of_versions.number  #获得当前页
		range_page = list(range(max(current_page_num-2,1),current_page_num))+\
                list(range(current_page_num, min(current_page_num+2,paginator.num_pages)+1))
		if range_page[0]!=1:
			range_page.insert(0,1)
		if range_page[-1]!=paginator.num_pages:
			range_page.append(paginator.num_pages)
		if range_page[0]-1>=2:
			range_page.insert(0,'...')
		if paginator.num_pages-range_page[-1]>=2:
			range_page.append('...')
		context['page_of_versions']=page_of_versions
		context['versions'] = page_of_versions.object_list
		context['version_list'] = version_list
		context['range_page'] = range_page
	context['username'] = request.user.username
	return render(request,'versions.html',context)

#添加版本,需要登录
@check_login
def add_version(request):
	context = {}
	if request.method == 'GET':		
		return render(request,'add_version.html',context)
	elif request.method =='POST':
		version_name = request.POST.get('version_name',"")
		if version_name:
			context['version_name'] = version_name
			context['username'] = request.user.username
			add_version = TcVersion()
			add_version.version_name=version_name
			add_version.save()
			return redirect('versions')

			
#获取所有的模块,搜索模块,需要登录
@check_login
def get_module(request):
	context = {}
	context['username'] = request.user.username
	module_form = request.GET.get("module_name")
	if module_form:
		search_module = TcModule.objects.filter(module_name=module_form)
		context['search_module'] = search_module
	else:
		module_list = TcModule.objects.all()
		context['module_list'] = module_list
	return render(request,'models.html',context)

#添加模块,需要登录
@check_login
def add_module(request):
	context = {}
	context['username'] = request.user.username
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

#获取所有的测试用例,需要登录
@check_login
def get_testcase(request):
	context = {}
	context['username'] = request.user.username
	case_list = TcCase.objects.all()
	context['case_list'] = case_list
	return render(request,'testcases.html',context)


#添加用例,需要登录
@check_login
def add_testcase(request):
	context = {}
	context['username'] = request.user.username
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
	context['case_form'] = case_form
	return render(request,'add_testcase.html',context)

#查看用例详情,需要登录
@check_login
def get_case_detail(request,case_id):
	context = {}
	context['username'] = request.user.username
	case_detail = get_object_or_404(TcCase,pk=case_id)
	context['case_detail'] =case_detail
	return render(request,'case_detail.html',context)

#提交数据
def commit_result(request):
	if request.method=='POST':
		result = request.POST.get('resultradio')
		#更新测试结果
		case_id= request.POST.get('case_id')
		TcCase.objects.filter(pk=case_id).update(tc_actual_result=result)
	else:
		pass
	return redirect(request.GET.get('from', reverse('testcases')))

#登录
def login(request):
	context = {}
	if request.method == 'POST':
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			user = login_form.cleaned_data['user']
			auth.login(request,user)
			#添加session,跳转到versions
			request.session['is_login']=True
			request.session['username']=user.username
			return redirect(request.GET.get('from', reverse('versions')))
	else:
		login_form = LoginForm()
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
		    # 登录用户,添加session,跳转到versions
		    user = auth.authenticate(username=username, password=password)
		    auth.login(request, user)
		    request.session['is_login']=True
		    request.session['username']=user.username
		    return redirect(request.GET.get('from', reverse('versions')))
	else:
	    reg_form = RegForm()
	context = {}
	context['reg_form'] = reg_form
	return render(request, 'register.html', context)


#退出-->清除session,跳转到登录页面
def log_out(request):
	request.session.flush()
	auth.logout(request)
	return redirect(request.GET.get('from', reverse('login')))
