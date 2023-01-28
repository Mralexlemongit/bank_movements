from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from users.models import NewUser
from users.forms import ( NewUserForm,
						  SignupForm,
						  LoginForm,
						  GroupForm,
						  PermissionsForm,
						  UserPermissionsForm,
						  EditUserForm,
						)
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required 
from django.contrib.auth.models import Group, Permission
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.contrib.contenttypes.models import ContentType

from django.core.paginator import Paginator

from django.core.mail import send_mail
from django.conf import settings
from users.tokens import account_activation_token
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect

from smtplib import SMTPSenderRefused, SMTPAuthenticationError

email_list = ['customer@example.com','manager@example.com','admin@example.com']

@login_required(login_url='login')
def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user,request.POST)
		if form.is_valid():
			user=form.save()
			update_session_auth_hash(request, user)
			messages.success(request,'Password Update Successfully')
			return redirect('/password/')
		else:
			messages.warning(request,'Form is not valid')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'users/change-password.html', {'form': form})


@login_required(login_url='login')
@permission_required({'users.view_newuser'}, raise_exception=True)
def users(request):
	context={
		"user_list": NewUser.objects.filter(is_superuser=False).order_by('groups__name')
	}
	print(context)
	return render(request, "mophy/modules/users.html",context)

@login_required(login_url='login')
@permission_required({'users.view_newuser'}, raise_exception=True)
def user_details(request,id):
	user_obj=get_object_or_404(NewUser,id=id)

	context={
		"user_obj":user_obj,
		"user_group_perms":user_obj.get_group_permissions(),
		"user_perms":user_obj.get_user_permissions()
	}


	return render(request,"mophy/modules/user-details.html",context)


@login_required(login_url='login')
@permission_required({'users.view_newuser','users.delete_newuser'},raise_exception=True)
def delete_user(request,id):
	u = NewUser.objects.get(id=id)
	u.delete()
	messages.success(request, "User deleted successfully") 
	return redirect('users')

@login_required(login_url='login')
@permission_required({'users.view_newuser','users.add_newuser'},raise_exception=True)
def add_user(request):
	if request.method == 'POST':
		form = NewUserForm(request.POST, request.FILES)
		if form.is_valid():
			user_obj = form.save()
			user_obj.groups.clear()
			for i in form.cleaned_data.get('groups'):
				user_obj.groups.add(i)
			messages.success(request,f'{user_obj.first_name} {user_obj.last_name} is created successfully')
			return redirect('users')
	else:
		form = NewUserForm()
	return render(request, 'mophy/modules/add-user.html', {'form': form})


def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user_obj = form.save(commit=False)
			user_obj.is_active = False
			user_obj.save()
			# Default Group assign Start -------------------------------------------------------
			if Group.objects.filter(name='Customer'):
				user_obj.groups.add(Group.objects.filter(name='Customer')[0])

			else:
				Customer_group, created = Group.objects.get_or_create(name="Customer")
				content_type = ContentType.objects.get_for_model(NewUser)
				NewUser_permission = Permission.objects.filter(content_type=content_type)
				for perm in NewUser_permission:
					if perm.codename == "view_newuser":
						Customer_group.permissions.add(perm)
				user_obj.groups.add(Customer_group)

			# Default Group assign End-----------------------------------------------------------
			current_site = get_current_site(request)
			subject = 'Activa tu cuenta en Bank Movements'
			message = render_to_string('users/account_activation_email.html', {
					'user': user_obj,
					'domain': current_site.domain,
					'uid': urlsafe_base64_encode(force_bytes(user_obj.pk)),
					'token': account_activation_token.make_token(user_obj),
			})
			email = form.cleaned_data.get('email')
			name = form.cleaned_data.get('first_name')
			ReceiversList = [email]
			EmailSender = settings.EMAIL_HOST_USER
			try:
				send_mail(subject, message, EmailSender, ReceiversList, fail_silently=False)
				if user_obj.is_active == False:
					messages.success(request, 'Finaliza tu registro ingresando a la liga que enviamos a tu correo electronico.', 'Registro Exitoso')
				return redirect('signup')
			except (SMTPSenderRefused, SMTPAuthenticationError):
				print("Favor de configurar el email del sistema.")
				messages.error(request,"Comunicar a soporte.", "Problemas con el registro")
				user_obj.delete()
			except:
				messages.error(request,'Comunicar a soporte.', "Problemas con el registro")
				user_obj.delete()
		else:
			messages.warning(request,"Favor de verificar el registro.", "Tarea no concluida")
	else:
		if request.user.is_authenticated:
			return redirect('index')
		form = SignupForm()
	return render(request, 'users/signup.html', {'form': form})


def activate(request, uidb64, token):
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = NewUser.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, NewUser.DoesNotExist):
		user = None

	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		login(request, user)
		messages.success(request, 'Disfruta ahora de el mejor servicio de análisis financiero cuántico.', 'Registro Finalizado.')
		return redirect('index')
	else:
		return render(request, 'users/account_activation_invalid.html')


@login_required(login_url='login')
@permission_required({'users.view_newuser','users.change_newuser'}, raise_exception=True)
def edit_user(request,id):
	user_obj = get_object_or_404(NewUser,id=id)
	if request.method == 'POST':
		form = EditUserForm(request.POST, request.FILES, instance=user_obj)
		if form.is_valid():
			user_obj = form.save()
			user_obj.groups.clear()
			for i in form.cleaned_data['groups']:
				user_obj.groups.add(i)
			return redirect('users')
	else:
		form = EditUserForm(instance=user_obj)
		print(form)
	return render(request, 'mophy/modules/add-user.html', {'form': form})

def login_user(request):
	message=''
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			user=form.login(request)
			if user is not None and user.is_active:
				login(request, user)
				usergroup = ','.join(request.user.groups.values_list('name',flat = True))
				messages.success(request, f'Bienvenido')
				next_url = request.GET.get('next')
				if next_url:
					return HttpResponseRedirect(next_url)
				else:
					return redirect('index')
			else:
				messages.warning(request,'User is Not Active')	
				
		else:
			messages.warning(request,"Favor de verificar usuario y contraseña.")
			return render(request, 'users/login.html', context={'form': form})
	else:
		if request.user.is_authenticated:
			return redirect('index')
		form = LoginForm()
	return render(request, 'users/login.html', context={'form': form})

def logout_user(request):
	logout(request)
	messages.success(request,'Sesión cerrada exitosamente.')
	return redirect('login')


@login_required(login_url='login')
@permission_required({'auth.view_group'}, raise_exception=True)
def groups_list(request):
	context={
		"groups":Group.objects.annotate(user_count=Count('newuser',distinct=True)).annotate(perms_count=Count('permissions',distinct=True)),
		"colors":{'primary':'primary','success':'success','dark':'dark'}
	}
	return render(request, 'mophy/modules/group-list.html', context)

@login_required(login_url='login')
@permission_required({'auth.view_group','auth.change_group'}, raise_exception=True)
def group_edit(request,id):
	group_obj = get_object_or_404(Group,id=id)

	if request.method == 'POST':
		queryDict = request.POST
		data = dict(queryDict)

		try:
			group_obj.name = data['name'][0]
			group_obj.save()
		except:
			response = JsonResponse({"error": "Group Name already exist"})
			response.status_code = 403
			return response

		if 'permissions[]' in data:
			group_obj.permissions.clear()
			group_obj.permissions.set(data['permissions[]'])
		else:
			group_obj.permissions.clear()

	
		response = JsonResponse({"success": "Save Successfully"})
		response.status_code = 200
		return response

	else:
		form = GroupForm(instance=group_obj)
	return render(request, 'mophy/modules/group-edit.html',{'form': form})

@login_required(login_url='login')
@permission_required({'auth.view_group','auth.delete_group'}, raise_exception=True)
def group_delete(request,id):
	g=get_object_or_404(Group,id=id)

	g.delete()
	messages.success(request,'Group Deleted Sucessfully')
	
	return redirect('groups')

@login_required(login_url='login')
@permission_required({'auth.view_group','auth.add_group'}, raise_exception=True)
def group_add(request):
	if request.method == 'POST':
		form = GroupForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,'Group Created Successfully')
			return redirect('groups')
		else:
			messages.warning(request,'Name Already Exist')
			return render(request, 'mophy/modules/group-add.html',{'form': form})
	else:
		form = GroupForm()
		return render(request, 'mophy/modules/group-add.html',{'form': form})

@login_required(login_url='login')
@permission_required({'auth.view_permission'}, raise_exception=True)
def permissions(request):

	permission_list = Permission.objects.all()

	paginator = Paginator(permission_list, 5) # Show 5 permission per page.
	context={
		"permissions_obj" : paginator.get_page(request.GET.get('page')),
	}
	
	return render(request, 'mophy/modules/permissions.html',context)

@login_required(login_url='login')
@permission_required({'auth.view_permission','auth.change_permission'}, raise_exception=True)
def edit_permissions(request,id):
	perm_obj = get_object_or_404(Permission,id=id)
	if request.method == 'POST':
		form = PermissionsForm(request.POST,instance=perm_obj)

		if form.is_valid():
			form.save()
			return redirect('permissions')
	else:
		form = PermissionsForm(instance=perm_obj)
		return render(request, 'mophy/modules/edit-permissions.html',{'form': form})

@login_required(login_url='login')
@permission_required({'auth.view_permission','auth.delete_permission'}, raise_exception=True)
def delete_permissions(request,id):
	perm_obj = get_object_or_404(Permission,id=id)
	perm_obj.delete()
	messages.success(request,'Permission Delete Successfully')
	return redirect('permissions')

@login_required(login_url='login')
@permission_required({'auth.view_permission','auth.add_permission','auth.change_permission'}, raise_exception=True)
def assign_permissions_to_user(request,id):
	user_obj = get_object_or_404(NewUser,id=id)
	if request.method == 'POST':
		queryDict = request.POST
		data = dict(queryDict)
		
		if 'user_permissions[]' in data:
			user_obj.user_permissions.clear()
			user_obj.user_permissions.set(data['user_permissions[]'])
		else:
			user_obj.user_permissions.clear()
		response = JsonResponse({"success": "Save Successfully"})
		response.status_code = 200
		return response


	else:
		form = UserPermissionsForm(instance=user_obj)
	return render(request, 'mophy/modules/assign_permissions_to_user.html',{'form':form})
