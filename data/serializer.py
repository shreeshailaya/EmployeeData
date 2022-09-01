from importlib.metadata import files
from rest_framework import serializers
from .models import Company, Department, Designation, Employee, UserProfile


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields ='__all__'

    def create(self, validated_data):
        return Designation.objects.create(**validated_data)

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class EmployeeSerializerGet(serializers.ModelSerializer):
    designation = serializers.CharField()
    department  = serializers.CharField()
    userProfile = serializers.StringRelatedField(many=True)
    company = serializers.CharField()

    class Meta:
        model = Employee
        fields = '__all__'



class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['department'] = instance.department.name
        response['designation'] = instance.designation.name
        response['company'] = instance.company.name
        #response['userProfile'] = EmployeeSerializerGet(instance.userProfile.all(), many=True).data
        response['userProfile'] = [UserProfile.objects.get(id=x).name for x in response['userProfile']]
        return response

     

    def create(self,attr):
        #print(attr)
        if 'userProfile' in attr:
            userP = attr.pop('userProfile')
            emp_profile = Employee.objects.create(**attr)
            emp_profile.userProfile.add(*userP)
        else:
            emp_profile = Employee.objects.create(**attr)
        return emp_profile

class EmployeeSerializerRegistration(serializers.ModelSerializer):
    designation = serializers.SlugRelatedField(queryset = Designation.objects.all(), allow_null = True  ,slug_field='name')
    department  = serializers.SlugRelatedField(queryset = Department.objects.all(),allow_null = True ,slug_field='name')
    userProfile = serializers.SlugRelatedField(many=True, queryset=UserProfile.objects.all(), slug_field='name')
    company = serializers.SlugRelatedField(queryset=Company.objects.all(), allow_null = True,slug_field='name')
    class Meta:
        model = Employee
        fields = '__all__'
    
    def create(self,attr):
        #print(attr)
        if 'userProfile' in attr:
            userP = attr.pop('userProfile')
            emp_profile = Employee.objects.create(**attr)
            emp_profile.userProfile.add(*userP)
        else:
            emp_profile = Employee.objects.create(**attr)
        return emp_profile
