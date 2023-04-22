from emp_app import views
from django.conf.urls import url
from django.urls import path

app_name = 'emp_app'

urlpatterns = [
    # url(r'^$',views.IndexView.as_view()),
    url(r'^index/$',views.index,name='index'),
    url(r'^employer_form/$',views.employer_form,name='employer_form'),
    url(r'^employee_form/$',views.employee_form,name='employee_form'),
    url(r'^create_employer/$',views.create_employer,name='create_employer'),
    url(r'^create_employee/$',views.create_employee,name='create_employee'),
    url(r'^update_salary_page/$',views.update_salary_page,name='update_salary_page'),
    url(r'^update_salary_company/$',views.update_salary_company,name='update_salary_company'),
    url(r'^update_salary/$',views.update_salary,name='update_salary'),
    url(r'^display_company/$',views.display_company,name='display_company'),
    url(r'^show_employees/$',views.show_employees,name='show_employees'),
    url(r'^payroll/$',views.payroll,name='payroll'),
    url(r'^password/$',views.password,name='password'),
    url(r'secondpage/$',views.secondpage,name='secondpage'),
    url(r'apply_leave_page_and_show_status/$',views.apply_leave_page_and_show_status,name='apply_leave_page_and_show_status'),
    url(r'store_leave/$',views.store_leave,name='store_leave'),
    url(r'fromleavetohome/$',views.fromleavetohome,name='fromleavetohome'),
    url(r'show_leaves_to_manager/$',views.show_leaves_to_manager,name='show_leaves_to_manager'),
    url(r'approve_leaves/$',views.approve_leaves,name='approve_leaves'),
    url(r'fromapprovetohome/$',views.fromapprovetohome,name='fromapprovetohome'),
    url(r'policy/$',views.policy,name='policy'),
    path('accrual/',views.policy_page,name='policy_page'),
    # url(r'^$',views.EmployerListView.as_view(),name='emplist'),

]
