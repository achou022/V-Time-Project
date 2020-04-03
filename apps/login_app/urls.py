from django.urls import path
from . import views

app_name = 'login'
urlpatterns=[
    path('', views.landingPage),
    path('login/menu', views.loginMenu),
    path('login', views.login),
    path('register/menu', views.registerMenu, name='register'),
    path('register', views.register),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/<int:adminID>/admin', views.adminDashboard, name='admin_dashboard'),
    path('profile/<int:userID>', views.profile, name='profile'),
    path('edit/menu', views.editMenu, name="editMenu"),
    path('edit', views.edit, name="edit"),
    path('logout', views.logout),
    path('getNavBar', views.getNavBar),
    path('generate', views.generate)
    # path('users/<int:userID>', views.user),
]