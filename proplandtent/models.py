from django.db import models
# Create your models here.
class Status(models.Model):
    # status type is Model name
    # status type id is the model record id(FK)
    status_id = models.BigAutoField(primary_key=True, unique=True)
    status_type = models.CharField(default=None)
    status_type_id = models.BigIntegerField(default=0)
    status = models.CharField(default="None")

class Role(models.Model):
    role_id = models.BigAutoField(primary_key=True, unique=True)
    role_name = models.CharField(max_length=100)

class PayTypes(models.Model):
    paytype_id = models.BigAutoField(primary_key=True, unique=True)
    paytype_name = models.CharField(max_length=1000)


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
    status = models.ForeignKey('Status', null=True, blank=True, on_delete=models.CASCADE)
    user_password = models.CharField(max_length = 150, default="abc123")
    id_number = models.CharField(max_length=200, default="None")


class Landlord(models.Model):

    landlord_id = models.BigAutoField(primary_key=True, unique=True)
    landlord_name = models.CharField(max_length=1000)
    user_id = models.ForeignKey("UserRegistry", null=True, blank=True, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=1000)
    contact_name = models.CharField(max_length=1000)
    contact_number = models.BigIntegerField(default=0)
    email = models.EmailField()
    password = models.CharField(max_length=1000)
    address = models.JSONField(default=dict)
    remarks = models.CharField(max_length=1000)
    landlord_type = models.CharField(max_length=200)
    VAT_id = models.BigIntegerField(default=0)
    bank_account_details = models.JSONField(default=dict)
    nationality = models.CharField(max_length=500, default="None")
    charges = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    created_by = models.BigIntegerField(default=0)  # this is logged in user's user id 

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
    status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.CASCADE)
    deposit_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)



class RefreshTokenRegistry(models.Model):

    token = models.CharField()
    user = models.ForeignKey(UserRegistry, on_delete=models.CASCADE)
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()
    expire_time = models.DateTimeField()
    role = models.CharField()
    scope = models.CharField()
    status = models.CharField()

# class PropertyImages(models.Model):

#     image_id = models.BigAutoField(primary_key=True, unique=True)
#     image_property = models.ForeignKey(Property, null=True, blank=True, on_delete=models.CASCADE)
#     image_name = models.CharField(max_length=1000)
#     image = models.ImageField(upload_to="property_images")

# class PropertyDocuments(models.Model):

#     document_id = models.BigAutoField(primary_key=True, unique=True)
#     document_property = models.ForeignKey(Property, null=True, blank=True, on_delete=models.CASCADE)
#     document_name = models.CharField(max_length=1000)
#     document = models.FileField(upload_to="property_documents")

class tenancyDocuments(models.Model):

    document_id = models.BigAutoField(primary_key=True, unique=True)
    document_related_to = models.ForeignKey(TenancyLease, null=True, blank=True, on_delete=models.CASCADE)
    document_name = models.CharField(max_length=1000)
    document = models.FileField(upload_to="tenancy_documents")

class UserDocuments(models.Model):

    document_id = models.BigAutoField(primary_key=True, unique=True)
    document_user = models.ForeignKey(UserRegistry, null=True, blank=True, on_delete=models.CASCADE)
    document_name = models.CharField(max_length=1000)
    document = models.FileField(upload_to="user_documents")
    image = models.ImageField(upload_to="user_images")

class Invoices(models.Model):

    invoice_id = models.BigAutoField(primary_key=True, unique=True)
    invoice_name = models.CharField(max_length=1000)
    tenancy_id = models.ForeignKey(TenancyLease,blank=True, null=True, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, blank=True, null=True, on_delete=models.CASCADE)
    invoice_amount = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    remarks = models.CharField(max_length=1000, default="None")
    payment_type = models.ForeignKey(PayTypes, blank=True, null=True, on_delete=models.CASCADE)
    payment_date = models.DateField()
    created_by = models.ForeignKey(UserRegistry,blank=True, null=True, on_delete=models.CASCADE, related_name="+")
    created_on = models.DateTimeField()
    discount = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    water_amount = models.BooleanField(default=False)
    telephone_amount = models.BooleanField(default=False)
    electricity_amount = models.BooleanField(default=False)
    internet_connection = models.BooleanField(default=False)
    tenant_id = models.ForeignKey(UserRegistry, blank=True, null=True, on_delete=models.CASCADE)