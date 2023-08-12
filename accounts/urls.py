from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	path('', views.customer_home, name='customer-home'),
	path('employee/', views.employee_home, name='employee-home'),
	path('admin/', views.admin_home, name='admin-home'),
	#path('login/', views.LoginView.as_view(), name='login'),
	path('login/', views.login_view, name='login'),
	#path('login/', views.auth_view, name='login'),
	path('verify/', views.verify_view, name='verify'),
	path('signup/customer/', views.CustomerSignUpView.as_view(), name='customer-signup'),
	path('signup/employee/', views.EmployeeSignUpView.as_view(), name='employee-signup'),
	path('main/', views.main_view, name='main-view'),
	path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
]