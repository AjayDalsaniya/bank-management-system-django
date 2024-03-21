
import django.conf
import django.db
from django.shortcuts import redirect, render
from django.http import request, HttpResponse
from myproject.settings import AUTH_PASSWORD_VALIDATORS
from .models import * 
import random
from django.db.models import Empty, Q
import time





named_tuple = time.localtime()
time_string = time.strftime("%d/%m/%y, %I:%M:%S",named_tuple)
# Create your views here.
#Admin 

#def  admin (request):

# admin add manager
def add_manager(request):
    return render(request,"bankingApp/admin/add_manager.html")

def add_manager_data(request):
    try:

        if request.POST:
            branch = request.POST['branch']
            branch =branch.upper()
            uid = User.objects.create(
            email = request.POST["email"],
            password = request.POST["password"],
            role = "Manager" ,
        )
        uid.save()
        
        mid = Branch.objects.create(
            user_id = uid,
            branch = branch,
            firstname = request.POST['firstname'],
            lastname = request.POST['lastname'],
            mobile_no = request.POST['mobile_no'],
            gender = request.POST['gender'],
            date = request.POST['date'],
            address = request.POST['address'],
            country = "India",
            state = request.POST['state'],
            city = request.POST['city'],
            pic = request.FILES['pic'],
        )
        mid.save()
        context = {
            "s_msg":"Add Manager successfully"
        }
        return render(request,'bankingApp/admin/add_manager.html',context)
    except:
        context = {
            "s_msg":"Details Fill Up"
        }
        return render(request,'bankingApp/admin/add_manager.html',context)
    
    
#admin all manager display 
def allmanager(request):
   mid = Branch.objects.all()
   context = {
       "mid":mid,
   } 
   return render(request,'bankingApp/admin/all_manager.html',context)

#manager view profile
def view_profile_manager(request,pk):
    mid = Branch.objects.get(id = pk)
    context = {
        "mid":mid,
    }
    return render(request,'bankingApp/admin/viewprofile_manager.html',context)


def Branch_Customer(request):
    return render(request,"bankingApp/admin/branch_customer.html")

#branch_cust_filter
def branch_cust_filter(request):
    try:
        if request.POST:
            branch = request.POST['branch']
                
            mid = Branch.objects.all()

        if branch:
            midfilter =mid.filter(Q(branch__icontains = branch))

        context = {
                'midfilter':midfilter,
                
            }
        return render (request,'bankingApp/admin/branch_customer.html',context)
    except:
        context = {
                "s_msg":"Account Number Fill up"
            }
        return render (request,'bankingApp/admin/branch_customer.html',context)

def view_cust_filter(request,pk):
    cid = Customer.objects.all()
   
    if pk:
        cidfilter = cid.filter(Q(mngid__icontains = pk))

    context = {
       "cidfilter":cidfilter, 
    }
    return render (request,'bankingApp/admin/branch_customer.html',context)


#----------------------------------------

# Manager $ Customer

def home (request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session["email"])
        if uid.role == "Manager":
            # Manager Panel
            mid = Branch.objects.get(user_id = uid)
            
            cust_data = Customer.objects.filter(mngid = mid.id)
           
           
            cust_count = Customer.objects.filter(mngid = mid.id).count()
            context = {
            "uid":uid,
            "mid":mid,
            "cust_data":cust_data,
            "cust_count":cust_count,

            }
         
            return render(request,"bankingApp/manager/index.html",context)
        elif uid.role == "Customer":
            # Customer Panel
            cid = Customer.objects.get(user_id = uid)
            call = Customer.objects.all()

            
            cust_count = Customer.objects.all().count()
           
            context = {
            "uid":uid,
            "cid":cid,
            "call":call,
            "cust_count":cust_count,
            
            }
            return render(request,"bankingApp/customer/customer_index.html",context)
        elif uid.role == "Admin":
            mngall = Branch.objects.all()
            mngcount = Branch.objects.all().count()
            context = {
                        "mngall":mngall,
                        "mngcount":mngcount,   
                    }
                    
            return render(request,'bankingApp/admin/admin-panel.html',context)
                
    else:
        return render(request,"bankingApp/authentication/login.html")

#login manager & customer
def login(request):
    # manager login
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
       
        mid = Branch.objects.get(user_id = uid)

       
            
        context = {
            "uid":uid,
            "mid":mid,
            

        }
        #return render(request,"bankingApp/manager/index.html",context)
        return redirect('home')
    else:
      
        if request.POST:
            email= request.POST["email"]
            password = request.POST["password"]
            try:
                uid = User.objects.get(email = email)

                if uid.email == email and uid.password == password:
                    if uid.role == "Manager":
                        mid = Branch.objects.get(user_id = uid)
                        request.session['email']=email
                        
                        context = {
                            'uid':uid,
                            'mid':mid,
                        }
                        #return render(request,"bankingApp/manager/index.html",context)
                        return redirect('home')
                    elif uid.role =="Customer":
                        #custommer
                        cid = Customer.objects.get(user_id = uid)
                        request.session['email'] = email
                        uid = "Customer"
                        context = {
                            'uid':uid,
                            'cid':cid,
                        }
                        #return render(request,"bankingApp/customer/customer_index.html",context)   
                        return redirect('home')
                    elif uid.role == "Admin":
                        request.session['email'] = email
                        aid = "Admin"
                        mngall = Branch.objects.all()
                        mngcount = Branch.objects.all().count()
                        context = {
                        "mngall":mngall,
                        "mngcount":mngcount,
                        "aid":aid,
                        
                        }
                        #return render(request,'bankingApp/admin/admin-panel.html',context)
                        return redirect('home')
                else:
                    msg = "Inavlid Email and Password"
                    context = {
                        'msg':msg,
                    }
                    return render(request,"bankingApp/login.html",context)
            except:
                msg = "Inavalid email And Password "
                context = {
                    'msg':msg,
                }
                return render(request,"bankingApp/authentication/login.html",context)

    return render(request,"bankingApp/authentication/login.html")

# logout
def logout(request):
    if "email" in request.session:
        del request.session['email']
        return render(request,"bankingApp/authentication/login.html")

def profile(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session["email"])
        mid = Branch.objects.get(user_id = uid)
        context = {
            "uid":uid,
            "mid":mid,

        }
        return render(request,"bankingApp/manager/profile.html",context)
    
def profile_password_change(request):
    if "email" in request.session:
        if request.POST:
            uid = User.objects.get(email = request.session["email"])
            mid = Branch.objects.get(user_id = uid)
            try:
                password = request.POST["password"]
                newpassword = request.POST["newpassword"]

                if password == uid.password:
                    uid.password = newpassword
                    uid.save()#save
                context = {
                    "uid":uid,
                    "mid":mid,

                }
                return render(request,"bankingApp/manager/profile.html",context) 
            except:
                context={
                    "uid":uid,
                    "mid":mid,
                    "s_msg":"Enter Details filup",
                }
                return render(request,"bankingApp/manager/profile.html",context) 
# Add customer for manager
def add_customer(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session["email"])
        mid = Branch.objects.get(user_id = uid)
        context = {
                "uid":uid,
                "mid":mid,

        }
        return render(request,'bankingApp/manager/add_customer.html',context)
    else:
        uid = User.objects.get(email = request.session["email"])
        mid = Branch.objects.get(user_id = uid)
        context = {
                "uid":uid,
                "mid":mid,

        }
        return render(request,'bankingApp/manager/add_customer.html',context)

def pic_profile(requsest):
    if "email" in requsest.session:
       uid = User.objects.get(email = requsest.session["email"])
       mid = Branch.objects.get(user_id = uid)
       try:
           if requsest.POST:
                email = requsest.POST["email"] 
                address = requsest.POST["address"]
                mngTpassword = requsest.POST["mngTpassword"]
                firstname = requsest.POST["firstname"]
                lastname = requsest.POST['lastname']
                country = requsest.POST['country']
                state = requsest.POST['state']
                city = requsest.POST['city']
                email = requsest.POST['email']
                
                uid.email=email
                uid.save()
                mid.mngTpassword = mngTpassword
                mid.firstname = firstname
                mid.lastname = lastname
                mid.country = country
                mid.state = state
                mid.city = city
                mid.address = address




                if  "profilepic" in requsest.FILES:
                    profile = requsest.FILES["profilepic"]
                    mid.pic = profile
                    mid.save()
                mid.save() 

                context = {
                    "uid":uid,
                    "mid":mid,
                }
                return render(requsest,'bankingApp/manager/profile.html',context)
       except Exception as e :
            print("....... e : ",e)
            context = {
                    "uid":uid,
                    "mid":mid,
                    "s_msg":"Details Fill Up"
                }
            return render(requsest,'bankingApp/manager/profile.html',context)
        
def add_bank_account(request):
    if "email" in request.session:
        try:
            if request.POST:
                uid = User.objects.get(email = request.session['email'])
                mid = Branch.objects.get(user_id = uid)
                accnum =random.randint(111111111111,999999999999)
                account_number = accnum
                ac1 = account_number
                
                #create Customer
                user_id = User.objects.create(
                    email = request.POST['email'],
                    password = request.POST['password'],
                    role= "Customer",
                    )
            
                
                
                cid  = Customer.objects.create(
                    user_id = user_id,
                    cust_no = account_number,
                    manager_id = mid,
                    mngid  = mid.id,
                    account_number = ac1,
                    firstname = request.POST["firstname"],
                    lastname = request.POST['lastname'],
                    mobile_no = request.POST['mobile_no'],
                    gender = request.POST['gender'],
                    date = request.POST['date'],
                    country = "india",
                    state = request.POST['state'],
                    city = request.POST['city'],
                    address = request.POST['address'],
                    signature = request.FILES['signature'],
                    pic = request.FILES['pic'],
                    
                )
                
                bid = Account.objects.create(
                    manager_id = mid,
                    customer_id = cid,
                    account_number = account_number,
                    account_type = request.POST['account_type'],
                    aadhar_card_number = request.POST['aadhar_card_number'],
                    pan_card_number = request.POST['pan_card_number'],
                    aadhar_card = request.FILES['aadhar_card'],
                    pan_card = request.FILES['pan_card'],
                    nominee_name = request.POST['nominee_name'],
                    nominee_relationship = request.POST['nominee_relationship'],

                )
                context = {
                    "uid":uid,
                    "mid":mid,
                    "bid":bid,
                    
                    
                    "s_msg" : "Successfully account created "
                }
                return render(request,"bankingApp/manager/add_customer.html",context)
            context = {
                    "uid":uid,
                    "mid":mid,
                }
            return render(request,'bankingApp/manager/add_customer.html',context)
        except Exception as e:
            print("............... e : ",e)
            context = {
                    "uid":uid,
                    "mid":mid,
                    "s_msg":"Details Fill Up"
                }
            return render(request,'bankingApp/manager/add_customer.html',context)


# display All Customer
def all_customers(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Branch.objects.get(user_id = uid)
        
        call = Customer.objects.all()
        
        context = {
                "uid":uid,
                "mid":mid,
                "call":call,
               
                
        }
        return render(request,'bankingApp/manager/all_customer.html',context)
# loan
# emi calculator

def emi(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Branch.objects.get(user_id = uid)
        context = {
                "uid":uid,
                "mid":mid,  
        }
        return render(request,'bankingApp/manager/emi.html',context)

def emi_calc(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Branch.objects.get(user_id = uid)
        try:
            if request.POST:
                amount = int(request.POST['amount'])
                rate = float(request.POST['rate'])
                periods = float(request.POST['periods'])

                total = amount*rate*periods/100
                total_emi = amount+total
                #month1 = periods*12
                month = total_emi/12
            

                rate = rate
                
                
                context = {
                    "amount":amount,
                    'total':total,
                    "rate" : rate,
                    "month":month,
                    "total_emi" :total_emi,
                    "uid":uid,
                    "mid":mid,  
                }
                return render(request,'bankingApp/manager/emi.html',context)
            context = {
                    "uid":uid,
                    "mid":mid,  
            }
            return render(request,'bankingApp/manager/emi.html',context)
        except Exception as e:
            
            context = {
                    "uid":uid,
                    "mid":mid, 
                    "s_msg":"Details Fill Up" 
            }
            return render(request,'bankingApp/manager/emi.html',context)



def loan(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Branch.objects.get(user_id = uid)
        
        call = Customer.objects.all()
        
        context = {
                "uid":uid,
                "mid":mid,
                "call":call,
               
                
        }
        return render(request,'bankingApp/manager/loan_customer.html',context)



def add_loan(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Branch.objects.get(user_id = uid)
        try:       
            if request.POST:
                account_number = int(request.POST['account_number'])
                loan_type = request.POST['loan_type']
                loan_amount = int(request.POST['loan_amount'])
                tranpassword = request.POST['tranpassword']
                
            
                periods =float(request.POST['periods'])

                #bid = Account.objects.get(customer_id = account_number)
                #tpassword = bid.tpassword

                
                #Home Loan
                if tranpassword == mid.mngTpassword and loan_type == "Home Loan" :
                    interest_rate = 4.5
                    #formula for loan
                    interest = loan_amount*interest_rate*periods/100
                    total_amount= loan_amount+interest
                    month1 = periods*12
                    monthli_amount = total_amount/month1

                
                    #create loan
                    cid  = Customer.objects.get(cust_no = account_number)
                    lid = Loan.objects.create(
                    manager_id = mid,
                    customer_id = cid,
                    
                    account_number = account_number,
                    loan_type = loan_type,
                    loan_amount = loan_amount,
                    interest_rate = interest_rate, 
                    periods = periods,
                    interest_amount = interest,
                    monthli_amount = monthli_amount,
                    totalAmount = total_amount,
                    loanDate = time_string,

                    )

                    #add amount for Account
                    bid  = Account.objects.get(customer_id = account_number)
                    balance = bid.balance

                    totalBalance = (balance+loan_amount)
                    bid.balance = totalBalance
                    bid.loanBalance = total_amount
                    bid.save()

                    #add payment
                    pid = paymentLoan.objects.create(
                        manager_id = mid,
                        customer_id =cid,
                        account_number = account_number,
                        loanBalance = total_amount,

                    )
                    pid.save()
                    


                    context = {
                        "uid":uid,
                        "mid":mid,
                        "lid":lid,
                        "cid":cid,
                        "s_msg":"successfull loan "
                        
                    }
                    return render(request,'bankingApp/manager/loan_customer.html',context)
                #Personal Loan
                elif tranpassword == mid.mngTpassword and loan_type == "Personal Loan" :
                    interest_rate = 6
                    #formula for loan
                    interest = loan_amount*interest_rate*periods/100
                    total_amount= loan_amount+interest
                    
                    month1 = periods*12
                    monthli_amount = total_amount/month1

                
                    #create loan
                    cid  = Customer.objects.get(cust_no = account_number)
                    lid = Loan.objects.create(
                    manager_id = mid,
                    customer_id = cid,
                    
                    account_number = account_number,
                    loan_type = loan_type,
                    loan_amount = loan_amount,
                    interest_rate = interest_rate, 
                    periods = periods,
                    interest_amount = interest,
                    monthli_amount = monthli_amount,
                    totalAmount = total_amount,
                    loanDate = time_string,

                    )

                    #add amount for Account
                    bid  = Account.objects.get(customer_id = account_number)
                    balance = bid.balance

                    totalBalance = (balance+loan_amount)
                    bid.balance = totalBalance
                    bid.loanBalance = total_amount
                    bid.save()

                    #add payment
                    pid = paymentLoan.objects.create(
                        manager_id = mid,
                        customer_id =cid,
                        account_number = account_number,
                        loanBalance = total_amount,

                    )
                    pid.save()
                 


                    context = {
                        "uid":uid,
                        "mid":mid,
                        "lid":lid,
                        "cid":cid,
                        "s_msg":"successfull loan "
                        
                    }
                    return render(request,'bankingApp/manager/loan_customer.html',context) 
            
            
                context = {
                        "uid":uid,
                        "mid":mid,

                        "s_msg":"Transaction Password Not Valid "
                        
                    }
                return render(request,'bankingApp/manager/loan_customer.html',context)
        except Exception as e:
            print("..... e ",e)
            context = {
                        "uid":uid,
                        "mid":mid,

                        "s_msg":"Detail Fill Up "
                        
                    }
            return render(request,'bankingApp/manager/loan_customer.html',context)



def Loan_Repayment(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Branch.objects.get(user_id = uid)
        context = {
                "uid":uid,
                "mid":mid,
            }
        return render(request,'bankingApp/manager/Repayment_loan.html',context)


def add_Repayment(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Branch.objects.get(user_id = uid)
        try:
            if request.POST:
                account_number = request.POST["account_number"]
                paymentAmount = int(request.POST["paymentAmount"])
                tranpassword = request.POST['tranpassword']

                cid  = Customer.objects.get(cust_no = account_number)
                bid  = Account.objects.get(customer_id = cid.cust_no)
                loanBalance1 = bid.loanBalance
                balance = bid.balance
                loanBalance2 = loanBalance1 - paymentAmount

                bid = Account.objects.get(customer_id = account_number)
                tpassword = bid.tpassword

                if (balance - paymentAmount) < 0:
                    
                    context = {
                        "uid":uid,
                        "mid":mid,  
                        "s_msg":"You don't have that much money in the bank ",  
                    }
                    return render(request,'bankingApp/manager/Repayment_loan.html',context)

                elif tranpassword == mid.mngTpassword and (loanBalance2 ) >= 0:
                    pid = paymentLoan.objects.create(
                        manager_id = mid,
                        customer_id = cid,
                        account_number = account_number,
                        paymentDate = time_string,
                        paymentAmount = paymentAmount,
                        loanBalance = loanBalance2,
                    )
                


                    pid.save()
                    bid.save()
                
                    #Account
                    bid = Account.objects.get(customer_id = cid)
                    balance = bid.balance
                    loanBalance = bid.loanBalance

                    bid.balance = balance-paymentAmount
                    bid.loanBalance = loanBalance-paymentAmount
                    bid.save()

                    context = {
                        "uid":uid,
                        "mid":mid,  
                        "s_msg":"successfull Payment     ",  
                    }
                    return render(request,'bankingApp/manager/Repayment_loan.html',context)
                elif loanBalance1 == 0:
                    context = {
                        "uid":uid,
                        "mid":mid,

                        "s_msg":"No Loan "
                        
                    }
                    return render(request,'bankingApp/manager/Repayment_loan.html',context)

                context = {
                        "uid":uid,
                        "mid":mid,

                        "s_msg":"Transaction Password Not Valid "
                        
                    }
                return render(request,'bankingApp/manager/Repayment_loan.html',context)
        except:
            context = {
                        "uid":uid,
                        "mid":mid,

                        "s_msg":"Deatail Fill Up "
                        
                    }
            return render(request,'bankingApp/manager/Repayment_loan.html',context)



#loan passbook
def loan_passbook(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Branch.objects.get(user_id = uid)
        cid = Customer.objects.get(cust_no = pk)
        bid = Account.objects.get(customer_id = cid.cust_no)
        pid  = paymentLoan.objects.all()  
        lid = Loan.objects.get(account_number = cid.cust_no)  
        

        if cid.cust_no:
            pid =pid.filter(Q(account_number__icontains = cid.cust_no))    


        context = {
            'uid':uid,
            'mid':mid,
            'cid':cid,
            'pid':pid,
            'bid':bid,
            'lid':lid,
        }
        return render(request,"bankingApp/manager/loan_passbook.html",context)

def loan_View(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Branch.objects.get(user_id = uid)
        try:
            #lid = Loan.objects.get(customer_id = pk)
            lid = Loan.objects.all()
            if pk:
                lidfilter =lid.filter(Q(account_number__icontains = pk))
            context = {
                        "uid":uid,
                        "mid":mid,    
                        "lid":lid,
                        "lidfilter":lidfilter,
                            }
            return render(request,'bankingApp/manager/loan_view.html',context)
        except:
            context = {
                        "uid":uid,
                        "mid":mid,    
                        "msg":"No Loan",
                        
                            }
            return render(request,'bankingApp/manager/loan_view.html',context)

        
# only one customer display
def view_customer(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Branch.objects.get(user_id = uid)
        
        call = Customer.objects.all()
        
        context = {
                "uid":uid,
                "mid":mid,
                "call":call,
               
                
        }
        return render(request,'bankingApp/manager/managerviewcustomer.html',context)

def filter(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Branch.objects.get(user_id = uid)    
        try:
            if request.POST:
                accno = request.POST['accno']
                
                cid = Customer.objects.all()

            if accno:
                cidfilter =cid.filter(Q(account_number__icontains = accno))

            context = {
                'cidfilter':cidfilter,
                'uid':uid,
                'mid':mid,
            }
            return render (request,'bankingApp/manager/managerviewcustomer.html',context)
        except:
            context = {
                
                'uid':uid,
                'mid':mid,
                "s_msg":"Account Number Fill up"
            }
            return render (request,'bankingApp/manager/managerviewcustomer.html',context)


def view_profile(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Branch.objects.get(user_id = uid)
              
        cid = Customer.objects.get(cust_no=pk)
        bid = Account.objects.get(customer_id = cid.cust_no)
       
        context = {
                    "uid":uid,
                    "mid":mid,    
                    "cid":cid,
                    "bid":bid,
                        }
        return render(request,'bankingApp/manager/viewprofile.html',context)
        



def edit_customers_function(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Branch.objects.get(user_id = uid)
        
        
        customer_edit = Customer.objects.get(cust_no=pk)
        bacc = Account.objects.get(customer_id = customer_edit.cust_no)
        context = {
                "uid":uid,
                "mid":mid,
                
                "customer_edit":customer_edit,
                "bacc":bacc,
                
        }
        return render(request,'bankingApp/manager/edit_customer.html',context)
    
def update_customers_function(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        #id = uid.id


        mid = Branch.objects.get(user_id = uid)
        
        if request.POST:
            
            cbid = request.POST['accno']
            password = request.POST['password']
            newpassword = request.POST['newpassword']
            id = request.POST['id']
            tranpassword = request.POST['tranpassword']
            
            
         
            uid1 = User.objects.get(id = int(id))
           
            #customer Login Password 
            if uid1.password == password:
                uid1.password = newpassword
                uid1.save()
                """cid = Customer.objects.get(cust_no=cbid)
                bid = Account.objects.get(customer_id= cid.cust_no)"""
                context = {
                "uid":uid,
                "mid":mid,
                "s_msg" : "Password success ",
                }
                return render(request,'bankingApp/manager/edit_customer.html',context)
            
            
                """if uid1.password == app_password:
                                        bid.tpassword = tranpassword
                                        bid.save()
                                    uid1.save()""""""if uid1.password != app_password:
                            context = {
                            "uid":uid,
                            "mid":mid,
                            "s_msg" : "Application Password Not Valid ",
                            }
                            return render(request,'bankingApp/manager/edit_customer.html',context)"""
            
            elif mid.mngTpassword == tranpassword:
                try:
                    cid = Customer.objects.get(cust_no=cbid)
                    bid = Account.objects.get(customer_id= cid.cust_no)
                    if mid.mngTpassword == tranpassword:
                        cid.firstname = request.POST["firstname"]
                        cid.lastname = request.POST['lastname']
                        cid.mobile_no = request.POST['mobile_no']
                        cid.gender = request.POST['gender']
                        cid.date = request.POST['date']
                                
                        cid.state = request.POST['state']
                        cid.city = request.POST['city']
                        cid.address = request.POST['address']
                        if 'pic' in request.FILES:
                            cid.pic = request.FILES['pic']

                        cid.save()
                        
                        context = {
                            "uid":uid,
                            "mid":mid,
                            "s_msg" : "Account Details updated ",
                        }
                        return render(request,'bankingApp/manager/edit_customer.html',context)
                except:
                    context = {
                    "uid":uid,
                    "mid":mid,
                    "s_msg" : " Details Fillup ",
                    }
                    return render(request,'bankingApp/manager/edit_customer.html',context)
            context = {
                "uid":uid,
                "mid":mid,
                "s_msg" : "Details Fillup",
            }
            return render(request,'bankingApp/manager/edit_customer.html',context)

        context={
            "uid":uid,
            "mid":mid,
            }
        return render(request,"BankingApp/manager/add_customer.html",context)
             
def delete_customers_function(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Branch.objects.get(user_id = uid)

        cid = Customer.objects.get(cust_no = pk)
        cid.delete()

        call =Customer.objects.all()

        context = {
            'uid':uid,
            'mid':mid,
            'call':call,
        }
        return render(request,"bankingApp/manager/all_customer.html",context)
            
def transaction(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Branch.objects.get(user_id = uid)
        cid = Customer.objects.get(cust_no = pk)
        context = {
            'uid':uid,
            'mid':mid,
            'cid':cid,

        }
        return render(request,"bankingApp/manager/transcation.html",context)

def deposit_withdraw(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Branch.objects.get(user_id = uid)

        try:
            if request.POST:
            
                custno = int(request.POST['custno'])
                
                print("cust_no : ",custno)
                title = request.POST['title']
                transcations_type = request.POST['transcation_type']
                tpassword = request.POST['tpassword']
                amount = request.POST['amount']
                #type cast 
                amount = int(amount)

                cid = Customer.objects.get(cust_no = custno)
                bid = Account.objects.get(customer_id = cid)
                withdrw = bid.balance
                tpassword1 = bid.tpassword
                bid.save()

                
                if  tpassword != mid.mngTpassword:
                    msg = "Transaction Failed"
                    context = {
                        'cid':cid,
                        'bid':bid,
                        'uid':uid,
                        'mid':mid,
                        'msg':msg,
                        
                    }
                    return render(request,"bankingApp/manager/transcation.html",context)
                

                
                elif transcations_type == "Deposit"and tpassword == mid.mngTpassword :
                 
                    tid = Transcations.objects.create(bank_id = bid,
                                                    user_id = uid,
                                                    customer_id = cid,
                                                    account_number = custno,
                                                    title = title,
                                                    transcations_type = transcations_type,
                                                    amount = amount,
                                                    created_at = time_string
                                                    )
                    tid.save()

                   
                    amount = int(request.POST['amount'])
         
                    bid  = Account.objects.get(customer_id  = custno)
                
                    balance = bid.balance
                    total_balance = (balance + amount)

                    bid.balance = total_balance
                    bid.save()

                    msg = "Deposit Successfull "
                    context = {
                        'cid':cid,
                        'bid':bid,
                        'uid':uid,
                        'mid':mid,
                        'msg':msg,
                        
                    }
                    return render(request,"bankingApp/manager/transcation.html",context)
                
                elif transcations_type == "Withdraw" and (withdrw - amount) >=500 and tpassword ==mid.mngTpassword:
                    cid = Customer.objects.get(cust_no = custno)
                    bid = Account.objects.get(customer_id = cid.cust_no)
             
                    tid = Transcations.objects.create(bank_id = bid,
                                                    user_id = uid,
                                                    customer_id = cid,
                                                    account_number = custno,
                                                    title = title,
                                                    transcations_type = transcations_type,
                                                    amount = amount,
                                                     created_at = time_string
                                                    
                                                    )
                    tid.save()

                 
                    amount = int(request.POST['amount'])
                    
                    bid  = Account.objects.get(customer_id  = custno)
                
                    balance = bid.balance

                    total_balance = (balance - amount)
                    
                    bid.balance = total_balance
                    bid.save()

                    msg = "withdraw Successfull "
                    context = {
                        'cid':cid,
                        'bid':bid,
                        'uid':uid,
                        'mid':mid,
                        'msg':msg,
                    }
                    return render(request,"bankingApp/manager/transcation.html",context)
                
                else:
                    cid = Customer.objects.get(cust_no = custno)
                    bid = Account.objects.get(customer_id = cid.cust_no)
                    msg = "You don't have that much money in the bank "
                    context = {
                        'cid':cid,
                        'bid':bid,
                        'uid':uid,
                        'mid':mid,
                        'msg':msg,
                    }
                    return render(request,"bankingApp/manager/transcation.html",context)

        except Exception as e:
            print("........     e : ",e)
            msg = "Details Fillup "
            cid = Customer.objects.get(cust_no = custno)
            bid = Account.objects.get(customer_id = cid.cust_no)
            context = {
                        'cid':cid,
                        'bid':bid,
                        'uid':uid,
                        'mid':mid,
                        'msg':msg,
                    }
            return render(request,"bankingApp/manager/transcation.html",context)
        

def Passbook(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Branch.objects.get(user_id = uid)
        cid = Customer.objects.get(cust_no = pk)
        bid = Account.objects.get(customer_id = cid.cust_no)
        tid = Transcations.objects.all()
        if cid.cust_no:
            tid =tid.filter(Q(account_number__icontains = cid.cust_no))

        context = {
            'uid':uid,
            'mid':mid,
            'cid':cid,
            'tid':tid,
            'bid':bid,
        }
        return render(request,"bankingApp/manager/passbook.html",context)
    
def transfer_money(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Branch.objects.get(user_id = uid)
        
        context = {
                "uid":uid,
                
                'mid':mid,

            }
        return render(request,"bankingApp/manager/transferamount.html",context)
    
def TRANFER_MONEY1(request):
    if 'email' in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Branch.objects.get(user_id = uid)
        
        try:
            if request.POST:
                YourAccountNum = int(request.POST['YourAccountNum'])
                TransferAccountNum = int(request.POST['TransferAccountNum'])
                title = request.POST['title']
                tpassword = request.POST['tpassword']

                #account_number2 = int(account_number2)
                amount = int(request.POST['amount'])
                cid = Customer.objects.get(cust_no= YourAccountNum)
                bid  = Account.objects.get(customer_id = YourAccountNum)
                bidbalance = bid.balance
                
                #tpassword1 = bid.tpassword

                    
                
                if mid.mngTpassword != tpassword:
                    msg="Transcation Password Not valid"
                    context = {
                            "uid":uid,
                            "bid":bid,
                            'mid':mid,
                            'msg':msg,
                    }
                    return render(request,"bankingApp/manager/transferamount.html",context)
                    

                #elif (bidbalance - amount)>=500 and mid.mngTpassword == tpassword and bid.customer_id == TransferAccountNum:
                elif (bidbalance - amount)>=500 and mid.mngTpassword == tpassword :
                        bid  = Account.objects.get(customer_id = YourAccountNum)
                        balance = bid.balance
                        balance1 = (balance - amount)
                        bid.balance = balance1
                        bid.save()
                        
                        bid = Account.objects.get(customer_id = TransferAccountNum)
                        balance = bid.balance
                        balance1 = (balance + amount)
                        bid.balance = balance1
                        bid.save()
                        tarnfer = "Tranfer To "+str(TransferAccountNum)
                        #if condition
                        
                        tid = Transcations.objects.create(bank_id = bid,
                                                                user_id = uid,
                                                                customer_id = cid,
                                                                account_number = YourAccountNum,
                                                                title = title,
                                                                transcations_type =tarnfer ,
                                                                amount = amount,
                                                                created_at = time_string
                                                                )
                        tid.save()

                        tarnfer = "Credit To "+str(YourAccountNum)
                        tid = Transcations.objects.create(bank_id = bid,
                                                                user_id = uid,
                                                                customer_id = cid,
                                                                account_number = TransferAccountNum,
                                                                title = title,
                                                                transcations_type =tarnfer,
                                                                amount = amount,
                                                                created_at = time_string
                                                                )
                        tid.save()
                        
                        msg="Transfer successfull"
                        context = {
                            "uid":uid,
                            "bid":bid,
                            'mid':mid,
                            'msg':msg,
                        }
                        return render(request,"bankingApp/manager/transferamount.html",context)
                else:
                    msg = "You don't have that much money in the bank "
                    context = {
                            "uid":uid,
                            "bid":bid,
                            'mid':mid,
                            'msg':msg,

                    }
                    return render(request,"bankingApp/manager/transferamount.html",context)
                
        except:
            context = {
                        "uid":uid,
                        
                        'mid':mid,
                        'msg':"Details Fill Up",

                }
            return render(request,"bankingApp/manager/transferamount.html",context)



#=========================================================================================    
#customer
def custpassbook(request):
    if 'email' in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Customer.objects.get(user_id = uid)
        bid  = Account.objects.get(customer_id = cid.cust_no)
        tid  = Transcations.objects.all()
        if cid.cust_no:
            tid =tid.filter(Q(account_number__icontains = cid.cust_no))
        context={
            'uid':uid,
            'cid':cid,
            'bid':bid,
            'tid':tid,

        }

        return render(request,"bankingApp/customer/customerpassbook.html",context)
    

def cust_profile(request):
    if 'email' in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Customer.objects.get(user_id = uid)
        bid  = Account.objects.get(customer_id = cid.cust_no)
        context={
            'uid':uid,
            'cid':cid,
            'bid':bid,
        }
        return render(request,"bankingApp/customer/customerprofile.html",context)

def cust_profile_password_change(request):
    if 'email' in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Customer.objects.get(user_id = uid)
        bid  = Account.objects.get(customer_id = cid.cust_no)
        
        try:
            if request.POST:
                    
                password = request.POST["password"]
                newpassword = request.POST["newpassword"]
                tpassword = request.POST["tpassword"]
                bid.tpassword = tpassword
                bid.save()
                if password == uid.password:
                    uid.password = newpassword
                    uid.save()#save
                context = {
                            "uid":uid,
                            "bid":bid,
                            'cid':cid,

                        }
                return render(request,"bankingApp/customer/customerprofile.html",context)
        except:
            context = {
                        "uid":uid,
                        "bid":bid,
                        'cid':cid,
                        "msg":"details Fill Up"
                        }
            return render(request,"bankingApp/customer/customerprofile.html",context)

        


def custTransfer(request):
    if 'email' in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Customer.objects.get(user_id = uid)
        bid  = Account.objects.get(customer_id = cid.cust_no) 
        context = {
                "uid":uid,
                "bid":bid,
                'cid':cid,

            }
        return render(request,"bankingApp/customer/customertransferamount.html",context)

def transfer_amount(request):
     if 'email' in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Customer.objects.get(user_id = uid)
        
        try:
            if request.POST:
                accno = request.POST['accno']
                account_number2 = request.POST['account_number2']
                title = request.POST['title']
                tpassword = request.POST['tpassword']

                #account_number2 = int(account_number2)
            
           
                amount = int(request.POST['amount'])
                bid  = Account.objects.get(customer_id = accno)
                bidbalance = bid.balance
                tpassword1 = bid.tpassword
                
                if tpassword1 != tpassword:
                    msg="Transcation Password not valid"
                    context = {
                        "uid":uid,
                        "bid":bid,
                        'cid':cid,
                        'msg':msg,
                    }
                    return render(request,"bankingApp/customer/customertransferamount.html",context)
                    

                elif (bidbalance - amount)>=500 and tpassword1 == tpassword :
                    bid  = Account.objects.get(customer_id = accno)
                    print("-------bid : ",bid)
                    yourbalance = bid.balance
                    balance = (yourbalance - amount)
                    bid.balance = balance
                    bid.save()

                    bid = Account.objects.get(customer_id = account_number2)
                    balance = bid.balance
                    balance1 = (balance + amount)
                    bid.balance = balance1
                    bid.save()
                    tarnfer = "Tranfer To "
                    #if condition
                    
                    tid = Transcations.objects.create(bank_id = bid,
                                                            user_id = uid,
                                                            customer_id = cid,
                                                            account_number = accno,
                                                            title = title,
                                                            transcations_type =tarnfer + account_number2,
                                                            amount = amount,
                                                            created_at = time_string
                                                            )
                    tid.save()

                    tarnfer = "Credit To "
                    tid = Transcations.objects.create(bank_id = bid,
                                                            user_id = uid,
                                                            customer_id = cid,
                                                            account_number = account_number2,
                                                            title = title,
                                                            transcations_type =tarnfer + accno,
                                                            amount = amount,
                                                            created_at = time_string
                                                            )
                    tid.save()
                    
                    msg="Transfer successfull"
                    context = {
                        "uid":uid,
                        "bid":bid,
                        'cid':cid,
                        'msg':msg,
                    }
                    return render(request,"bankingApp/customer/customertransferamount.html",context)
                else:
                    msg = "You don't have that much money in the bank "
                    context = {
                        "uid":uid,
                        "bid":bid,
                        'cid':cid,
                        'msg':msg,

                    }
                    return render(request,"bankingApp/customer/customertransferamount.html",context)
            
        except:
            context = {
                        "uid":uid,
                        
                        'cid':cid,
                        'msg':"No Tranfer Amount",

                }
            return render(request,"bankingApp/customer/customertransferamount.html",context)

def Loan_Repayment_cust(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Customer.objects.get(user_id = uid)
       
        context = {
                "uid":uid,
                "cid":cid,
            }
        return render(request,'bankingApp/customer/Repayment_loan_cust.html',context)
def add_Repayment_cust(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        
        cid = Customer.objects.get(user_id = uid)
        mid = cid.manager_id
        try:
            if request.POST:
                account_number = request.POST["account_number"]
                paymentAmount = int(request.POST["paymentAmount"])
                tranpassword = request.POST['tranpassword']

                cid  = Customer.objects.get(cust_no = account_number)
                bid  = Account.objects.get(customer_id = cid.cust_no)
                loanBalance1 = bid.loanBalance
                balance = bid.balance
                loanBalance2 = loanBalance1 - paymentAmount

                bid = Account.objects.get(customer_id = account_number)
                tpassword = bid.tpassword

                if (balance - paymentAmount) < 0:
                    
                    context = {
                        "uid":uid,
                        "mid":mid,  
                        "s_msg":"You don't have that much money in the bank ",  
                    }
                    return render(request,'bankingApp/customer/Repayment_loan_cust.html',context)
                if tranpassword == tpassword and loanBalance2 > 0:
                    pid = paymentLoan.objects.create(
                        manager_id = mid,
                        customer_id = cid,
                        account_number = account_number,
                        paymentDate = time_string,
                        paymentAmount = paymentAmount,
                        loanBalance = loanBalance2,
                    )

                    pid.save()
                    bid.save()
                
                    #Account
                    bid = Account.objects.get(customer_id = cid)
                    balance = bid.balance
                    loanBalance = bid.loanBalance

                    bid.balance = balance-paymentAmount
                    bid.loanBalance = loanBalance-paymentAmount
                    bid.save()

                    context = {
                        "uid":uid,
                        "cid":cid,  
                        "s_msg":"successfull Payment     ",  
                    }
                    return render(request,'bankingApp/customer/Repayment_loan_cust.html',context)
                context = {
                        "uid":uid,
                        "cid":cid, 
                        "s_msg":"Transaction Password Not Valid "                        
                    }
                return render(request,'bankingApp/customer/Repayment_loan_cust.html',context)
        except Exception as e:
            print("........e : ",e)
            context = {
                        "uid":uid,
                        "cid":cid, 
                        "s_msg":"Reapayment Failed "                        
                    }
            return render(request,'bankingApp/customer/Repayment_loan_cust.html',context)


def loan_passbook_cust(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
       
        cid = Customer.objects.get(cust_no = pk)
        bid = Account.objects.get(customer_id = cid.cust_no)
        pid  = paymentLoan.objects.all()    
        if cid.cust_no:
            pid =pid.filter(Q(account_number__icontains = cid.cust_no))    

        context = {
            'uid':uid,
            
            'cid':cid,
            'pid':pid,
            'bid':bid,
        }
        return render(request,"bankingApp/customer/loan_passbook_cust.html",context)

def Loan_details_cust(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Customer.objects.get(user_id = uid)
        try:
            lid  = Loan.objects.get(customer_id = pk )

            context = {
                "uid":uid,
                "cid":cid,
                "lid":lid,
                
            }
            return render (request,"bankingApp/customer//loan_view_cust.html",context)
        except:
            context = {
                "uid":uid,
                "cid":cid,
                
                "msg":"No Loan",    
                
            }
            return render (request,"bankingApp/customer//loan_view_cust.html",context)

    
def Dashboard(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Customer.objects.get(user_id = uid)
     
        call = Customer.objects.all()
        context = {
            "uid":uid,
            "cid":cid,
            "call":call,
        }
        return render (request,"bankingApp/customer/dashboard.html",context)
    
def emi_cust(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Customer.objects.get(user_id = uid)
     
        
        context = {
            "uid":uid,
            "cid":cid,
            
        }
        return render (request,"bankingApp/customer/emi_cust.html",context)

def emi_calc_cust(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Customer.objects.get(user_id = uid)
        try:
            if request.POST:
                amount = int(request.POST['amount'])
                rate = float(request.POST['rate'])
                periods = float(request.POST['periods'])

                total = amount*rate*periods/100
                total_emi = amount+total
                #month1 = periods*12
                month = total_emi/12
            

                rate = rate
                
                
                context = {
                    "amount":amount,
                    'total':total,
                    "rate" : rate,
                    "month":month,
                    "total_emi" :total_emi,
                    "uid":uid,
                    "cid":cid,  
                }
                return render(request,'bankingApp/customer/emi_cust.html',context)


            context = {
                    "uid":uid,
                    "cid":cid,  
            }
            return render(request,'bankingApp/customer/emi_cust.html',context)
        except Exception as  e:
            print("--------- e : ",e)
            context = {
                    "uid":uid,
                    "cid":cid, 
                    "s_msg": "Details Fill up", 
            }
            return render(request,'bankingApp/customer/emi_cust.html',context)
            
#App Password 
def app_password(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Customer.objects.get(user_id = uid)

        context = {
                    "uid":uid,
                    "cid":cid, 
                    
            }
        return render(request,'bankingApp/customer/app_password.html',context)
def change_password(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Customer.objects.get(user_id = uid)
        try:
            if request.POST:
                id = request.POST['id']
                password = request.POST['password']
                newpassword = request.POST['newpassword']

                uidpass = User.objects.get(id = id)
                if  uidpass.password != password:
                    context = {
                    "uid":uid,
                    "cid":cid,
                    "msg":"Password Not Succsessfull ",
                    }
                    return render(request,'bankingApp/customer/app_password.html',context)

                else:
                    uidpass.password == password
                    uidpass.password = newpassword

                uidpass.save()

                context = {
                    "uid":uid,
                    "cid":cid,
                    "msg":"Password Succsessfull ",
                }
                return render(request,'bankingApp/customer/app_password.html',context)
            context = {
                    "uid":uid,
                    "cid":cid,
                    "msg":"Password Not Succsessfull ",
                }
            return render(request,'bankingApp/customer/app_password.html',context)
        except:
            context = {
                    "uid":uid,
                    "cid":cid,
                    "msg":"Details Fill UP ",
                }
            return render(request,'bankingApp/customer/app_password.html',context)

    
def tra_password(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Customer.objects.get(user_id = uid)
        bid = Account.objects.get(customer_id = pk)
        context = {
                    "uid":uid,
                    "cid":cid, 
                    "bid":bid,
                    
            }
        return render(request,'bankingApp/customer/transaction_password.html',context)
    
def tran_change_password(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Customer.objects.get(user_id = uid)
        try:
            if request.POST:
                id = request.POST['id']
                password = request.POST['password']
                newpassword = request.POST['newpassword']

                bidtpass = Account.objects.get(customer_id = id)
                if  bidtpass.tpassword != password:
                    context = {
                    "uid":uid,
                    "cid":cid,
                    "msg":"Password Not Succsessfull ",
                    }
                    return render(request,'bankingApp/customer/transaction_password.html',context)

                else:
                    bidtpass.tpassword == password
                    bidtpass.tpassword = newpassword

                bidtpass.save()

                context = {
                    "uid":uid,
                    "cid":cid,
                    "msg":"Password Succsessfull ",
                }
                return render(request,'bankingApp/customer/transaction_password.html',context)
            context = {
                    "uid":uid,
                    "cid":cid,
                    "msg":"Password Not Succsessfull ",
                }
            return render(request,'bankingApp/customer/transaction_password.html',context)
        except:
            context = {
                    "uid":uid,
                    "cid":cid,
                    "msg":"Details Fill Up ",
                }
            return render(request,'bankingApp/customer/transaction_password.html',context)

                
