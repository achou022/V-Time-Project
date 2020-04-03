from django.urls import path
from . import views

app_name = 'company'

urlpatterns=[
    path('company/register/menu', views.registerMenu, name="registerMenu"),
    path('company/register', views.newCompany, name="register"),
    path('company/splash', views.companySplash, name="splash"),
    path('company/edit/menu/<int:company_id>', views.editCompanyMenu, name="editMenu"),
    path('company/edit/<int:company_id>', views.editCompany, name="edit"),
    path('company/profile/<int:companyID>', views.profile, name='profile')
]