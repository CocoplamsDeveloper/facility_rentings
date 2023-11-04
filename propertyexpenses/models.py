from django.db import models
from proplandtent.models import UserRegistry, Property, Units, Role, TenancyLease



class Status(models.Model):

    status_id = models.BigAutoField(primary_key=True, unique=True)
    user_status = models.CharField(max_length=200, default="None")
    payment_status = models.CharField(max_length=200, default="None")
    property_status = models.CharField(max_length=200, default="None")
    unit_status = models.CharField(max_length=200, default="None")
    

class Invoices(models.Model):

    invoice_id = models.BigAutoField(primary_key=True, unique=True)
    payment_id = models.ForeignKey()
    tenant_user = models.ForeignKey(UserRegistry, on_delete=models.CASCADE)
    related_unit = models.ForeignKey(Units, on_delete=models.CASCADE)
    status = models.ForeignKey(Status,default=None)
    invoice_amount = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    payment_type = models.ForeignKey(Payment,default=null)
    remarks = models.CharField(max_length=1000, default="None")




