from dataclasses import fields
from rest_framework.authtoken.models import Token
from django.contrib import auth
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import Department, Designation, Profile, Projects

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6,write_only=True)

    repeat_password = serializers.CharField(write_only=True)



    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
            'repeat_password',
            'first_name',
            'last_name', 
            
        ]
        depth = 1
    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        password1 = attrs.get('password', '')
        password2 = attrs.get('repeat_password', '')

        if password1 != password2:
            raise serializers.ValidationError(
                'Password dont match'
            )

        if username.isalnum():
            raise serializers.ValidationError(
                'The username and Email is not same entered')
        return attrs
'''

    def create(self, validated_data):
        validated_data.pop('repeat_password')
        return User.objects.create_user(**validated_data)
'''

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = [
            'user',
            'image',
            'salary',
            'experience',
            'designation',
            'department',
            'project'
        ]


    def create(self, validate_data): 
        user_data = validate_data.pop('user')
        user_data.pop('repeat_password')
        user = User.objects.create(**user_data)
        projects_pop = validate_data.pop('project')
        profile_ = Profile.objects.create(user = user, **validate_data)
        profile_.project.add(*projects_pop)
        return profile_



class LoginSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=255, min_length=3,)

    class Meta:
        model = User
        fields = ['id','username','password']

    def generateToken(self, obj):
        is_tokened = Token.objects.filter(user=obj)
        if(is_tokened):
            token = Token.objects.get(user=obj)
            return {
                "token":token.key
            }
        else:
            token = Token.objects.create(user=obj)
            return {
                "token":token.key
            }
    def validate(self, attrs):
        username = attrs.get('username','')
        password = attrs.get('password', '')

        user = auth.authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed('User name or password is invalid')
        
        return{
            'username': user.username,
            'password':user.password,
        }


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = [
            'user',
            'image',
            'salary',
            'experience',
            'designation',
            'department',
            'project'
        ]

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

    def create(self,attrs):
        return Department.objects.create(**attrs)


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = [
            'name',
            'department'
        ]

    def create(self,attrs):
        return Designation.objects.create(**attrs)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'

    def create(self,attrs):
        return Projects.objects.create(**attrs)