from django.urls import path
from . import views

urlpatterns = [
    path('versions', views.get_version,name='versions'),
    path('add_version',views.add_version,name='add_version'),
    path('models',views.get_module,name='models'),
    path('add_module',views.add_module,name='add_module'),
    path('testcases',views.get_testcase,name='testcases'),
    path('add_testcase',views.add_testcase,name='add_testcase'),
    path('testcases/<int:case_id>', views.get_case_detail,name='case_detail'),
    path('login', views.login,name='login'),
    path('register', views.register,name='register'),
]