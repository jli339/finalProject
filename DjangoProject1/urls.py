"""
URL configuration for DjangoProject1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from FinalProject import views

from django.contrib.auth import views as auth_views
# urls.py
# This file defines the URL routing configuration for the Django project.
# It maps URL patterns to views, determining how the application responds to different requests.

urlpatterns = [

    path('',views.index),
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('index/',views.index, name='index'),


    path('predict/', views.predict_view, name='predict_priority'),
    # path('dbtest/',views.get_credential),

    path('unassigned/', views.unassigned_list, name='unassigned_list'),

    path('add_unassigned_task/', views.add_unassigned_task, name='add_unassigned_task'),

    path('predict_unassigned/<int:task_id>/', views.predict_unassigned, name='predict_task'),

    path('assigned/',views.assigned_list, name='assigned_list'),

    path('assigned_view/<int:task_id>/', views.assigned_view, name='assigned_view'),

    path('historical/',views.historical_list,name='historical_list'),

    path('delete_task/<int:task_id>/', views.delete_unassigned_task, name='delete_task'),

    path('update_task/<int:task_id>/', views.update_unassigned_task, name='update_task'),

]
