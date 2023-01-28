from django.contrib import admin
from users.models import NewUser
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea



class UserAdminConfig(UserAdmin):
	model = NewUser
	search_fields = ('email','first_name','last_name','gender')
	list_filter = ('email','first_name','last_name','gender','is_active','is_staff')
	ordering = ('-dob',)
	list_display=('email','first_name','last_name','gender','is_active','is_staff')

	fieldsets=(
			(None,{'fields':('email', 'first_name','last_name','gender','avatar','dob')}),
			('Permissions',{'fields':('is_staff','is_active','is_superuser','groups','user_permissions')}),
			('Personal',{'fields':('phone_number','about',)}),
		)

	formfield_overrides = {
		NewUser.about: {'widget': Textarea(attrs={'rows':10,'cols':40})},
	}

	add_fieldsets = (
	(None,{
		'classes':('wide',),
		'fields':('email','phone_number','first_name','last_name','gender','avatar','dob','password1','password2','is_active','is_staff','groups','user_permissions')
		}
		),
	)

admin.site.register(NewUser,UserAdminConfig)

# Register your models here.
