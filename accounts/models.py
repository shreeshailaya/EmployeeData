from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Designation(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

class Projects(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    
    
    def __str__(self):
        return '{}-{}'.format(
            self.name,
            self.description,
        )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    salary = models.IntegerField()
    experience = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    project = models.ManyToManyField(Projects, related_name='profile')

    
    def __str__(self):
        return str(self.user)