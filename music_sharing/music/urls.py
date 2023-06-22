from django.urls import path
from . import views
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('upload/', views.upload_file, name='upload'),
]
    # path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    # the default login behavior provided by Django's authentication system. 
    # When a user tries to access a protected page without being authenticated, 
    # Django redirects them to the login page by default.
  