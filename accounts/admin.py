import profile
from django.contrib import admin
from .models import Profile, Department,Designation, Projects
from django_reverse_admin import ReverseModelAdmin
import nested_admin
# Register your models here.

class ProfileAdmin(ReverseModelAdmin):
    inline_type = 'tabular'
    inline_reverse = [
                      ('user', {'fields': ['username', 'email', 'first_name', 'last_name']}),
                      'designation', 'salary'
                      ]
admin.site.register(Profile, ProfileAdmin)

class ProfileInline(nested_admin.NestedTabularInline):
    model = Profile
    extra = 0

class DepartmentAdmin(nested_admin.NestedModelAdmin):
    inlines = [ProfileInline, ]

admin.site.register(Department, DepartmentAdmin)

admin.site.register(Designation)
admin.site.register(Projects)


    