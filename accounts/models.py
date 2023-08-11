from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth import get_user_model
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from . managers import UserManager

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):

	MALE = 'MALE'
	FEMALE = 'FEMALE'

	GENDER_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
	)

	email = models.EmailField(unique=True)
	name = models.CharField(max_length=120)
	mobile = PhoneNumberField(unique=True)
	first_name = models.CharField(max_length=120)
	last_name = models.CharField(max_length=120)
	date_birth = models.DateField(blank=True, null=True)
	gender = models.CharField(max_length=6, choices=GENDER_CHOICES, verbose_name='Gender')
	is_staff = models.BooleanField(default=False)
	is_customer = models.BooleanField(default=True)
	is_employee = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
	date_joined = models.DateTimeField(default=timezone.now)
	last_login = models.DateTimeField(null=True)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name', 'mobile']


	def get_full_name(self):
		return f'{self.first_name }{self.last_name}'.title()

	def get_short_name(self):
		return self.name.split()[0]	

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='customer')
	location = models.CharField(max_length=150)
	is_customer = models.BooleanField(default=True)
	is_employee = models.BooleanField(default=True)	


class Employee(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='employee')
	nif = models.CharField(max_length=10, unique=True)
	cin = models.CharField(max_length=10, unique=True)
	is_employee = models.BooleanField(default=True)	
	location = models.CharField(max_length=150)
	designation = models.CharField(max_length=150)

