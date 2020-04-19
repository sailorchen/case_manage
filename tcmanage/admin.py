from django.contrib import admin
from .models import TcVersion,TcModule,TcUser,TcCase

# Register your models here.

@admin.register(TcVersion)
class TcAdminVersion(admin.ModelAdmin):
	list_display = ['id','version_name','create_time','update_time']

@admin.register(TcModule)
class TcAdminModule(admin.ModelAdmin):
	list_display = ['id','module_name','create_time','update_time']

@admin.register(TcCase)
class TcAdminCase(admin.ModelAdmin):
	list_display = ['id','case_name','tc_style','tc_level','tc_module','tc_version','tc_user']

@admin.register(TcUser)
class TcAdminUser(admin.ModelAdmin):
	list_display = ['id','username','password','phone','role','create_time','update_time']
