from django.shortcuts import render
from django.conf import settings
from django.views.generic import View,TemplateView,ListView,DetailView
from django.http import HttpResponse
from . import models
from emp_app.models import Employer,Employee,Salary,Leaves,LeaveAccrualPolicy
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
# from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
import datetime



# class IndexView(TemplateView):
#     template_name = 'index.html'

def login(request):
    return render(request,'login.html')

def fromleavetohome(request):
    emp=request.POST.get('emp_name')
    print(emp)
    return render(request,'index_employee.html',{'emp':emp})

def fromapprovetohome(request):
    emp=request.POST.get('emp_name')
    print(emp)
    return render(request,'index_manager.html',{'emp':emp})


def secondpage(request):
    return render(request,'index.html')




def index(request):
    emp = request.POST.get('username')
    pwd = request.POST.get('password')

    user = authenticate(request,username=emp,password=pwd)

    if user:
        #return render(request,'index_employee.html',{'emp':emp})
        obj = Employee.objects.get(user=User.objects.get(username=emp))
        if obj.manager ==True:
            return render(request,'index_manager.html',{'emp':emp,'emplr':obj.emplyr_name})
        else:
            return render(request,'index_employee.html',{'emp':emp,'emplr':obj.emplyr_name})
    else:
        return HttpResponse("Invalid Credentials")







def employer_form(request):
    return render(request,'add_employer_form.html')

def employee_form(request):
    return render(request,'add_employee_form.html',{'employers':Employer.objects.all()})


def create_employer(request):
    if request.method == 'POST':
        emplr = request.POST.get('employer_name')
        adr = request.POST.get('address')

        to_db = Employer(emplyr_name=emplr,address=adr)
        to_db.save()

        return render(request,'employer_created.html')


def create_employee(request):
    if request.method == 'POST':
        emp =request.POST.get('emp_name')
        emplr = request.POST.get('emplyr_name')
        dob = request.POST.get('dob')
        doj = request.POST.get('doj')
        desig = request.POST.get('desig')
        depart= request.POST.get('depart')
        mng = request.POST.get('manager')
        if mng=='on':
            mng=True
        else:
            mng = False
        return render(request,'password.html',{'emp':emp.lower(),'emplr':emplr,'dob':dob,'doj':doj,'desig':desig,'depart':depart,'mng':mng})


def password(request):
    if request.method == 'POST':
        pwd=request.POST.get('pwd')
        emp = request.POST.get('emp_name')
        emplr = request.POST.get('emplr')
        dob = request.POST.get('dob')
        doj = request.POST.get('doj')
        desig = request.POST.get('desig')
        depart= request.POST.get('depart')
        mng = request.POST.get('mng')

        mail = emp+"@"+emplr.lower()+".com"

        user =User.objects.create(username=request.POST['emp_name'],
                email=mail)
        user.password = make_password(pwd)
        user.is_superuser=True
        user.save()

        to_db = Employee(user=user,emplyr_name=Employer.objects.get(emplyr_name=emplr),emp_dob=dob,emp_doj=doj,desig=desig,depart=depart,manager=mng)
        to_db.save()

        return render(request,'employee_created.html')



def update_salary_page(request):
    return render(request,'salary_company.html',{'employers':Employer.objects.all()})

def update_salary_company(request):
    if request.method == 'POST':
        emplyr = request.POST.get('emplyr_name')
        print(emplyr)
        return render(request,'salary.html',{'emplyr':emplyr,'employs':Employee.objects.filter(emplyr_name=emplyr)})


def update_salary(request):
    if request.method == 'POST':
        emp =request.POST.get('emp_name')
        emplr = request.POST.get('emplyr_name')
        sal = request.POST.get('salary')
        # try:
        to_db = Salary(emplyr_name=Employer.objects.get(emplyr_name=emplr),user=Employee.objects.get(user=User.objects.get(username=emp)),salary=sal)
        to_db.save()
        return render(request,'salary_updated.html')


def display_company(request):
    return render(request,'display_company.html',{'employers':Employer.objects.all()})


def show_employees(request):
    emplyr = request.POST.get('emplyr_name')
    return render(request,'show_employees.html',{'emplyr':emplyr,'salemps':Salary.objects.filter(emplyr_name=emplyr),'employs':Employee.objects.filter(emplyr_name=emplyr)})

def payroll(request):
    emp = request.POST.get('emp_name')
    ctc = int(request.POST.get('ctc'))
    ctcpm = ctc//12
    basic_pa =int(0.4*ctc)
    basic_pm = int(0.4*ctcpm)
    hra_pa =int(0.4*basic_pa)
    hra_pm =int(0.4*basic_pm)
    empf_pa = int(0.12*basic_pa)
    empf_pm = int(0.12*basic_pm)
    spc_alw_pa = ctc-hra_pa-basic_pa-empf_pa
    spc_alw_pm = ctcpm-hra_pm-basic_pm-empf_pm
    gross_pa = basic_pa+hra_pa+spc_alw_pa
    gross_pm = basic_pm+hra_pm+spc_alw_pm

    cals={'emp':Employee.objects.filter(user=User.objects.get(username=emp)),'ctc':ctc,'ctcpm':ctcpm,'basic_pa':basic_pa,'basic_pm':basic_pm,'hra_pa':hra_pa,'hra_pm':hra_pm,'empf_pa':empf_pa,'empf_pm':empf_pm,'spc_alw_pa':spc_alw_pa,'spc_alw_pm':spc_alw_pm,'gross_pa':gross_pa,'gross_pm':gross_pm}
    return render(request,'show_pays.html',context=cals)



def apply_leave_page_and_show_status(request):
    emp=request.POST.get('emp_name')
    return render(request,'leave_page.html',{'leav':Leaves.objects.filter(user=Employee.objects.get(user=User.objects.get(username=emp))),'emp':Employee.objects.get(user=User.objects.get(username=emp))})
    #return render(request,'leave_page.html',{'emp':Employee.objects.get(user=User.objects.get(username=emp))})







def resett(obj):
    obj.ac_ndays_incre_decre=0
    obj.set_ex_ac_updt_list([[0,0,0,0]])
    obj.save()
    return True

def leaves_reset(obj):
    x = datetime.datetime.now()
    if obj.re_dat==None:
        if obj.re_datm==x.day and obj.re_mth==x.month:
            resett(obj)
    elif obj.re_datm==None:
        if obj.re_dat==x.day:
            resett(obj)

    return True


def remove_expired_leaves(obj):
    ls=obj.get_ex_ac_updt_list()
    x = datetime.datetime.now()
    to_del=[]
    if len(ls)>1:
        for k in range(1,len(ls)):
            if ls[k][2]=='m':
                if ls[k][1]==x.month:
                    if ls[k][0]>0:
                        if obj.ac_ndays_incre_decre>=ls[k][0]:
                            obj.ac_ndays_incre_decre-=ls[k][0]
                            if obj.en_u!=None:
                                obj.en_u-=ls[k][0]
                        else:
                            obj.ac_ndays_incre_decre=0
                            if obj.en_u!=None:
                                obj.en_u=0
                        to_del.append(k)

            elif ls[k][2]=='y':
                if ls[k][1]==x.year:
                    if ls[k][0]>0:
                        if obj.ac_ndays_incre_decre>=ls[k][0]:
                            obj.ac_ndays_incre_decre-=ls[k][0]
                            if obj.en_u!=None:
                                obj.en_u-=ls[k][0]
                        else:
                            obj.ac_ndays_incre_decre=0
                            if obj.en_u!=None:
                                obj.en_u=0
                        to_del.append(k)

        for k in to_del:
            del ls[k]
        obj.set_ex_ac_updt_list(ls)
        obj.save()
    return True




def carry_units(obj):
    if obj.cf_u <=obj.ac_ndays_incre_decre:
        carry=obj.cf_u
    else:
        carry=obj.ac_ndays_incre_decre
    return carry


def carry_percent(obj):
    p = obj.cf_p
    tmp = int((p/100)*obj.ac_ndays)
    if tmp<=obj.ac_ndays_incre_decre:
        carry=tmp
    else:
        carry = obj.ac_ndays_incre_decre
    return carry

def fill_expire_leaves(obj):
    x = datetime.datetime.now()
    ls=obj.get_ex_ac_updt_list()
    print("List: ",ls)
    if obj.ex_y_m=="2":
        if obj.cf_meter=="1":
            carry = carry_units(obj)
        elif obj.cf_meter=="2":
            carry = carry_percent(obj)
        if int(obj.ex_mth)+x.month>12:
            mth=int(obj.ex_mth)+x.month-12
            ls.append([carry,mth,'m',x.month])
        else:
            ls.append([carry,int(obj.ex_mth)+x.month,'m',x.month])

        obj.set_ex_ac_updt_list(ls)
        obj.save()
    elif obj.ex_y_m=="1":
        if obj.cf_meter=="1":
            carry = carry_units(obj)
        elif obj.cf_meter=="2":
            carry = carry_percent(obj)
        ls.append([carry,int(obj.ex_y)+x.year,'y',x.year])
        obj.set_ex_ac_updt_list(ls)
        obj.save()
    print("LIST: ",ls)
    return carry

def check_unexpired_carries(obj):
    x = datetime.datetime.now()
    ls=obj.get_ex_ac_updt_list()
    print("List1: ",ls)
    carry=0
    if len(ls)>1:
        for k in range(1,len(ls)-1):
            carry+=ls[k][0]
    return carry


def carrys(obj):
    if obj.cf=="1":
        if obj.cf_meter=="1":
            carry = carry_units(obj)

        elif obj.cf_meter == "2":
            carry = carry_percent(obj)

        print("carry1:  ",carry)
        obj.ac_ndays_incre_decre=carry+obj.ac_ndays
        if obj.en_u!=None:
            obj.en_u+=carry
            if obj.en_u>obj.en_ml:
                obj.en_u=obj.en_ml
        obj.save()

    elif obj.cf=="2":
        carry=fill_expire_leaves(obj)
        car = check_unexpired_carries(obj)
        obj.ac_ndays_incre_decre=carry+obj.ac_ndays+car
        if obj.en_u!=None:
            obj.en_u+=carry+car
            if obj.en_u>obj.en_ml:
                obj.en_u=obj.en_ml
        obj.save()

    elif obj.cf=="3":
        if obj.cf_meter=="1":
            carry = carry_units(obj)

        elif obj.cf_meter == "2":
            carry = carry_percent(obj)

        print("carry1 with overall limit:  ",carry)
        obj.ac_ndays_incre_decre=carry+obj.ac_ndays
        if obj.ac_ndays_incre_decre>obj.ovr_lmt:
            obj.ac_ndays_incre_decre=obj.ovr_lmt

        if obj.en_u!=None:
            obj.en_u+=carry
            if obj.en_u>obj.en_ml:
                obj.en_u=obj.en_ml
        obj.save()

    return True

def accrual_update(request,obj):
    x = datetime.datetime.now()
    month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    emplr = request.POST.get('emplr')
    emp= request.POST.get('emp_name')


    if obj.ac_date==0:   #yearly
        if month[x.month-1]== obj.ac_mth and obj.ac_datm==x.day:
            carrys(obj)
    else:
        if x.day==obj.ac_date:  #every month
            carrys(obj)

    return True


def leave_accrual_update_check(request):
    x = datetime.datetime.now()
    month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    emplr = request.POST.get('emplr')
    emp= request.POST.get('emp_name')
    obj = LeaveAccrualPolicy.objects.get(user=User.objects.get(username=emp))

    remove_expired_leaves(obj)
    print("OBJ: ", obj.ac_date)
    print("EP:", emp)

    if obj.eff_yorm=='m':
        if x.month>=obj.effective_after_no:
            accrual_update(request,obj)
    elif obj.eff_yorm == 'y':
        if x.year>=obj.effective_after_no:
            accrual_update(request,obj)

    ##RESET FUNCTION BELOW
    # leaves_reset(obj)
    return True


def store_leave(request):
    leave_accrual_update_check(request)


    ldf = request.POST.get('ldf')
    ldt = request.POST.get('ldt')
    dscp = request.POST.get('descript')

    emplr = request.POST.get('emplr')
    emp= request.POST.get('emp_name')

    lvs_taken = request.POST.get('lvs_taken')
    print("leaves_taken: ",lvs_taken)




    obj = LeaveAccrualPolicy.objects.get(user=User.objects.get(username=emp))
    print("Accrual Leaves:  ",obj.policy_name)
    # num = obj.ac_ndays
    if obj.ac_ndays_incre_decre>0:
        obj.ac_ndays_incre_decre-=1
        obj.save()
        if obj.en_u!=None:
            if obj.en_u>0:
                obj.en_u-=1
                obj.save()
        if obj.cf=="2":
            ls=obj.get_ex_ac_updt_list()
            if len(ls)>1:
                for k in range(1,len(ls)):
                    if ls[k][0]>0:
                        ls[k][0]-=1
                        obj.set_ex_ac_updt_list(ls)
                        break

        obj.save()
        to_db = Leaves(leaves_taken=int(lvs_taken)+1,leave_date_from=ldf,leave_date_to=ldt,descript=dscp,emplyr_name=Employer.objects.get(emplyr_name=emplr),user=Employee.objects.get(user=User.objects.get(username=emp)),status='pending')
        to_db.save()
        msg=""
    else:
        msg="Leaves exceeded policy leaves!"
    # if int(lvs_taken)<int(num):
    #     to_db = Leaves(leaves_taken=int(lvs_taken)+1,leave_date_from=ldf,leave_date_to=ldt,descript=dscp,emplyr_name=Employer.objects.get(emplyr_name=emplr),user=Employee.objects.get(user=User.objects.get(username=emp)),status='pending')
    #     to_db.save()
    #     msg=""
    # else:
    #     msg="Leaves exceeded policy leaves!"

    # subject, from_email, to = 'Your Employee applied for Leave', 'vinay040998@gmail.com', 'vinay@gridlex.com'
    # message= 'Description: '+dscp+' \nFrom: '+ldf+" To: "+ldt
    # html_content = '<p>This is an <strong>important</strong> message.</p>'
    # send_mail(subject, message, from_email, [to])

    return render(request,'leave_page.html',{'msg':msg,'leav':Leaves.objects.filter(user=Employee.objects.get(user=User.objects.get(username=emp))),'emp':Employee.objects.get(user=User.objects.get(username=emp))})



def show_leaves_to_manager(request):
    emp = request.POST.get('emp_name')
    emplr = request.POST.get('emplr')
    print(emplr)
    return render(request,'approve_page.html',{'leav':Leaves.objects.filter(emplyr_name=Employer.objects.get(emplyr_name=emplr)),'emp':emp,'emplr':emplr})



def approve_leaves(request):
    emp = request.POST.get('emp_name')
    emplr = request.POST.get('emplr')
    lv=request.POST.get('lvemp')
    stat = request.POST.get('status')
    pm = request.POST.get('pm')

    if stat=="approve":
        stat="Approved"
    elif stat=="reject":
        stat="Rejected"

    to_db = Leaves.objects.get(id=pm,user=Employee.objects.get(user=User.objects.get(username=lv)))
    to_db.status=stat
    to_db.save()

    return render(request,'approve_page.html',{'leav':Leaves.objects.filter(emplyr_name=Employer.objects.get(emplyr_name=emplr)),'emp':emp,'emplr':emplr})

def policy(request):
    emp=request.POST.get('emp_name')
    emplr =request.POST.get('emplyr_name')
    print("EMP: ",emp)
    mdays=[x for x in range(1,29)]
    month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    return render(request,'policy_page.html',locals())


def policy_page(request):

    x = datetime.datetime.now()
    eff = request.POST.get('eff')
    yorm = request.POST.get('yorm')

    if yorm=='m':
        eff = int(eff)+x.month
    elif yorm=='y':
        eff = x.year+int(eff)


    frm = request.POST.get('frm')

    ac_y_m = request.POST.get('ac_y_m')
    ac_date = request.POST.get('dat')
    ac_datm = request.POST.get('datm')
    ac_mth = request.POST.get('mth')
    ac_ndays = request.POST.get('ac_ndays')

    re_y_m =request.POST.get('re_y_m')
    re_dat=request.POST.get('re_dat')
    re_datm = request.POST.get('re_datm')
    re_mth = request.POST.get('re_mth')

    cf = request.POST.get('cf')
    cf_meter = request.POST.get('cf_meter')
    cf_u = request.POST.get('cf_u')
    cf_p = request.POST.get('cf_p')



    ex_y_m = request.POST.get('ex_y_m')
    ex_mth = request.POST.get('ex_mth')
    ex_y = request.POST.get('ex_y')

    ovr_lmt = request.POST.get('ovr_lmt')

    en_mtr = request.POST.get('en_mtr')
    en_u = request.POST.get('en_u')
    en_p = request.POST.get('en_p')
    en_ml = request.POST.get('en_ml')


    policy_type= request.POST.get('policy_type')

    print("eff: ",eff)
    print("yorm: ",yorm)



    print("frm: ",frm)
    print("ac_y_m: ",ac_y_m)
    print("ac_date: ",ac_date)
    print("ac_datm: ",ac_datm)
    print("ac_mth: ",ac_mth)
    print("ac_ndays: ",ac_ndays)
    print("re_y_m: ",re_y_m)
    print("re_dat: ",re_dat)
    print("re_datm: ",re_datm)
    print("re_mth: ",re_mth)
    print("cf: ",cf)
    print("cf_meter: ",cf_meter)
    print("cf_u: ",cf_u)
    print("cf_p: ",cf_p)
    print("ex_y_m: ",ex_y_m)
    print("ex_mth: ",ex_mth)
    print("ex_y: ",ex_y)
    print("ovr_lmt: ",ovr_lmt)
    print("en_mtr: ",en_mtr)
    print("en_u: ",en_u)
    print("en_p: ",en_p)
    print("en_ml: ",en_ml)



    policy=request.POST.get('top_name')
    print(policy)
    des=request.POST.get('top_desc')
    print(des)
    emp = request.POST.get('emp')
    print("Employee: ",emp)
    emplr = request.POST.get('emplyr_name')
    print(emplr)
    mdays=[x for x in range(1,29)]
    month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']





    ## carry with Encashment with reset
    if en_mtr!=None:
        if en_mtr=="1":
            if cf!=None:
                if cf=="1":
                    if cf_meter!=None:
                        if cf_meter == "1":
                            to_db = LeaveAccrualPolicy( policy_type=policy_type, en_u=en_u, en_mtr=en_mtr, en_ml=en_ml ,re_y_m=re_y_m,re_datm=re_datm, re_mth=re_mth, cf_u=cf_u , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                            to_db.save()
                            print("yeah done it!")
                            return render(request,'policy_page.html',locals())
                        elif cf_meter == "2":
                            to_db = LeaveAccrualPolicy( policy_type=policy_type, en_u=en_u, en_mtr=en_mtr, en_ml=en_ml , re_y_m=re_y_m,re_datm=re_datm, re_mth=re_mth, cf_p=cf_p , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                            to_db.save()
                            print("yeah done it! carry percent")
                            return render(request,'policy_page.html',locals())
                elif cf=="2":
                    if cf_meter!=None:
                        if cf_meter=="1":
                            if ex_y_m=="2":
                                to_db = LeaveAccrualPolicy( policy_type=policy_type, en_u=en_u, en_mtr=en_mtr, en_ml=en_ml , re_y_m=re_y_m, re_datm=re_datm, re_mth=re_mth, ex_mth=ex_mth , ex_y_m=ex_y_m ,cf_u=cf_u , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                                to_db.save()
                                return render(request,'policy_page.html',locals())
                            elif ex_y_m=="1":
                                to_db = LeaveAccrualPolicy( policy_type=policy_type, en_u=en_u, en_mtr=en_mtr, en_ml=en_ml , re_y_m=re_y_m, re_datm=re_datm, re_mth=re_mth, ex_y = ex_y , ex_y_m=ex_y_m ,cf_u=cf_u , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                                to_db.save()
                                return render(request,'policy_page.html',locals())
                        elif cf_meter == "2":
                            if ex_y_m=="2":
                                to_db = LeaveAccrualPolicy( policy_type=policy_type, en_u=en_u, en_mtr=en_mtr, en_ml=en_ml , re_y_m=re_y_m, re_datm=re_datm, re_mth=re_mth, ex_mth=ex_mth , ex_y_m=ex_y_m ,cf_p=cf_p , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                                to_db.save()
                                return render(request,'policy_page.html',locals())
                            elif ex_y_m=="1":
                                to_db = LeaveAccrualPolicy( policy_type=policy_type, en_u=en_u, en_mtr=en_mtr, en_ml=en_ml , re_y_m=re_y_m, re_datm=re_datm, re_mth=re_mth, ex_y = ex_y , ex_y_m=ex_y_m ,cf_p=cf_p , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                                to_db.save()
                                return render(request,'policy_page.html',locals())


                elif cf=="3":
                    if cf_meter!=None:
                        if cf_meter == "1":
                            to_db = LeaveAccrualPolicy( policy_type=policy_type, en_u=en_u, en_mtr=en_mtr, en_ml=en_ml ,re_y_m=re_y_m, re_datm=re_datm, re_mth=re_mth, ovr_lmt=ovr_lmt,cf_u=cf_u , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                            to_db.save()
                            print("yeah done it with overall limit !")
                            return render(request,'policy_page.html',locals())
                        elif cf_meter == "2":
                            to_db = LeaveAccrualPolicy( policy_type=policy_type, en_u=en_u, en_mtr=en_mtr, en_ml=en_ml ,re_y_m=re_y_m, re_datm=re_datm, re_mth=re_mth, ovr_lmt=ovr_lmt,cf_p=cf_p , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                            to_db.save()
                            print("yeah done it! carry percent with overall limit ")
                            return render(request,'policy_page.html',locals())


        if en_mtr=="2":
            en_u = int((int(en_p)/100)*ac_ndays)
            if cf!=None:
                if cf=="1":
                    if cf_meter!=None:
                        if cf_meter == "1":
                            to_db = LeaveAccrualPolicy( policy_type=policy_type, en_u=en_u,en_p=en_p, en_mtr=en_mtr, en_ml=en_ml ,re_y_m=re_y_m, re_dat=re_dat, cf_u=cf_u , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                            to_db.save()
                            print("yeah done it!")
                            return render(request,'policy_page.html',locals())
                        elif cf_meter == "2":
                            to_db = LeaveAccrualPolicy( policy_type=policy_type, en_u=en_u,en_p=en_p, en_mtr=en_mtr, en_ml=en_ml ,re_y_m=re_y_m, re_dat=re_dat, cf_p=cf_p , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                            to_db.save()
                            print("yeah done it! carry percent")
                            return render(request,'policy_page.html',locals())
                elif cf=="2":
                    if cf_meter!=None:
                        if cf_meter=="1":
                            if ex_y_m=="2":
                                to_db = LeaveAccrualPolicy( policy_type=policy_type, en_u=en_u,en_p=en_p, en_mtr=en_mtr, en_ml=en_ml ,re_y_m=re_y_m, re_dat=re_dat, ex_mth=ex_mth , ex_y_m=ex_y_m ,cf_u=cf_u , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                                to_db.save()
                                return render(request,'policy_page.html',locals())
                            elif ex_y_m=="1":
                                to_db = LeaveAccrualPolicy( policy_type=policy_type, en_u=en_u,en_p=en_p, en_mtr=en_mtr, en_ml=en_ml ,re_y_m=re_y_m, re_dat=re_dat, ex_y = ex_y , ex_y_m=ex_y_m ,cf_u=cf_u , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                                to_db.save()
                                return render(request,'policy_page.html',locals())
                        elif cf_meter == "2":
                            if ex_y_m=="2":
                                to_db = LeaveAccrualPolicy( policy_type=policy_type, en_u=en_u,en_p=en_p, en_mtr=en_mtr, en_ml=en_ml ,re_y_m=re_y_m, re_dat=re_dat, ex_mth=ex_mth , ex_y_m=ex_y_m ,cf_p=cf_p , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                                to_db.save()
                                return render(request,'policy_page.html',locals())
                            elif ex_y_m=="1":
                                to_db = LeaveAccrualPolicy( policy_type=policy_type, en_u=en_u,en_p=en_p, en_mtr=en_mtr, en_ml=en_ml ,re_y_m=re_y_m, re_dat=re_dat, ex_y = ex_y , ex_y_m=ex_y_m ,cf_p=cf_p , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                                to_db.save()
                                return render(request,'policy_page.html',locals())


                elif cf=="3":
                    if cf_meter!=None:
                        if cf_meter == "1":
                            to_db = LeaveAccrualPolicy( policy_type=policy_type, en_u=en_u,en_p=en_p, en_mtr=en_mtr, en_ml=en_ml ,re_y_m=re_y_m, re_dat=re_dat, ovr_lmt=ovr_lmt,cf_u=cf_u , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                            to_db.save()
                            print("yeah done it with overall limit !")
                            return render(request,'policy_page.html',locals())
                        elif cf_meter == "2":
                            to_db = LeaveAccrualPolicy( policy_type=policy_type, en_u=en_u,en_p=en_p, en_mtr=en_mtr, en_ml=en_ml ,re_y_m=re_y_m, re_dat=re_dat, ovr_lmt=ovr_lmt,cf_p=cf_p , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                            to_db.save()
                            print("yeah done it! carry percent with overall limit ")
                            return render(request,'policy_page.html',locals())
















    #carry with reset
    if re_y_m!=None:
        if re_dat=="0":
            if cf!=None:
                if cf=="1":
                    if cf_meter!=None:
                        if cf_meter == "1":
                            to_db = LeaveAccrualPolicy(re_y_m=re_y_m,re_datm=re_datm, re_mth=re_mth, cf_u=cf_u , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                            to_db.save()
                            print("yeah done it!")
                            return render(request,'policy_page.html',locals())
                        elif cf_meter == "2":
                            to_db = LeaveAccrualPolicy( re_y_m=re_y_m,re_datm=re_datm, re_mth=re_mth, cf_p=cf_p , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                            to_db.save()
                            print("yeah done it! carry percent")
                            return render(request,'policy_page.html',locals())
                elif cf=="2":
                    if cf_meter!=None:
                        if cf_meter=="1":
                            if ex_y_m=="2":
                                to_db = LeaveAccrualPolicy(re_y_m=re_y_m, re_datm=re_datm, re_mth=re_mth, ex_mth=ex_mth , ex_y_m=ex_y_m ,cf_u=cf_u , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                                to_db.save()
                                return render(request,'policy_page.html',locals())
                            elif ex_y_m=="1":
                                to_db = LeaveAccrualPolicy(re_y_m=re_y_m, re_datm=re_datm, re_mth=re_mth, ex_y = ex_y , ex_y_m=ex_y_m ,cf_u=cf_u , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                                to_db.save()
                                return render(request,'policy_page.html',locals())
                        elif cf_meter == "2":
                            if ex_y_m=="2":
                                to_db = LeaveAccrualPolicy(re_y_m=re_y_m, re_datm=re_datm, re_mth=re_mth, ex_mth=ex_mth , ex_y_m=ex_y_m ,cf_p=cf_p , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                                to_db.save()
                                return render(request,'policy_page.html',locals())
                            elif ex_y_m=="1":
                                to_db = LeaveAccrualPolicy(re_y_m=re_y_m, re_datm=re_datm, re_mth=re_mth, ex_y = ex_y , ex_y_m=ex_y_m ,cf_p=cf_p , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                                to_db.save()
                                return render(request,'policy_page.html',locals())


                elif cf=="3":
                    if cf_meter!=None:
                        if cf_meter == "1":
                            to_db = LeaveAccrualPolicy(re_y_m=re_y_m, re_datm=re_datm, re_mth=re_mth, ovr_lmt=ovr_lmt,cf_u=cf_u , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                            to_db.save()
                            print("yeah done it with overall limit !")
                            return render(request,'policy_page.html',locals())
                        elif cf_meter == "2":
                            to_db = LeaveAccrualPolicy(re_y_m=re_y_m, re_datm=re_datm, re_mth=re_mth, ovr_lmt=ovr_lmt,cf_p=cf_p , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                            to_db.save()
                            print("yeah done it! carry percent with overall limit ")
                            return render(request,'policy_page.html',locals())

        elif re_datm=="0":
            if cf!=None:
                if cf=="1":
                    if cf_meter!=None:
                        if cf_meter == "1":
                            to_db = LeaveAccrualPolicy(re_y_m=re_y_m, re_dat=re_dat, cf_u=cf_u , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                            to_db.save()
                            print("yeah done it!")
                            return render(request,'policy_page.html',locals())
                        elif cf_meter == "2":
                            to_db = LeaveAccrualPolicy(re_y_m=re_y_m, re_dat=re_dat, cf_p=cf_p , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                            to_db.save()
                            print("yeah done it! carry percent")
                            return render(request,'policy_page.html',locals())
                elif cf=="2":
                    if cf_meter!=None:
                        if cf_meter=="1":
                            if ex_y_m=="2":
                                to_db = LeaveAccrualPolicy(re_y_m=re_y_m, re_dat=re_dat, ex_mth=ex_mth , ex_y_m=ex_y_m ,cf_u=cf_u , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                                to_db.save()
                                return render(request,'policy_page.html',locals())
                            elif ex_y_m=="1":
                                to_db = LeaveAccrualPolicy(re_y_m=re_y_m, re_dat=re_dat, ex_y = ex_y , ex_y_m=ex_y_m ,cf_u=cf_u , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                                to_db.save()
                                return render(request,'policy_page.html',locals())
                        elif cf_meter == "2":
                            if ex_y_m=="2":
                                to_db = LeaveAccrualPolicy(re_y_m=re_y_m, re_dat=re_dat, ex_mth=ex_mth , ex_y_m=ex_y_m ,cf_p=cf_p , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                                to_db.save()
                                return render(request,'policy_page.html',locals())
                            elif ex_y_m=="1":
                                to_db = LeaveAccrualPolicy(re_y_m=re_y_m, re_dat=re_dat, ex_y = ex_y , ex_y_m=ex_y_m ,cf_p=cf_p , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                                to_db.save()
                                return render(request,'policy_page.html',locals())


                elif cf=="3":
                    if cf_meter!=None:
                        if cf_meter == "1":
                            to_db = LeaveAccrualPolicy(re_y_m=re_y_m, re_dat=re_dat, ovr_lmt=ovr_lmt,cf_u=cf_u , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                            to_db.save()
                            print("yeah done it with overall limit !")
                            return render(request,'policy_page.html',locals())
                        elif cf_meter == "2":
                            to_db = LeaveAccrualPolicy(re_y_m=re_y_m, re_dat=re_dat, ovr_lmt=ovr_lmt,cf_p=cf_p , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                            to_db.save()
                            print("yeah done it! carry percent with overall limit ")
                            return render(request,'policy_page.html',locals())


















    #Only carry
    if cf!=None:
        if cf=="1":
            if cf_meter!=None:
                if cf_meter == "1":
                    to_db = LeaveAccrualPolicy( cf_u=cf_u , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                    to_db.save()
                    print("yeah done it!")
                    return render(request,'policy_page.html',locals())
                elif cf_meter == "2":
                    to_db = LeaveAccrualPolicy( cf_p=cf_p , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                    to_db.save()
                    print("yeah done it! carry percent")
                    return render(request,'policy_page.html',locals())
        elif cf=="2":
            if cf_meter!=None:
                if cf_meter=="1":
                    if ex_y_m=="2":
                        to_db = LeaveAccrualPolicy( ex_mth=ex_mth , ex_y_m=ex_y_m ,cf_u=cf_u , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                        to_db.save()
                        return render(request,'policy_page.html',locals())
                    elif ex_y_m=="1":
                        to_db = LeaveAccrualPolicy( ex_y = ex_y , ex_y_m=ex_y_m ,cf_u=cf_u , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                        to_db.save()
                        return render(request,'policy_page.html',locals())
                elif cf_meter == "2":
                    if ex_y_m=="2":
                        to_db = LeaveAccrualPolicy( ex_mth=ex_mth , ex_y_m=ex_y_m ,cf_p=cf_p , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                        to_db.save()
                        return render(request,'policy_page.html',locals())
                    elif ex_y_m=="1":
                        to_db = LeaveAccrualPolicy( ex_y = ex_y , ex_y_m=ex_y_m ,cf_p=cf_p , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                        to_db.save()
                        return render(request,'policy_page.html',locals())


        elif cf=="3":
            if cf_meter!=None:
                if cf_meter == "1":
                    to_db = LeaveAccrualPolicy( ovr_lmt=ovr_lmt,cf_u=cf_u , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                    to_db.save()
                    print("yeah done it with overall limit !")
                    return render(request,'policy_page.html',locals())
                elif cf_meter == "2":
                    to_db = LeaveAccrualPolicy( ovr_lmt=ovr_lmt,cf_p=cf_p , cf=cf, cf_meter=cf_meter ,effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
                    to_db.save()
                    print("yeah done it! carry percent with overall limit ")
                    return render(request,'policy_page.html',locals())







    to_db = LeaveAccrualPolicy(effective_after_no=eff, eff_yorm=yorm, ac_ndays=ac_ndays, ac_ndays_incre_decre=ac_ndays, policy_name=policy, ac_date=ac_date , ac_datm=ac_datm, ac_mth=ac_mth , user=User.objects.get(username=emp) ,emplyr_name=Employer.objects.get(emplyr_name=emplr))
    to_db.save()




    return render(request,'policy_page.html',locals())
