from django.urls import path
from . import views
from .views import RegisterEmployee, AddDesignation
urlpatterns = [
    path('employees/', views.getEmployee, name='getemployees'),
    path('employee/<nam>',views.getEmployeeOnName, name='emponname'),
    path('company-emp/<comp>', views.getCompanyEmployee, name='getcompantemp'),
    path('register/',  RegisterEmployee.as_view(), name='register'),
    path('designation/', AddDesignation.as_view(), name='designation'),
    path('update-emp/<emp>', views.updateOnPatch, name='update'),
    path('delete-emp/<emp>', views.deleteEmployee, name='deleteemp')
]