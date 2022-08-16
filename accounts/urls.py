from typing import ValuesView
from django.urls import path
from .views import RegisterView, LoginAPIView
from . import views
urlpatterns = [
    path('register/', RegisterView.as_view() , name= 'registration'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('userprofile/', views.getUserProfile, name='userprofile' ),
    path('userprofile/<pk>', views.getUserProfileOnId, name='userprofileid' ),
    path('allusers/', views.allUserProfile, name='allUsers'),
    path('logout/', views.logoutCall, name='logout'),
    path('adddepartment', views.addDepartment, name='adddepartment'),
    path('adddes/', views.addDesignation, name='adddesignation'),
    path('addproject/', views.addProjects, name='addprojects'),
]