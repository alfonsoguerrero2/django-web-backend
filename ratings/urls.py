"""
URL configuration for webServices project.

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

from django.urls import path
from .views import register, login, logout, register, professor_avg
from .views import modules, professor_ratings, rating
urlpatterns = [
    path('students/register', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('modules/',modules, name='modules'),
    path('professors_ratings/', professor_ratings, name='professor_ratings'),
    path('professor_avg/professor/<str:professor_id>/module/<str:module_code>/', professor_avg, name='professor_avg'),
    path('rating/', rating, name='rating'),
]
