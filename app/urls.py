from django.urls import path
from . import views

urlpatterns = [
    path('', views.app_index, name="home"),
    path('index/', views.app_index, name="index"),
    path('add_bank/', views.add_bank, name="add-bank"),
    path('login_bank/<slug:bank_slug>', views.login_bank, name="login-bank"),
    path('bank/<uuid:link_id>', views.link_accounts, name='link-accounts'),
    path('bank/<uuid:link_id>/account/<uuid:account_id>', views.transactions, name='transactions'),

    path('page-error-404/', views.page_error_404, name="page-error-404"),
]
