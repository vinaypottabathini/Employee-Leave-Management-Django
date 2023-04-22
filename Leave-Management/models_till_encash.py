from django.db import models
from datetime import date
from django.contrib.auth.models import User
# Create your models here.

class Employer(models.Model):
    # emplyr_id = models.AutoField(primary_key=True)
    emplyr_name = models.CharField(primary_key='true',max_length=256)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.emplyr_name

    class Meta:
        db_table = "Employer"





class Employee(models.Model):
    # emp_id = models.AutoField(primary_key=True)
    # emp_name = models.CharField(primary_key='true',max_length=256)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    emp_dob = models.DateField(("Date"), default=date.today,blank=True)
    emp_doj = models.DateField(("Date"), default=date.today,blank=True)
    desig = models.CharField(max_length=256,blank=True)
    depart = models.CharField(max_length=256,blank=True)

    emplyr_name = models.ForeignKey(Employer,on_delete=models.CASCADE)

    manager = models.BooleanField(choices=[(True,'on'),(False,'off')],default=False)

    def __str__(self):
        return str(self.user)

    class Meta:
        db_table = "Employee"


class Salary(models.Model):
    user = models.ForeignKey(Employee,on_delete=models.CASCADE)
    emplyr_name = models.ForeignKey(Employer,on_delete=models.CASCADE)
    # emp_name = models.ForeignKey(Employee,on_delete=models.CASCADE)
    salary =  models.PositiveIntegerField()

    def __str__(self):
        return str(self.user)

    class Meta:
        db_table = "Salary"



class Leaves(models.Model):
    date_of_applied = date.today
    leave_date_from = models.DateField(("Date"), default=date.today,blank=True)
    leave_date_to = models.DateField(("Date"), default=date.today,blank=True)
    descript = models.CharField(max_length=256,blank=True)
    status = models.CharField(max_length=32,blank=True)
    emplyr_name = models.ForeignKey(Employer,on_delete=models.CASCADE)
    # emp_name = models.ForeignKey(Employee,on_delete=models.CASCADE)
    user = models.ForeignKey(Employee,on_delete=models.CASCADE)
    leaves_taken = models.PositiveIntegerField(default=0,blank=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        db_table = "Leaves"

import json

class LeaveAccrualPolicy(models.Model):
    policy_name = models.CharField(max_length=256,blank=True,null=True)
    descript = models.CharField(max_length=256,blank=True,null=True)
    effective_after_no = models.PositiveIntegerField(blank=True,null=True)
    eff_yorm = models.CharField(max_length=32,blank=True,null=True)
    eff_from = models.CharField(max_length=32,blank=True,null=True)
    ac_y_m = models.CharField(max_length=32,blank=True,null=True)
    ac_date = models.PositiveIntegerField(blank=True,null=True)
    ac_datm = models.PositiveIntegerField(blank=True,null=True)
    ac_mth = models.CharField(max_length=32,blank=True,null=True)


    ac_ndays = models.PositiveIntegerField(blank=True,null=True)
    ac_ndays_incre_decre = models.PositiveIntegerField(blank=True,null=True)


    re_y_m = models.CharField(max_length=32,blank=True,null=True)
    re_dat = models.PositiveIntegerField(blank=True,null=True)
    re_datm = models.PositiveIntegerField(blank=True,null=True)
    re_mth = models.CharField(max_length=32,blank=True,null=True)

    cf = models.CharField(max_length=32,blank=True,null=True)
    cf_meter = models.CharField(max_length=32,blank=True,null=True)
    cf_u = models.PositiveIntegerField(blank=True,null=True)
    cf_p = models.PositiveIntegerField(blank=True,null=True)

    ex_y_m = models.CharField(max_length=32,blank=True,null=True)
    ex_mth = models.PositiveIntegerField(blank=True,null=True)
    ex_y = models.PositiveIntegerField(blank=True,null=True)

    ex_ac_updt_list = models.CharField(max_length=1024,default='[[0,0,0,0]]',blank=True,null=True)
    def set_ex_ac_updt_list(self, x):
        self.ex_ac_updt_list = json.dumps(x)

    def get_ex_ac_updt_list(self):
        return json.loads(self.ex_ac_updt_list)

    ovr_lmt = models.PositiveIntegerField(blank=True,null=True)

    en_mtr = models.CharField(max_length=32,blank=True,null=True)
    en_u = models.PositiveIntegerField(blank=True,null=True)
    en_p = models.PositiveIntegerField(blank=True,null=True)
    en_ml = models.PositiveIntegerField(blank=True,null=True)

    emplyr_name = models.ForeignKey(Employer,on_delete=models.CASCADE)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

    class Meta:
        db_table = "LeaveAccrualPolicy"
