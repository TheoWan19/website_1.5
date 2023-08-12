from django import forms
from django.db import transaction
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


from .models import User, Customer, Employee

class RegistrationForm(forms.ModelForm):
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	
	class Meta:
		model = User
		fields = ('email', 'name', 'mobile', 'first_name', 'last_name', 'date_birth', 'gender', 'avatar', 'password')
		widgets = {
			'date_birth': forms.DateInput(attrs={'type': 'date'}),
			'mobile': PhoneNumberPrefixWidget(initial='US'),
		}

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password'])
		if commit:
			user.save()
		return user
		
class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email', 'name', 'mobile', 'first_name', 'last_name', 'date_birth', 'gender', 'avatar', 'is_staff', 'is_superuser')

		def clean_password2(self):
			password1 = self.cleaned_data.get('password1')
			password2 = self.cleaned_data.get('password2')	
			if password1 and password2 and password1 != password2:
				raise forms.ValidationError("Password don't match")
			return password2
			
		def save(self, commit=True):
			user = super().save(commit=False)
			user.set_password(self.cleaned_data['password1'])
			if commit:
				user.save()
			return user
			
class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User
		fields = ('email', 'name', 'mobile', 'first_name', 'last_name', 'date_birth', 'gender', 'avatar', 'password', 'is_staff', 'is_superuser')	

	def clean_password(self):
		return self.initial['password']	

class CustomerSignUpForm(UserCreationForm):

	MALE = 'MALE'
	FEMALE = 'FEMALE'

	GENDER_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
	)

	email = forms.EmailField(widget=forms.EmailInput())
	name = forms.CharField(widget=forms.TextInput())
	#mobile = PhoneNumberField()
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
	password2 = forms.CharField(label='Password Confirm', widget=forms.PasswordInput())

	first_name = forms.CharField(widget=forms.TextInput())
	last_name = forms.CharField(widget=forms.TextInput())
	#date_birth = forms.DateField()
	gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES)
	avatar = forms.ImageField()
	location = forms.CharField(widget=forms.TextInput())
	is_customer = forms.BooleanField()
	is_employee = forms.BooleanField()	

	class Meta:
		model = User
		fields = ('email', 'name', 'mobile', 'date_birth', 'first_name', 'last_name', 'gender', 'avatar', 'location', 'is_customer', 'is_employee', 'password1', 'password2')
		widgets = {
			'date_birth': forms.DateInput(attrs={'type': 'date'}),
			'mobile': PhoneNumberPrefixWidget(initial='US'),
		}

	@transaction.atomic
	def save(self, commit=True):
		user = super().save(commit=False)
		user.is_customer = True
		if commit:
			user.save()
		customer = Customer.objects.create(user=user, name=self.cleaned_data.get('name'), mobile=self.cleaned_data.get('mobile'), first_name=self.cleaned_data.get('first_name'), last_name=self.cleaned_data.get('last_name'), date_birth=self.cleaned_data.get('date_birth'), gender=self.cleaned_data.get('gender'), avatar=self.cleaned_data.get('avatar'), location=self.cleaned_data.get('location'), is_customer=self.cleaned_data.get('is_customer'), is_employee=self.cleaned_data.get('is_employee'))
		return user

class EmployeeSignUpForm(UserCreationForm):

	MALE = 'MALE'
	FEMALE = 'FEMALE'

	GENDER_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
	)

	email = forms.EmailField(label='Email Address', widget=forms.EmailInput())	
	name = forms.CharField(label='Name', widget=forms.TextInput())
	#mobile = PhoneNumberField()
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
	password2 = forms.CharField(label='Password Confirm', widget=forms.PasswordInput())

	first_name = forms.CharField(widget=forms.TextInput())
	last_name = forms.CharField(widget=forms.TextInput())
	#date_birth = forms.DateField()
	gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES)
	avatar = forms.ImageField(label='Avatar')
	nif = forms.CharField(widget=forms.TextInput())
	cin = forms.CharField(widget=forms.TextInput())
	location = forms.CharField(widget=forms.TextInput())
	designation = forms.CharField(widget=forms.TextInput())
	is_employee = forms.BooleanField()	

	class Meta:
		model = User
		fields = ('email', 'name', 'mobile', 'password1', 'password2', 'date_birth', 'mobile')

		widgets = {
			'date_birth': forms.DateInput(attrs={'type': 'date'}),
			'mobile': PhoneNumberPrefixWidget(initial='US'),
		}

	@transaction.atomic
	def save(self, commit=True):
		user = super().save(commit=False)
		user.is_employee = True
		if commit:
			user.save()
		employee = Employee.objects.create(user=user, name=self.cleaned_data.get('name'), mobile=self.cleaned_data.get('mobile'), first_name=self.cleaned_data.get('first_name'), last_name=self.cleaned_data.get('last_name'), date_birth=self.cleaned_data.get('date_birth'), gender=self.cleaned_data.get('gender'), avatar=self.cleaned_data.get('avatar'), nif=self.cleaned_data.get('nif'), cin=self.cleaned_data.get('cin'), location=self.cleaned_data.get('location'), designation=self.cleaned_data.get('designation'), is_employee=self.cleaned_data.get('is_employee'))
		return user		

class LoginForm(AuthenticationForm):
	email = forms.CharField(widget=forms.TextInput())
	password = forms.CharField(widget=forms.PasswordInput())


class ProfileForm(forms.ModelForm):
	
	email = forms.EmailField(label='Email Address', widget=forms.EmailInput())	

	class Meta:
		model = User
		fields = ('email', 'name', 'mobile', 'first_name', 'last_name', 'date_birth', 'gender', 'avatar')
		widgets = {
			'date_birth': forms.DateInput(attrs={'type': 'date'}),
			'mobile': PhoneNumberPrefixWidget(initial='US'),
		}

		def save(self, commit=True):
			user = super().save(commit=False)
			user.set_email(self.cleaned_data['email'])
			if commit:
				user.save()
			return user
