from django.contrib import admin

# Register your models here.
from emp_app.models import Employer,Employee,Salary,Leaves,LeaveAccrualPolicy


admin.site.register(Employer)
admin.site.register(Employee)
admin.site.register(Salary)
admin.site.register(Leaves)
admin.site.register(LeaveAccrualPolicy)
