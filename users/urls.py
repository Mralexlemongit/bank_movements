from django.urls import path
from django.contrib.auth import views as auth_views

from users import users_views
from users.forms import EmailValidationOnForgotPassword

urlpatterns = [
	path('activate/<uidb64>/<token>/',users_views.activate, name='activate'),
    path('change_password/', users_views.change_password, name='change_password'),
    path('login/', users_views.login_user, name="login"),
	path('logout/',users_views.logout_user,name="logout"),
    path(
        'reset_password/',
        auth_views.PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword),
        name='reset_password'
    ),
    path('signup/',users_views.signup, name="signup"),
	path('users/',users_views.users, name="users"),
    path('password/', users_views.change_password, name='change_password'),
]
