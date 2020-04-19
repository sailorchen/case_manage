from django.db import models

# Create your models here.

class TcVersion(models.Model):
	#版本名称
	version_name = models.CharField(max_length=20,verbose_name='版本名称',unique=True)
	create_time = models.DateField(verbose_name='创建时间',auto_now_add=True)
	update_time = models.DateTimeField(verbose_name='更新时间',auto_now=True)

	def __str__(self):
		return self.version_name

	class Meta:
		ordering = ['-create_time']

class TcModule(models.Model):
	#模块名称
	module_name = models.CharField(max_length=20,verbose_name='模块名称',unique=True)
	create_time = models.DateField(verbose_name='创建时间',auto_now_add=True)
	update_time = models.DateTimeField(verbose_name='更新时间',auto_now=True)

	def __str__(self):
		return self.module_name

	class Meta:
		ordering = ['-create_time']


class TcCase(models.Model):
	#测试用例名称
	case_name = models.CharField(max_length=50,verbose_name='用例名称')
	#用例类型 【UI、功能、性能】
	styles = (('UI','UI'),('Function','功能'),('Perfermance','性能'),)
	tc_style = models.CharField(verbose_name='用例类型',max_length=20,choices=styles,default='Function')
	#用例等级 【冒烟、level1,level2,level3】
	levels = (('SMOKING','冒烟'),('Function','LEVEL0'),('LEVEL1','LEVEL1'),('LEVEL2','LEVEL2'),)
	tc_level = models.CharField(verbose_name='用例等级',max_length=20,choices=levels,default='SMOKING')
	#前置条件
	tc_presetting = models.TextField(verbose_name='前置条件',blank=True)
	#测试步骤
	tc_steps = models.TextField(verbose_name='用例步骤')
	#关联模块
	tc_module = models.ForeignKey('TcModule',on_delete=models.DO_NOTHING,related_name='module')
	#关联版本
	tc_version = models.ForeignKey('TcVersion',on_delete=models.DO_NOTHING,related_name='version')
	#期望结果
	tc_except_result = models.TextField(verbose_name='期望结果')
	#测试结果 【pass、fail、block、na,】
	results = (('PASS','通过'),('FAIL','失败'),('BLOCK','阻塞'),('NA','无法测试'),('NotTest','未测试'))
	tc_actual_result = models.CharField(verbose_name='实际结果',max_length=20,choices=results,default='NotTest')
	#备注
	tc_comment = models.TextField(verbose_name='备注显示')
	#指派测试人
	tc_user = models.CharField(verbose_name='分配人',max_length=20)
	create_time = models.DateField(verbose_name='创建时间',auto_now_add=True)
	update_time = models.DateTimeField(verbose_name='更新时间',auto_now=True)

	class Meta:
		ordering = ['-create_time']
		
	def __str__(self):
		return self.case_name

class TcUser(models.Model):
	role = ((0,'普通用户'),(1,'管理员'),)
	username = models.CharField(max_length=20,verbose_name='用户名',unique=True)
	password = models.CharField(max_length=20,verbose_name='密码')
	#设置管理员和普通账号
	role = models.IntegerField(verbose_name='角色',choices=role)
	phone = models.CharField(verbose_name='手机号',max_length=20)
	create_time = models.DateField(verbose_name='创建时间',auto_now_add=True)
	update_time = models.DateTimeField(verbose_name='更新时间',auto_now=True)

	def __str__(self):
		return self.username


