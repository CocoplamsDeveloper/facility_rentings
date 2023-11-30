from django.db import models


class Payments(models.Model):
    payment_id = models.BigAutoField(primary_key=True, unique=True)
    transaction_id = models.CharField(default="askj3763", max_length=1000)
    payment_type = models.ForeignKey("proplandtent.PayTypes", null=True, blank=True, on_delete=models.CASCADE)
    invoice_id = models.ForeignKey("proplandtent.Invoices", null=True, blank=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    status = models.ForeignKey("proplandtent.Status", blank=True, null = True, on_delete=models.CASCADE)
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()



















