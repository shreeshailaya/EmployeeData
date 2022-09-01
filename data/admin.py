from django.contrib import admin
from .models import Company,Department, Designation,Employee,UserProfile

admin.site.register(Company)
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(UserProfile)
admin.site.register(Designation)
