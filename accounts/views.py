from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views
from django import forms

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse

from . models import User
from . forms import RegistrationForm, ProfileForm, CustomerSignUpForm, EmployeeSignUpForm, LoginForm
from . decorators import customer_required, employee_required, admin_required
from codes.forms import CodeForm
from . utils import send_sms

# Create your views here.

class RegistrationView(CreateView):
	template_name = 'registration/register.html'
	form_class = RegistrationForm

	def get_context_data(self, *args, **kwargs):
		context = super(RegistrationView, self).get_context_data(*args, **kwargs)
		context['next'] = self.request.GET.get('next')
		return context

	def get_success_url(self):
		next_url = self.request.POST.get('next')
		success_url = reverse('login')
		if next_url:
			success_url += '?next={}'.format(next_url)

		return success_url

class CustomerSignUpView(CreateView):
	model = User
	form_class = CustomerSignUpForm
	template_name = 'accounts/customer_signup.html'

	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 'student'
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return redirect('student-home')	


class EmployeeSignUpView(CreateView):
	model = User
	form_class = EmployeeSignUpForm
	template_name = 'accounts/employee_signup.html'

	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 'employee'
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return redirect('employee-home')

'''
class LoginView(auth_views.LoginView):
	form_class = LoginForm
	template_name = 'accounts/login.html'

	def get_context_data(self, **kwargs):
		return super().get_context_data(**kwargs)

	def get_success_url(self):
		user = self.request.user
		if user.is_authenticated:
			if user.is_customer:
				return reverse('customer-home')
			elif user.is_employee:
				return reverse('employee-home')	
			elif user.is_superuser:
				return reverse('admin-home')	
		else:
			return reverse('login')	
'''				

		
class ProfileView(UpdateView):

	template_name = 'registration/profile.html'
	form_class = ProfileForm

	def get_success_url(self):
		return reverse('home')	

	def get_object(self):
		return self.request.user	

@login_required
@customer_required
def customer_home(request):
	context = {}
	return render(request, 'accounts/customer_home.html', context)


@login_required
@employee_required
def employee_home(request):
	context = {}
	return render(request, 'accounts/employee_home.html', context)	

@login_required
@admin_required
def admin_home(request):
	context = {}
	return render(request, 'accounts/admin_home.html', context)	


def login_view(request):
	error_message = None
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(request, email=email, password=password)
		if user is not None:
			request.session['pk'] = user.pk
			return redirect('verify')
		else:
			error_message = 'Invalid email or password'	
	return render(request, 'accounts/login.html', {'error_message': error_message})	
	
	
'''
def auth_view(request):
	error_message = None
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(request, email=email, password=password)
		if user is not None:
			request.session['pk'] = user.pk
			return redirect('verify')
	return render(request, 'accounts/auth.html')
'''

def verify_view(request):
	form = CodeForm(request.POST or None)
	pk = request.session.get('pk')
	if pk:
		user = User.objects.get(pk=pk)
		code = user.code
		code_user = f'{user.email}: {code}'
		if not request.POST:
			print(code_user)
			send_sms(code_user, user.mobile)
		if form.is_valid():
			num = form.cleaned_data.get('number')	

			if str(code) == num:
				code.save()
				login(request, user)
				return redirect('main')
			else:
				return redirect('login')	
	return render(request, 'accounts/verify.html', {'form': form})			

@login_required
@admin_required	
@employee_required
@customer_required
def main_view(request):	
	return redirect('main')		

