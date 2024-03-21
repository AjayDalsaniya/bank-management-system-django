from django.db import models


# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True,max_length=30)
    password = models.CharField(max_length=30)
    role = models.CharField(max_length=30)
    created_at= models.DateTimeField(auto_now_add=True,blank=False)
    update_at = models.DateTimeField(auto_now=True,blank=False)

    def __str__(self):
        return self.email
    
    

# bank manager table 
class Branch(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    
    branch = models.CharField(max_length=30)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    mobile_no = models.CharField(max_length=30)
    address = models.CharField(max_length=60)
    gender = models.CharField(max_length=30,null=True)
    date = models.CharField(max_length=20,null=True)
    country = models.CharField(max_length=30,null=True)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=20,null=True)
    pic = models.FileField(upload_to="media/manager/",default="media/manager.png")
    mngTpassword = models.CharField(max_length=30,null=True)
    def __str__(self):
        return self.firstname
   
    

# customer table
class Customer(models.Model):
    cust_no = models.BigIntegerField(primary_key = True, default=None)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    manager_id = models.ForeignKey(Branch,on_delete=models.CASCADE,null=True)
    mngid = models.CharField(max_length=30,null=True)
    account_number = models.CharField(max_length=30,null=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    mobile_no = models.CharField(max_length=30)
    gender = models.CharField(max_length=20)
    date = models.CharField(max_length=20,null=True)
    country = models.CharField(max_length=30,default="India",null=True) 
    state = models.CharField(max_length=30,null=True)
    city = models.CharField(max_length=30)
    address = models.TextField()
    signature = models.FileField(upload_to="media/signature/",default="media/manager.png")

    pic = models.FileField(upload_to="media/customer/",default="media/manager.png")

    def __str__(self):
        return self.account_number

class Account(models.Model):
    manager_id = models.ForeignKey(Branch,on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
    account_type = models.CharField(max_length=30)
    account_number = models.CharField(max_length=30,null=True) 
    aadhar_card_number = models.CharField(max_length=16)
    pan_card_number = models.CharField(max_length=16)
    aadhar_card = models.FileField(upload_to="media/images/",default="media/no-image.png")
    pan_card = models.FileField(upload_to="media/images/",default="media/no-image.png")
    nominee_name = models.CharField(max_length=30)
    nominee_relationship = models.CharField(max_length=30)
    balance = models.IntegerField(default=500)
    loanBalance = models.IntegerField(null=True)
    tpassword = models.CharField(max_length=300,null=True)

    def __str__(self):
        return self.account_number

class Transcations(models.Model):
    bank_id = models.ForeignKey(Account,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    tpassword = models.CharField(max_length=300)
    account_number = models.CharField(max_length=30,null=True)
    title = models.CharField(max_length=60)
    transcations_type = models.CharField(max_length=60)
    amount = models.IntegerField(default=500)
    created_at= models.CharField(max_length=60)
    def __str__(self):
        return self.account_number

 
class Loan(models.Model):
   manager_id = models.ForeignKey(Branch,on_delete=models.CASCADE)
   customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
   account_number = models.CharField(max_length=30,null=True)
   loan_type = models.CharField(max_length=60)
   loan_amount = models.CharField(max_length=60)
   interest_rate = models.CharField(max_length=60,null=True)
   periods = models.CharField(max_length=60)
   interest_amount = models.CharField(max_length=60)
   monthli_amount = models.CharField(max_length=60)
   totalAmount = models.CharField(max_length=60,null=True) 
   loanDate = models.CharField(max_length=60,null=True)
   
   def __str__(self):
        return self.account_number

class paymentLoan(models.Model):
    
    manager_id = models.ForeignKey(Branch,on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=30,null=True)
    paymentDate = models.CharField(max_length=60)
    paymentAmount = models.CharField(max_length=60)
    loanBalance = models.CharField(max_length=60)
   
    def __str__(self):
        return self.account_number
   
    
