from django import forms
from emp_app.models import Employer,Employee,Salary

class EmployerForm(forms.ModelForm):
    class Meta():
        model = Employer
        fields = ('emplyr_name','address')


 
