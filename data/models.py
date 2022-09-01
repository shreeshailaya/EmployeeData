from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "company"

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "department"

    def __str__(self):
        return self.name+ ' => ' + str(self.company)

class UserProfile(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "userprofile"

    def __str__(self):
        return self.name

class Designation(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "designation"

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    email = models.EmailField(blank=True)
    salary = models.IntegerField( null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    userProfile = models.ManyToManyField(UserProfile, blank=True)
    designation = models.OneToOneField(Designation, default=None, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    class Meta:
        verbose_name_plural = "employee"

    def __str__(self):
        return str(self.name)

