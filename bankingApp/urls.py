"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    #Admin
    #path('adminlogin', views.admin, name='admin'),
    #path('admin-login', views.admin_login, name='admin-login'),
    
    #path('admin', views.admin, name='admin'),
    #Add Maneger
    path('add-manager', views.add_manager, name='add-manager'), 
    path('add-manager-data', views.add_manager_data, name='add-manager-data'),

    #All Manager 
    path('allmanager', views.allmanager, name='allmanager'),

    #Branch-Customer
    path('Branch-Customer',views.Branch_Customer,name="Branch-Customer"),

    #Branch-Customer-filter
    path('branch-cust-filter',views.branch_cust_filter,name="branch-cust-filter"),

    #view-cust-filter
    path('view-cust-filter/<int:pk>/',views.view_cust_filter,name="view-cust-filter"),

    #Manager Details
    path('view-profile-manager/<int:pk>/',views.view_profile_manager,name="view-profile-manager"),
#-------------------------------------------------------------
#manager
   path('', views.home, name='home'),
   #path('register/', views.register, name='register'),
   path('login/',views.login, name="login1"),
   path('logout/', views.logout,name="logout"),
   path('profile/',views.profile,name="profile"),
   path('profile-password-change/',views.profile_password_change, name="profile-password-change"),
   path('addcustomer/',views.add_customer,name="addcustomer"),
   path('pic-profile/',views.pic_profile,name="pic-profile"),
   path('add-bank-account/',views.add_bank_account, name="add-bank-account"),
   path('allcustomers/',views.all_customers,name="all-customer"),
   path('view-customer/',views.view_customer,name="view-customer"),
   path('view-profile/<int:pk>/',views.view_profile,name="view-profile"),
   path('edit-customer/<int:pk>/', views.edit_customers_function, name="edit-customer"),
   path('update-customer/', views.update_customers_function, name="update-customer"),
   path('delete-customer/<int:pk>/', views.delete_customers_function, name="delete-customer"),
   
   path('transaction/<int:pk>/', views.transaction, name="transaction"),
   path('deposit/',views.deposit_withdraw,name="deposit"),
   path('Passbook/<int:pk>/',views.Passbook,name="passbook"),
  
   path('filter/',views.filter,name="filter"),
   #loan
   path('loan/',views.loan,name="loan"),
   path('add-loan/',views.add_loan,name="add-loan"),
   
   path("Loan-Repayment/",views.Loan_Repayment,name="Loan-Repayment"),
   path('add-Repayment/',views.add_Repayment,name="add-Repayment"),

   #loan filter
   path("loan-passbook/<int:pk>/",views.loan_passbook,name="loan-passbook"),

   path("loan-View/<int:pk>",views.loan_View,name="loan-View"),

   #emi calculator
   path('emi-calculator',views.emi,name="emi"),
   path('emi-calc/',views.emi_calc,name="emi-calc"),

   path('transfer-money/',views.transfer_money,name="transfer-money"),
   path('transfer-money1/',views.TRANFER_MONEY1,name="TRANFER-MONEY1"),

#------------------------------------------------------------------------------------------------------

   #customer

   path("Dashboard/",views.Dashboard,name="Dashboard"),
   
    #loan
   path("Loan-Repayment-cust/",views.Loan_Repayment_cust,name="Loan-Repayment-cust"),
   path('add-Repayment-cust/',views.add_Repayment_cust,name="add-Repayment-cust"),
   path("loan-passbook-cust/<int:pk>/",views.loan_passbook_cust,name="loan-passbook-cust"),
   path('Loan-details-cust/<int:pk>/',views.Loan_details_cust,name="Loan-details-cust"),
   path('emi-cust/',views.emi_cust,name="emi-cust"),
   path('emi-calc-cust/',views.emi_calc_cust,name="emi-calc-cust"),


   path('custpassbook/',views.custpassbook,name="custpassbook"),
   path('cust-profile/',views.cust_profile,name="cust-profile"),
   path('cust-profile-password-change/',views.cust_profile_password_change,name="cust-profile-password-change"),
   path('custTransfer/',views.custTransfer, name="custTransfer",),
   path('transfer-amount/',views.transfer_amount,name="transfer-amount"),

   #App Password 
   path('app-password/',views.app_password,name="app-password"),
   path("change-password/",views.change_password,name="change-password"),

   #Transcation Password
   path('tra-password/<int:pk>/',views.tra_password,name="tra-password"),
   path('tran-change-password/',views.tran_change_password,name="tran-change-password"),


   




  
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)