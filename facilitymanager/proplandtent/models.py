from django.db import models

# Create your models here.
class Role(models.Model):
    role_id = models.BigAutoField(primary_key=True, unique=True)
    role_name = models.CharField(max_length=100)

#Users table
class UserRegistry(models.Model):
    user_id = models.BigAutoField(primary_key=True, unique=True)
    user_firstname = models.CharField(max_length=150)
    user_lastname = models.CharField(max_length=150)
    user_fullname = models.CharField(max_length=250, default="default")
    user_contact_number = models.BigIntegerField()
    user_email = models.EmailField()
    user_nationality = models.CharField(max_length=100)
    user_role = models.ForeignKey(Role, on_delete=models.CASCADE)
    user_status = models.CharField(max_length=100, default="active")
    user_password = models.CharField(max_length = 150, default="abc123")
    user_document = models.FileField(upload_to="user_documents", default=None)
    user_image = models.ImageField(upload_to="user_images", default=None)
    id_number = models.CharField(max_length=200, default="None")

#property table
class Property(models.Model):
    property_id = models.BigAutoField(primary_key=True, unique=True)
    property_name = models.CharField(max_length=250)
    property_type = models.CharField(max_length=250, default="residential")
    owned_by = models.ForeignKey(UserRegistry, on_delete=models.CASCADE)
    tenants = models.ManyToManyField(UserRegistry,related_name="properties")
    floors = models.IntegerField(default=0)
    governate = models.CharField(default=None, max_length=300)
    City = models.CharField(default=None, max_length=300)
    Street = models.CharField(default=None, max_length=300)
    Block = models.CharField(default=None, max_length=300)
    property_number = models.CharField(default=0)
    parking_areas = models.IntegerField(default=1)
    property_civil_id = models.CharField(default="Not specified", max_length=200, null=True)
    underground_floors = models.IntegerField(default=1)
    units_per_floor = models.IntegerField(default=1)
    units_numbers_start_range = models.IntegerField(default=0)
    bathrooms_per_unit = models.IntegerField(default=1)
    area_insqmtrs = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    units_details = models.JSONField(default=dict)
    address = models.JSONField(default=dict)
    property_image = models.ImageField(upload_to='property_images')
    selling_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    buying_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    property_status = models.CharField(default="inactive")
    property_description = models.TextField(max_length=500, default=None, null=True)
    built_year = models.IntegerField(default=0000)
    deletedby_user = models.BooleanField(default=False)


class Units(models.Model):
    unit_id = models.BigAutoField(primary_key=True,unique=True)
    unit_property = models.ForeignKey(Property, on_delete=models.CASCADE)
    unit_name = models.CharField(max_length=100)
    unit_number = models.CharField(default="AB01")
    unit_type = models.CharField(default="other")
    unit_floor = models.CharField(default="AB02")
    unit_bathrooms_nos = models.IntegerField(default=1)
    unit_bedrooms = models.IntegerField(default=0)
    unit_rent = models.DecimalField(default=0, max_digits=15, decimal_places=2)
    area_insqmts = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    unit_occupied_by = models.IntegerField(default=0)
    unit_status = models.CharField(default="unoccupied", max_length=100)

class TenancyLease(models.Model):
    tenancy_id = models.BigAutoField(primary_key=True, unique=True)
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    unit_id = models.ForeignKey(Units, on_delete=models.CASCADE)
    tenant_id = models.ForeignKey(UserRegistry, on_delete=models.CASCADE, default=2)
    monthly_rent = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    yearly_rent = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    lease_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tenancy_start_date = models.DateField()
    tenancy_end_date = models.DateField()
    tenancy_agreement = models.FileField(upload_to='contract_documents')
    tenancy_status = models.CharField(max_length=150, default="inactive")

class RefreshTokenRegistry(models.Model):

    token = models.CharField()
    user = models.ForeignKey(UserRegistry, on_delete=models.CASCADE)
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()
    expire_time = models.DateTimeField()
    role = models.CharField()
    scope = models.CharField()
    status = models.CharField()

