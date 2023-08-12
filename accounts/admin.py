from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . models import User, Customer, Employee
from . forms import UserCreationForm, UserChangeForm

# Register your models here.

class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm

	list_display = ('email', 'name', 'mobile', 'first_name', 'last_name', 'date_birth', 'gender', 'avatar', 'is_staff', 'is_superuser', 'is_customer', 'is_employee')
	list_filter = ('is_superuser',)

	fieldsets = (
		(None, {'fields': ('email', 'is_staff', 'is_superuser', 'password')}),
		('Personal info', {'fields': ('name', 'mobile', 'first_name', 'last_name', 'date_birth', 'gender', 'avatar', 'is_customer','is_employee')}),
		('Groups', {'fields': ('groups',)}),
		('Permissions', {'fields': ('user_permissions',)}),
	)
	add_fieldsets = (
		(None, {'fields': ('email', 'is_staff', 'is_superuser', 'password1', 'password2')}),
		('Personal info', {'fields': ('name', 'mobile', 'first_name', 'last_name', 'date_birth', 'gender', 'avatar', 'is_customer', 'is_employee')}),
	)

	search_fields = ('email', 'name', 'mobile')
	ordering = ('email',)
	filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.register(Customer)
admin.site.register(Employee)

