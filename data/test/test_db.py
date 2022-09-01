
from django.test import TestCase
from data.models import Employee, Company, Department, Designation, UserProfile


class EmployeeTestCase(TestCase):
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
        

    def test_employee_created(self):
        user = Employee.objects.get(name="testuser")
        self.assertEqual(user.name, 'testuser')
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertEqual(user.salary, 12000)
        self.assertEqual(user.department.name, "IT")
        

