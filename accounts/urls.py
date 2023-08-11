from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	path('', views.customer_home, name='customer-home'),
	path('employee/', views.employee_home, name='employee-home'),
	path('admin/', views.admin_home, name='admin-home'),
	path('login/', views.LoginView.as_view(), name='login'),
	path('signup/customer/', views.CustomerSignUpView.as_view(), name='customer-signup'),
	path('signup/employee/', views.EmployeeSignUpView.as_view(), name='employee-signup'),
	path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
]