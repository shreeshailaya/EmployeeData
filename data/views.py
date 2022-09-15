from urllib import response
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializer import DesignationSerializer, EmployeeSerializer, EmployeeSerializerGet, EmployeeSerializerRegistration
from .models import Company, Department, Designation, Employee, UserProfile
from rest_framework import generics,status


# Create your views here.
@api_view(['GET'])
def getEmployee(request):
    instance = Employee.objects.all()
    serializers = EmployeeSerializerGet(instance, many=True)
    return Response(serializers.data,status.HTTP_200_OK)

@api_view(['GET'])
def getEmployeeOnName(request,nam):
    try:
        instance = Employee.objects.get(name = nam)
        serializer = EmployeeSerializerGet(instance)
        return Response(serializer.data, status.HTTP_200_OK)
    except Employee.DoesNotExist:
        data = {
            "Error": "Employee Not Found"
        }
        return Response( data, status.HTTP_400_BAD_REQUEST)

#re
class RegisterEmployee(generics.GenericAPIView):
    serializer_class = EmployeeSerializerRegistration
    def has_numbers(self,inputString):
        return any(char.isdigit() for char in inputString)
    def lowercase_machine(self, inputString):
        return inputString.lower()
    err_data = {
                "error": "values should not contain numbers in it"
            }
    def post(self, request):
        employee = request.data
        if 'name' not in employee:
            return Response({"error": "Name should be there"}, status.HTTP_400_BAD_REQUEST)


        employee['name'] = self.lowercase_machine(employee['name'])
        emp_exists = Employee.objects.filter(name = employee['name']).exists()
        if emp_exists:
            return Response({"error": "Employee is already exists"}, status.HTTP_406_NOT_ACCEPTABLE)
        if self.has_numbers(employee['name']):  
            return Response(self.err_data, status.HTTP_400_BAD_REQUEST)


        if 'userProfile' not in employee:
            employee['userProfile'] = []
        
        if 'company' in employee and 'department' in employee:
            employee['company'] = self.lowercase_machine(employee['company'])
            employee['department'] = self.lowercase_machine(employee['department'])
            if self.has_numbers(employee['company']):  
                return Response(self.err_data, status.HTTP_400_BAD_REQUEST)
            if self.has_numbers(employee['department']):  
                return Response(self.err_data, status.HTTP_400_BAD_REQUEST)

            company_ = Company.objects.get_or_create(name= employee['company'])
            employee_dept = Department.objects.get_or_create(name = employee['department'], company= company_[0])
            employee['department'] = employee_dept[0].name
            employee['company'] = employee_dept[0].company.name
        else:
            employee['department'] = None
            employee['company'] = None

        if 'designation' in employee:
            employee['designation'] = self.lowercase_machine(employee['designation'])
            if self.has_numbers(employee['designation']):  
                return Response(self.err_data, status.HTTP_400_BAD_REQUEST)
            try:
                des_pre = Employee.objects.filter(designation = Designation.objects.get(name = employee['designation'])).exists()
                if des_pre:
                    return Response({"error": "already registered designation"}, status.HTTP_400_BAD_REQUEST)
            except Designation.DoesNotExist:
                des_ = Designation.objects.get_or_create(name = employee['designation'])
                employee['designation'] = des_[0].name
        if 'designation' not in employee:
            employee['designation'] = None

        if 'userProfile' in employee:                
            for i in range(len(employee['userProfile'])):
                employee['userProfile'][i] = self.lowercase_machine(employee['userProfile'][i])
                if self.has_numbers(employee['userProfile'][i]):  
                    return Response(self.err_data, status.HTTP_400_BAD_REQUEST)

                up_ = UserProfile.objects.get_or_create(name = employee['userProfile'][i])
                #print(up_[0].id)
                employee['userProfile'][i] = up_[0].name
            
        serializer = self.serializer_class(data=employee)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

class AddDesignation(generics.GenericAPIView):
    serializer_class = DesignationSerializer
    def post(self, request):
        designation_data = request.data 
        serializer = self.serializer_class(data= designation_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

@api_view(['get'])
def getCompanyEmployee(request, comp):
    try:
        company_id = Company.objects.get(name = comp)
        dept_instance = Department.objects.filter(company =  company_id)
        emp_instance = Employee.objects.filter(department__in = dept_instance) 
        serializer = EmployeeSerializerGet(emp_instance, many=True)
        return Response( serializer.data , status.HTTP_200_OK)

    except Company.DoesNotExist:
        data = {
            "error": "Company Not Found"
        }
        return Response(data, status.HTTP_404_NOT_FOUND)



'''
company -> id
id -> departments id
department id -> employee


'''
@api_view(['PATCH'])
def updateOnPatch(request,emp):
    employee = request.data
    try:
        instance = Employee.objects.get(name = emp)
    except Employee.DoesNotExist:
        return Response({"error": "name is not valid"},status.HTTP_400_BAD_REQUEST)

    if 'company' in employee and 'department' in employee and len(employee['company'])!=0 and len(employee['department'])!=0:
        comp_ = Company.objects.get_or_create(name = employee['company'])
        employee['company'] = comp_[0]

        dept_ = Department.objects.get_or_create(name = employee['department'], company = employee['company'])
        employee['department'] = dept_[0].id 
        employee['company'] = comp_[0].id
    elif 'department' in employee and 'company' in employee and len(employee['department']) == 0 and len(employee['company'])==0:
        employee.pop('department')
        employee.pop('company')
    elif 'department' in employee and len(employee['department']) != 0:
        dept_ = Department.objects.get_or_create(name = employee['department'], company = employee.get('company', Company.objects.get_or_create(name = instance.company.name)[0]))
        employee['department'] = dept_[0].id 
    elif 'department' in employee and len(employee['department'])==0:
        employee.pop('department')
    elif 'company' in employee and len(employee['company']) != 0:
        comp_ = Company.objects.get_or_create(name = employee['company'])
        employee['company'] = comp_[0]
        dept_ = Department.objects.get_or_create(name = instance.department.name,
         company = employee.get('company',
         Company.objects.get_or_create(name = instance.company.name)[0]))
        employee['company'] = comp_[0].id
        employee['department'] = dept_[0].id
    elif 'company' in employee and len(employee['company']==0):
        employee.pop('company')
    
      
    if 'designation' in employee and len(employee['designation']) !=0:
        des1_ = Designation.objects.get_or_create(name = employee['designation'])
        try:
            Employee.objects.get(designation = des1_[0].id)
        except Employee.DoesNotExist:
            des_ = Designation.objects.get_or_create(name = employee['designation'])
            employee['designation'] = des_[0].id
        else:
            employee['designation'] = instance.designation.id
    elif 'designation' in employee and len(employee['designation'] )==0:
        employee.pop('designation')
    

    if 'userProfile' in employee and len(employee['userProfile'])!=0:
        for i in range(len(employee['userProfile'])):
            up_ = UserProfile.objects.get_or_create(name = employee['userProfile'][i])
            #print(up_[0].id)
            employee['userProfile'][i] = up_[0].id
    elif 'userProfile' in employee and len(employee['userProfile'] )== 0:
        employee.pop('userProfile')
    

    serializer = EmployeeSerializer(instance , data = employee, partial = True)
    serializer.is_valid()
    serializer.save()
    return Response(serializer.data, status.HTTP_200_OK)
'''
# Possibilities
## Department and Company
- If only company is passed than it will get_or_create 
existing instance department

eg: user5 in Cybage -> IT
if only company is given than it will get_or_create Fedora -> IT

- If only department is passed then it will get_or_create 
existing instance company

eg: user5 in Cybage -> IT
company will remain same get_or_create new department

- Both passed both get or created

-----------------------------------------

## Designation
- if already registered designation passed return present designation
- if new passed then create or get
- Nothing passed present designation
-----------------------------------------
## userProfile
- if nothing is passed it return already registered userprofile
 
'''
@api_view(['DELETE'])
def deleteEmployee(request,emp):
    try:
        instance = Employee.objects.get(name = emp)
        serializer = EmployeeSerializer(instance)
        instance.delete()
        
        return Response(serializer.data, status.HTTP_200_OK)
    except Employee.DoesNotExist:
        data = {
            "Error": "Employee Not Found"
        }
        return Response( data, status.HTTP_400_BAD_REQUEST)

