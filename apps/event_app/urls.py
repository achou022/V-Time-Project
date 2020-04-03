from django.urls import path
from . import views

app_name = 'event'

urlpatterns=[
    path('event/register/menu', views.registerMenu, name='register_menu'),
    path('event/register', views.register, name='register'),
    path('event/edit/menu/<int:event_id>', views.editMenu, name='editMenu'),
    path('event/<int:eventID>/job/signup/menu', views.jobMenu, name='jobMenu'),
    path('event/<int:eventID>/job/signup', views.jobSignUp, name='jobSignUp'),
    path('event/edit/<int:event_id>', views.edit, name='edit'),
    path('event/splash', views.eventSplash, name="splash"),
    path('event/dashboard/<int:event_id>', views.eventDashboard, name="dashboard"),
    path('event/<int:eventID>/new/post', views.newPost, name="newPost"),
    path('event/post/<int:postID>/new/comment', views.newComment, name="newComment"),
    path('event/<int:eventID>/user/signup', views.jobSignUp, name='signup'),
    path('event/<int:eventID>/delete_job/<int:jobID>', views.deleteJob, name='delete_job')
]