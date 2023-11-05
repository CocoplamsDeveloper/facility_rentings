from django.db import models
from proplandtent.models import UserRegistry, Property, Units, Role, TenancyLease


class Status(models.Model):

    status_id = models.BigAutoField(primary_key=True, unique=True)
    status_type = models.BigIntegerField(default = 0)
    status = models.CharField(default="None")


class Invoices(models.Model):

    invoice_id = models.BigAutoField(primary_key=True, unique=True)
    tenant_user = models.ForeignKey(UserRegistry,blank=True, null=True, on_delete=models.CASCADE)
    related_unit = models.ForeignKey(Units, blank=True, null=True,on_delete=models.CASCADE)
    status = models.ForeignKey(Status, blank=True, null=True, on_delete=models.CASCADE)
    invoice_amount = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    remarks = models.CharField(max_length=1000, default="None")
    payment_date = models.DateField()
    created_by = models.ForeignKey(UserRegistry,blank=True, null=True, on_delete=models.CASCADE, related_name="+")
    created_on = models.DateTimeField()
    discount = models.DecimalField(max_digits=15, decimal_places=3, default=0)



class Payments(models.Model):
    payment_id = models.BigAutoField(primary_key=True, unique=True)
    transaction_id = models.CharField(default="askj3763", max_length=1000)
    payment_type = models.CharField(max_length=250, default="None")
    invoice_id = models.ForeignKey(Invoices, null=True, blank=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    status = models.ForeignKey(Status, blank=True, null = True, on_delete=models.CASCADE)
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()












