"""emp_salary_payments URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from emp_app import views
from django.conf.urls import url,include

urlpatterns = [
    # url(r'^$',views.IndexView.as_view()),
    url(r'^$',views.login,name='login'),
    # url(r'^$',views.index,name='index'),
    path('admin/', admin.site.urls),
    url(r'^emp_app/',include('emp_app.urls')),
    # url(r'^$',views.EmployerListView.as_view(),name='emplist'),

    ###########
    path('accrual/',views.policy_page,name='policy_page'),

]
