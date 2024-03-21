
from django.contrib import admin
from bankingApp.models import Account, Customer, Loan, Branch, Transcations, User, paymentLoan

admin.site.register(User)
admin.site.register(Account)
admin.site.register(Branch)
admin.site.register(Customer)
admin.site.register(Transcations)
admin.site.register(Loan)
admin.site.register(paymentLoan)