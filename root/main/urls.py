from django.urls import path
from . import  views
from .views import register

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('work/<int:id>', views.work, name='work'),
    path('workapi/<int:id>', views.workapi, name='workapi'),
    path('works/<int:id>', views.works, name='works'),
    path('contact', views.contact, name='contact'),
    path('registor_file', views.registor_file, name='registor_file'),
    path('success', views.success, name='success'),
    path('login', views.login, name='login'),
    path('password_save', views.password_save, name='password_save'),
    path('admin_page', views.admin_page, name='admin_page'),
    path('user_page', views.user_page, name='user_page'),
    path('messag_user', views.message_user, name='messag_user'),
    path('registor', register, name='rcxt'),
]