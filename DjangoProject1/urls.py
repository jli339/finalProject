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

# Assigning url for each site

urlpatterns = [
    path('', views.login, name='login'),
    path('admin/', admin.site.urls),
    path('login/',views.login,name='login'),
    path('index/',views.index, name='index'),

    path('predict/', views.predict_view, name='predict_priority'),
    # path('dbtest/',views.get_credential),

    path('unassigned/', views.unassigned_list, name='unassigned_list'),
    path('predict_unassigned/<int:task_id>/', views.predict_unassigned, name='predict_task'),

    path('assigned/',views.assigned_list, name='assigned_list'),

    path('assigned_view/<int:task_id>/', views.assigned_view, name='assigned_view'),

    path('historical/',views.historical_list,name='historical_list'),


]
