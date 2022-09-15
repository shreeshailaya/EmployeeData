from django.test import TestCase, Client
from data.serializer import EmployeeSerializerGet
from data.serializer import EmployeeSerializer
from data.models import Employee, Company, Department, Designation, UserProfile
from rest_framework import generics,status
from django.urls import reverse
from rest_framework.test import APIClient
api_client = APIClient()
client = Client()


class GetAllEmployeeTest(TestCase):
    def setUp(self):
        user_p1 = UserProfile.objects.create(name = 'testrole1')
        user_p2 = UserProfile.objects.create(name = 'testrole2')
        company_instance = Company.objects.create(name = "testcompany")
        desig_instance = Designation.objects.create(name = "testdesg")
        dept_instance = Department.objects.create(name = "IT", company = company_instance)
        emp_instance = Employee.objects.create(
            name="testuser",
            email = "test@gmail.com",
            salary = 12000,
            department = dept_instance,
            designation = desig_instance,
            company = company_instance
            
        )
        emp_instance.userProfile.add(user_p1,user_p2)
        desig_instance1 = Designation.objects.create(name = "testdesgb")
        

    def test_get_all_employees(self):
        response = client.get(reverse('getemployees'))
        employees = Employee.objects.all()
        serializer = EmployeeSerializerGet(employees, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_employee_on_name(self):
        response = api_client.get('/api/employee/testuser')
        employee = Employee.objects.get(name = 'testuser')
        serializer =  EmployeeSerializerGet(employee)
        self.assertEqual(response.data, serializer.data )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_wrong_employee_name(self):
        response = api_client.get('/api/employee/testuser123')
        employee = Employee.objects.get(name = 'testuser')
        serializer =  EmployeeSerializerGet(employee)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        #self.assertEqual(serializer.data, response.data)

    def test_get_all_company_employees(self):
        response = api_client.get('/api/company-emp/testcompany')
        company_ = Company.objects.get(name = 'testcompany')
        dept_instance = Department.objects.filter(company =  company_)
        emp_instance = Employee.objects.filter(department__in = dept_instance)
        serializer = EmployeeSerializerGet(emp_instance, many=True)
        self.assertEqual(serializer.data, response.data)
    
    def test_get_all_company_employees_wrong_company(self):
        response = api_client.get('/api/company-emp/xyz')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_register_user_all_parameter(self):
        user_data = {
       
        "name": "test",
        "email": "user5@gmail.com",
        "salary": 2332,
        "department": "IT",
        "designation": "testdesga",
        "company": "testcompany",
        "userProfile": [
            "test"
        ]
    }
        response = api_client.post('/api/register/', user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_with_name(self):
        user_data = {
            "name": "shree"
        }
        request = api_client.post('/api/register/', user_data)
        response = Employee.objects.get(name = user_data['name'])

        self.assertEqual(request.data['name'], response.name)

    def test_register_user_without_name(self):
        user_data = {
            "email":"shree@gmail.com"
        }
        request = api_client.post('/api/register/', user_data)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_user_designation_already_registered(self):
        user_data = {
            "name": "nameUser",
            "designation": "testdesg"
        }
        request = api_client.post('/api/register/', user_data)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_already_exists(self):
        user_data = {
            "name":"testuser"
        }

        request = api_client.post('/api/register/', user_data)
        self.assertEqual(request.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_register_name_contain_number(self):
        user_data = {
            "name":"shree123"
        }

        request = api_client.post('/api/register/', user_data)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_company_contain_number(self):
        user_data = {
            "name":"shree1234",
            "company": "com2",
            "department": "dep1"
        }
        request = api_client.post('/api/register/', user_data)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
    def test_register_department_contain_number(self):
        user_data = {
            "name":"shree1234",
            "company": "com",
            "department": "dep1"
        }
        request = api_client.post('/api/register/', user_data)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_designation_contain_number(self):
        user_data = {
            "name":"shreeshail",
            "company": "com",
            "department": "dep",
            "designation": "desf4"
        }
        request = api_client.post('/api/register/', user_data)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_userPro_contain_number(self):
        user_data = {
            "name":"shreeshail",
            "company": "com",
            "department": "dep",
            "designation": "desf",
            "userProfile": [
                "up1"
            ]
        }
        request = api_client.post('/api/register/', user_data)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_add_designation_contain_number(self):
        user_data = {
            "name":"adddesg"
        }
        request = api_client.post('/api/designation/', user_data)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
    
    def test_patch_name_not_correct(self):
        patch_data = {
            "email": "test@g.com"
        }
        response = api_client.patch('/api/update-emp/xxx', patch_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_patch_request_on_email(self):
        patch_data = {
            "email": "test@g.com"
        }
        response = api_client.patch('/api/update-emp/testuser', patch_data, format='json')
        emp_ = Employee.objects.get(name = 'testuser')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'] , emp_.email)

    def test_patch_on_company(self):
        data = {
            "company": "TestCybage"
        }
        request = api_client.patch('/api/update-emp/testuser', data, format='json')
        response = Employee.objects.get(name ='testuser' )

        self.assertEqual(request.data['company'], response.company.name)
        self.assertEqual(request.data['department'], response.department.name)

    def test_patch_on_department(self):
        data = {
            "department": "TestDept"
        }
        request = api_client.patch('/api/update-emp/testuser', data, format='json')
        response = Employee.objects.get(name ='testuser' )

        self.assertEqual(request.data['company'], response.company.name)
        self.assertEqual(request.data['department'], response.department.name)

    def test_patch_on_company_and_department(self):
        data = {
            "company": "TestCybage",
            "department": "Admin"
        }
        request = api_client.patch('/api/update-emp/testuser', data, format='json')
        response = Employee.objects.get(name ='testuser' )

        self.assertEqual(request.data['company'], response.company.name)
        self.assertEqual(request.data['department'], response.department.name)

    def test_patch_company_department_blank(self):
        data = {
            "company": "",
            "department": ""
        }
        request = api_client.patch('/api/update-emp/testuser', data, format='json')
        response = Employee.objects.get(name ='testuser' )

        self.assertEqual(request.data['company'], response.company.name)
        self.assertEqual(request.data['department'], response.department.name)

    def test_patch_designation(self):
        data = {
            "designation": "TestDesignation"
        }
        request = api_client.patch('/api/update-emp/testuser', data, format='json')
        response = Employee.objects.get(name ='testuser' )

        self.assertEqual(request.data['name'], response.name)
        self.assertEqual(request.data['designation'], response.designation.name)

    def test_patch_nothing_passed_designation(self):
        data = {
            "designation": ""
        }
        request = api_client.patch('/api/update-emp/testuser', data, format='json')
        response = Employee.objects.get(name ='testuser' )

        self.assertEqual(request.data['name'], response.name)
        self.assertEqual(request.data['designation'], response.designation.name)

    def test_patch_userProfile(self):
        data = {
            "userProfile": [
                "upa",
                "upb"
            ]
        }
        request = api_client.patch('/api/update-emp/testuser', data, format='json')
        response = Employee.objects.get(name ='testuser' )
        up_ = UserProfile.objects.get(name = request.data['userProfile'][0])
        self.assertEqual(request.data['name'], response.name)
        self.assertEqual(request.data['userProfile'][0], up_.name)

    def test_delete_request(self):
        response = api_client.delete('/api/delete-emp/testuser')
        self.assertEqual(response.data['id'], None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_wrong(self):
        response = api_client.delete('/api/delete-emp/xxx')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
        
# pytest --html=report.html
# pytest --cov
# py.test --cov=data --cov-report=html
