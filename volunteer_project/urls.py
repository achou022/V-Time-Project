from django.urls import path, include

urlpatterns = [
    path('', include('apps.login_app.urls')),
    path('', include('apps.company_app.urls')),
    path('', include('apps.event_app.urls')),
]
