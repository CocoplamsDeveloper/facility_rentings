from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
from .models import Property, TenancyLease, Units, UserRegistry, Role, RefreshTokenRegistry, Status, Invoices, tenancyDocuments, PayTypes, Landlord, UserDocuments, Facilities, PropertyDocuments
# from propertyexpenses.models import Invoices, Status, Payments
from django.middleware import csrf
from django.db.models import Max
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse
from .decorators import is_authorized, is_admin, is_landlord, is_tenant
from .oauth2 import create_tokens, return_accesstoken_from_refresh
from django.conf import settings
from facilitymanager.settings import ACCESS_TOKEN_LIFETIME, ALGORITHM, REFRESH_TOKEN_LIFETIME
from datetime import datetime, date, timedelta
import pandas as pd
import traceback
import requests
import os
import csv
import json


#Global values
available_roles = {
    "admin"  : 1,
    "landlord" : 2,
    "tenant" : 3
}

available_payment_types = {
    "cash" : 1,
    "cheque": 2,
    "online" : 3
}
cookie_max_age = 3600*24*7

# logic functions 


def get_tenant_tenancy_data(tenant_id):

    try:
        temp = []
        if TenancyLease.objects.filter(tenant_id=tenant_id).exists():

            print("tenancy exists")

            tenancy = TenancyLease.objects.filter(tenant_id=tenant_id).values()
            for t in tenancy:
                d = {}
                d['details'] = t
                if Units.objects.filter(unit_id=t['unit_id_id']).exists():
                    unit = Units.objects.get(unit_id=t['unit_id_id'])
                    d['unitName'] = unit.unit_name
                    d['unitFloor'] = unit.unit_floor
                
                temp.append(d)

        return temp
    except:
        traceback.print_exc()



# APIs

@api_view(['GET'])
def get_user(request, id):

    try:
        uid = id
        if UserRegistry.objects.filter(user_id = uid).exists():
            users_data = UserRegistry.objects.filter(user_id=uid)
            users_data = json.loads(serializers.serialize('json', users_data))


            if len(users_data) > 1:
                response_payload = {"message": "Multiple Users with same ID"}
                return Response(response_payload, 400)

            response_payload = {
                "message" : "fetched successfully",
                'user_record' : users_data
            }
            return Response(response_payload, 200)
        else:
            response_payload = {
                'message' : 'user does not exist'
            }
            return Response(response_payload, 404)
    except:
        traceback.print_exc()
        response_payload = {"message" : "server error"}
        return Response(response_payload, 500)



@api_view(['GET'])
# @is_authorized
def get_property(request, id):
    # api to fetch single property with id
    try:
        if id is None or id == '':
            response_payload = {"message": 'Property Id Not recieved'}
            return Response(response_payload, 400)

        user_id = request.query_params['userId']
        pid = id
        data = {}
        if UserRegistry.objects.filter(user_id=user_id).exists():
            if Property.objects.filter(property_id=pid).exists():
                property_data = json.loads(serializers.serialize('json', Property.objects.filter(property_id=pid)))
                data['propertyId'] = property_data[0]['pk']
                data['details'] = property_data[0]['fields']
                data['documents'] = PropertyDocuments.objects.filter(document_property=id).values()
                data['status'] = Status.objects.get(status_id=property_data[0]['fields']['status']).status
                response_payload = {
                    "property_data" : data
                }
                return Response(response_payload, 200)

            else:
                response_payload = {"message": 'Property Not Found'}
                return Response(response_payload, 404)
        else:
            response_payload = {
                'message' : "Invalid request"
            }
            return Response(response_payload, 401)
    except:
        traceback.print_exc()
        response_payload = {
            "message" : "server error"
        }
        return Response(response_payload, 500)
    

@api_view(['GET'])
def get_landlord(request, id):

    try:
        user_id = request.query_params['userId']
        landlord_id = id

        if Landlord.objects.filter(user_id=landlord_id).exists():

            ld = Landlord.objects.filter(user_id=landlord_id)
            ld = json.loads(serializers.serialize('json', ld))
            ld_user_id = ld[0]['fields']['user_id']
            status_obj = UserRegistry.objects.get(user_id=id).status
            print(status_obj)
            d = {}
            d['landlordId'] = ld[0]['pk']
            d['details'] = ld[0]['fields']
            d['documents'] = UserDocuments.objects.filter(document_user=ld_user_id).values()
            d['status'] = Status.objects.get(status_id=status_obj.status_id).status

            response_payload = {
                "message" : "fetched successfully",
                "landlord" : d
            }

            return Response(response_payload, 200)
        else:
            response_payload = {
                "message" : "record not found",
                "landlord" : {}
            }

            return Response(response_payload, 400)
        
    except Exception as err:
        traceback.print_exc()
        response_payload = {
            "message" : type(err).__name__
        }
        return Response(response_payload, 500)
    
@api_view(['GET'])
# @is_authorized
def get_tenant(request, id):

    try:
        tenant_id = id
        tenant_data = {}
        if UserRegistry.objects.filter(user_id=tenant_id).exists():
            user_data = UserRegistry.objects.filter(user_id=tenant_id).values()[::1]

            tenant_data['tenant'] = user_data[0]
            tenant_data['tenancy'] = get_tenant_tenancy_data(tenant_id)

            response_payload = {
                "message": "fetched successfully",
                "tenantRecord" : tenant_data
            }
            return Response(response_payload, 200)
        else:
            response_payload = {
                "message": "Tenant not found",
                "tenantRecord" : tenant_data
            }
            return Response(response_payload, 200)

    except:
        traceback.print_exc()
        response_payload ={
            "message" : "Server error"
        }
        return Response(response_payload, 500)
    
@api_view(['GET'])
def get_tenancy(request, id):
    # api to fetch single tenancy record by id
    try:
        tenancy_id = id
        if TenancyLease.objects.filter(tenancy_id=tenancy_id).exists():
            tenancy_data = TenancyLease.objects.filter(tenancy_id=tenancy_id)
            tenancy_data = json.loads(serializers.serialize('json', tenancy_data))

            if len(tenancy_data) > 1:
                response_payload = {"message": "Multiple tenancy with same ID"}
                return Response(response_payload, 400)

            response_payload = {
                "message" : "fetched successfully",
                "tenancy_data" : tenancy_data
            }
            return Response(response_payload, 200)
        
        else:
            response_payload = {"message": 'Tenancy Not Found'}
            return Response(response_payload, 404)
    except:
        traceback.print_exc()
        response_payload = {
            "message" : "server error"
        }
        return Response(response_payload, 500)
    


@api_view(['GET'])
@is_authorized
def get_unit_floor_wise(request):

    try:
        print(request.query_params)
        property_id = request.query_params['propertyId']
        floor_no = request.query_params['floor']

        if Units.objects.filter(unit_property=property_id).exists():

            
            unit_details = Units.objects.filter(unit_floor=floor_no, unit_property=property_id).values('unit_id', 'unit_name', 'unit_rent')[::1]

            response_payload = {
                "message" : "fetched",
                "units" : unit_details
            }
            return Response(response_payload, 200)
        else:
            response_payload = {
                "message" : "No units for the property",
                "units" : []
            }
            return Response(response_payload, 200)
    except:
        traceback.print_exc()
        response_payload = {
            "message" : "server error"
        }
        return Response(response_payload, 500)


@api_view(['GET'])
def get_units(request, id):
    # api to fetch single unit with id
    try:
        unit_id = id
        if Units.objects.filter(unit_id=unit_id).exists():
            units_data = Units.objects.filter(unit_id=unit_id).values()
            print(units_data)
            # units_data = json.loads(serializers.serialize('json', units_data))

            if len(units_data) > 1:
                response_payload = {"message": "Multiple units with same ID"}
                return Response(response_payload, 400)

            response_payload = {
                "message" : "fetched successfully",
                "unitData" : units_data
            }
            return Response(response_payload, 200)
        
        else:
            response_payload = {"message": 'Unit Not Found'}
            return Response(response_payload, 404)
    except:
        traceback.print_exc()
        response_payload = {
            "message" : "server error"
        }
        return Response(response_payload, 500)

@api_view(['POST'])    
def add_roles(request):
    # api to add roles for users probably used by admin only
    try:
        data = request.data['roleName']
        adding = Role.objects.create(
            role_name = data
        )
        response_payload = {
            "message" : "role added successfully"
        }

        return Response(response_payload, 200)
    except:
        traceback.print_exc()
        response_payload = {
            "message" : "server error"
        }
        return Response(response_payload, 500)
    


@api_view(['GET'])
def user_logout(request):
    # api to logout landlord user
    try:
        user_id = request.query_params['userId']
        token_id = None
        if 'tokenId' in request.query_params.keys():
            token_id = request.query_params['tokenId']
        if UserRegistry.objects.filter(user_id=user_id).exists():
            # UserRegistry.objects.filter(user_id=user_id).update(user_status = "loggedout")

            if token_id is not None:
                if RefreshTokenRegistry.objects.filter(id=token_id).exists():
                    RefreshTokenRegistry.objects.filter(id=token_id).update(
                    status = "invalid",
                    updated_on = datetime.utcnow()
                )
            response_payload = {
                'message' : "Loggedout successfully",
                'user_id' : user_id,
                'status'  : "loggedout"
            }
            return Response(response_payload, 200)
        else:
            response_payload = {
                'message' : "User not found",
            }
            return Response(response_payload, 404)
    except:
        traceback.print_exc()
        response_payload = {
                'message' : "server error",
            }
        return Response(response_payload, 500)


@api_view(['POST'])
@is_authorized
def create_users(request):
    # api to use for admin for generating landlord and tenants
    try:
        print(request.data)
        user_id = request.data['userId']
        users_data = json.loads(request.data['userData'])
        users_role = request.data['userRole']
        user_image = None
        user_doc = None

        if 'userImage' in request.data.keys():
            user_image = request.data['userImage']
        if 'userDocument' in request.data.keys():
            user_doc = request.data['userDocument']
        if UserRegistry.objects.filter(user_email=users_data['userEmail']).exists():
            response_payload = {
                'message' : "user already exists"
            }
            return Response(response_payload, 400)
        else:
            role_id = available_roles[users_role]
            user_default_password = "abc123"
            if 'userPassword' in users_data.keys():
                user_default_password = users_data['userPassword']

            user = UserRegistry.objects.create(
                user_firstname = users_data['userFirstname'],
                user_lastname = users_data['userLastname'],
                user_fullname = users_data['userFirstname'] + " " + users_data['userLastname'],
                user_contact_number = users_data['contactNumber'],
                user_email = users_data['userEmail'],
                user_nationality = users_data['userNationality'],
                user_role = Role.objects.get(role_id=role_id),
                user_password = user_default_password,
                id_number = users_data['userIdNumber']
            )
            
            if user.user_id:
                user_obj = UserRegistry.objects.get(user_id=user.user_id)
                if user_image is not None:
                    user_obj.user_image = user_image
                    user_obj.save()
                if user_doc is not None:
                    user_obj.user_document = user_doc
                    user_obj.save()

                response_payload = {
                    "message" :  f"{users_role} Added successfully"
                }
                return Response(response_payload, 201)
            else:
                response_payload = {
                    "message" :  f"{users_role} not created!"
                }
                return Response(response_payload, 400)

    except:
        traceback.print_exc()
        response_payload = {
                'message' : "server error",
            }
        return Response(response_payload, 500)


@api_view(['POST'])
@is_authorized
def create_properties(request):
    # api to create property records in db 
    try:
        data = request.data
        print(data)
        property_data = data

        user_id = property_data['userId']
        if UserRegistry.objects.filter(user_id=user_id).exists():
            prop = Property.objects.create(
                property_name = property_data['propertyName'],
                property_type = property_data['propertyType'],
                owned_by = UserRegistry.objects.get(user_id=user_id),
                governate = property_data['governateName'],
                Street=property_data['propertyStreet'],
                City=property_data['propertyCity'],
                Block=property_data['propertyBlock'],
                property_number = property_data['propertyNumber'],
                zip_code = property_data['propertyZipCode'],
                area_insqmtrs = property_data['propertySize'],
                built_year = property_data['propertyBuiltYear'],
                floors = property_data['propertyFloor']
            )

            if prop.property_id:
                stat = Status.objects.create(
                    status_type = "Property",
                    status_type_id = prop.property_id,
                    status = property_data['propertyStatus']
                )
                if stat.status_id:
                    Property.objects.filter(property_id=prop.property_id).update(status=Status.objects.get(status_id=stat.status_id))

            response_payload = {
                "message" : "Property Added Successfully!",
                "propertyId" : prop.property_id,
                "propertyName" : prop.property_name
            }
            return Response(response_payload, 201)
        else:
            response_payload = {
                    "message" : "Invalid request" 
                }
            return Response(response_payload, 400)
    except:
        traceback.print_exc()
        response_payload = {
                'message' : "Server error",
            }
        return Response(response_payload, 500)

@api_view(['POST'])
@is_authorized
def add_property_additional_details(request):

    try:
        user_id = request.data['userId']
        additional_data = json.loads(request.data['data'])
        property_image = None
        if 'imageFile' in request.data.keys():
            property_image = request.data['imageFile']
        property_id = int(additional_data['propertyId'])

        facilities = additional_data['facilities']
        if not property_image:
            response_payload = {
                "message" : "Image not found!",
                "propertyId" : property_id
            }
            return Response(response_payload, 400)

        if Property.objects.filter(property_id=property_id).exists():

            record = Property.objects.get(property_id=property_id)
            record.property_civil_id = additional_data['propertyLicenseNo']
            record.property_description = additional_data['propertyDescription']
            record.selling_price = float(additional_data['propertySaleValue'])
            record.buying_price = float(additional_data['propertyBuyValue'])
            record.rentType = additional_data['rentType']
            record.construction_cost = additional_data['constructionCost']
            record.save()

            if property_image:
                PropertyDocuments.objects.create(
                    document_name = "property image",
                    document_property = Property.objects.get(property_id=property_id),
                    image = property_image
                )
            for f in facilities:
                if f['checked']:
                    record.facilities_available.add(Facilities.objects.get(facility_id=f['id']))
            
            
            response_payload = {
                "message" : "details added successfully",
                "propertyId" : property_id
            }

            return Response(response_payload, 200)
        else:
            response_payload = {
                "message" : "Property Not found!",
                "propertyId" : property_id
            }
            return Response(response_payload, 400)
    except:
        traceback.print_exc()
        return Response({"message" : "Server error"}, 500)


@api_view(['GET'])
@is_authorized
def landlord_property_list(request):
    # api to get property details(id, name) for dropdowns purpose
    try:

        landlord_id = request.query_params['userId']

        properties = Property.objects.filter(owned_by=landlord_id).exclude(deletedby_user=True).order_by("property_id").values_list('property_id', 'property_name', 'property_type', 'floors')[::1]
        property_data = []
        if len(properties) == 0:
            response_payload = {
                "message": "No properties found for the user",
                "propertiesData" : []
                }
        else:
            for prop in properties:
                property_data.append({
                    "propertyId"  : prop[0],
                    "propertyName" : prop[1],
                    "propertyType" : prop[2],
                    "floors": prop[3]
                })

            response_payload = {
            "message" : "fetched succesfully",
            "propertiesData" : property_data
            }

        return Response(response_payload, 200)


    except:
        traceback.print_exc()
        response_payload = {
                'message' : "server error",
            }
        return Response(response_payload, 500)


@api_view(['GET'])
@is_authorized
def get_landlord_properties_data(request):
    # api to get the landlord's properties
    try:
        landlord_id = request.query_params['userId']

        properties = []

        if UserRegistry.objects.filter(user_id = landlord_id).exists():

            properties_data = Property.objects.filter(owned_by=landlord_id).exclude(deletedby_user=True).order_by('property_id')
            properties_data = serializers.serialize('json', properties_data)
            properties_data = json.loads(properties_data)

            if len(properties_data) > 0:

                for prop in properties_data:
                    properties.append({
                        "propertyId" : prop['pk'],
                        "details": prop['fields'],
                        "documents" : PropertyDocuments.objects.filter(document_property=prop['pk']).values(),
                        'status': Status.objects.get(status_id=prop['fields']['status']).status
                    })

                response_payload = {
                    "message" : "fetched successfully",
                    "propertiesData" : properties
                }
            else:
                response_payload = {
                    "message" : "Properties not found",
                    "propertiesData" : []
                }

            return Response(response_payload, 200)

        else:
            response_payload = {"message":"Landlord not found"}
            return Response(response_payload, 400)

    except:
        traceback.print_exc()
        response_payload = {
            'message' : "server error",
        }
        return Response(response_payload, 500)
    


@api_view(['DELETE'])
@is_authorized
def soft_delete_property(request):

    try:
        user_property_id = request.query_params['propertyId']

        if Property.objects.filter(property_id=user_property_id).exists():
            Property.objects.filter(property_id = user_property_id).update(deletedby_user=True)
        
            response_payload = {
                "message" : "Property Deleted Successfully",
                "propertyId": user_property_id
            }
            return Response(response_payload, 200)
        else:
            response_payload = {
                "message" : "Property Not found",
                "propertyId": user_property_id
            }
            return Response(response_payload, 400)

    except Exception as err:
        traceback.print_exc()
        response_payload = {
            "message" : type(err).__name__
        }
        return Response(response_payload, 500)


    
@api_view(['POST'])
@is_authorized
def add_units(request):
    # api to add units entered manually by users
    try:
        recieved_data = request.data
        landlord_id = recieved_data['userId']
        property_id = recieved_data['propertyId']
        units_data = recieved_data['unitsData']
        print(units_data)
        
        if Property.objects.filter(property_id=property_id).exists():
            if len(units_data) > 0:
                unit_beds = units_data['Bedrooms']
                unit_baths = units_data['Bathrooms']
                if units_data['Bedrooms'] == "other":
                    unit_beds = 0
                if units_data['Bathrooms'] == "other":
                    unit_baths = 0
                created_unit = Units.objects.create(
                    unit_property = Property.objects.get(property_id=property_id),
                    unit_name =  units_data['Name'],
                    unit_type = units_data['Type'],
                    unit_rent = units_data['Rent'],
                    unit_bedrooms = int(unit_beds),
                    unit_bathrooms_nos = int(unit_baths),
                    area_insqmts = units_data['Size'],
                    unit_floor = units_data['Floor'],
                    unit_category = units_data['Category'],
                    unit_kitchens = units_data['Kitchens']
                )

                stat = Status.objects.create(
                    status_type = "Units",
                    status_type_id = created_unit.unit_id,
                    status = units_data['Status'],
                )

                Units.objects.filter(unit_id=created_unit.unit_id).update(unit_status=Status.objects.get(status_id=stat.status_id))   
                response_payload = {
                    "message" : "Unit added successfully",
                    "unit_id" : created_unit.unit_id 
                }
                return Response(response_payload, 200)
            else:
                response_payload = {
                    'message' : "Invalid request"
                }
                return Response(response_payload, 400)
        else:
            response_payload = {'message': 'property does not exist'}
            return Response(response_payload, 401)
    except:
        traceback.print_exc()
        response_payload = {
                'message' : "server error",
            }
        return Response(response_payload, 500)


@api_view(['POST'])
@is_authorized
def get_units_from_csv(request):
    # api to save units data into db from csv/excel file
    try:
        data = request.data
        skipped = False
        landlord_id = data['userId'],
        property_id = data['propertyId']
        csv_file = data['unitscsvfile']
        property_floor = Property.objects.get(property_id=property_id).floors

        FileSystemStorage(location='media').save(csv_file.name, csv_file)
        file_type = csv_file.name
        file_type = file_type.split('.')[1] 
        
        data_to_send = []
        if file_type != 'xlsx' and file_type != 'xlsm' and file_type != 'csv':
            response_payload = {
                'message' : "File Type not supported!"
            }
            return Response(response_payload, 400)
        
        if file_type == "xlsx" or file_type == "xlsm":

            file_data = pd.read_excel(f'media/{csv_file.name}')
            data_to_send = file_data.to_dict('records')
        elif file_type == 'csv':
            file_data = pd.read_csv(f'media/{csv_file.name}')
            data_to_send = file_data.to_dict('records')

        
        if Property.objects.filter(property_id=property_id).exists():
            if len(data_to_send) > 0:
                for unit in data_to_send:
                    if type(unit['Unit Bedrooms']) != int:
                        skipped=True
                    if type(unit['Unit Bathrooms']) != int:
                        skipped=True
                    if type(unit['Unit Rent']) == str:
                        skipped = True
                    if unit['Unit floors'] > property_floor or type(unit['Unit floors']) != int:
                        skipped = True

                    if skipped:
                        continue
                    Units.objects.create(
                        unit_property = Property.objects.get(property_id=property_id),
                        unit_name =  unit['Unit Name/Number'],
                        unit_type = unit['Unit Type'],
                        unit_rent = unit['Unit Rent'],
                        unit_bedrooms = unit['Unit Bedrooms'],
                        unit_bathrooms_nos = unit['Unit Bathrooms'],
                        area_insqmts = unit['Unit Size'],
                        unit_status = unit['Status'],
                        unit_floor=unit['Unit floors']
                    )

                os.remove(f'media\{csv_file.name}')

                response_message = ''
                if skipped:
                    response_message = "Incorrect data entered for some units!"
                else:
                    response_message = "Units data updated"
                response_payload = {
                    "message" : response_message
                }
                return Response(response_payload, 200)
            else:
                response_payload = {
                    'message' : "Invalid request"
                }
                return Response(response_payload, 400)
        else:
            response_payload = {'message': 'property doesnot exist'}
            return Response(response_payload, 401)
    except:
        traceback.print_exc()
        response_payload = {
                'message' : "server error",
            }
        return Response(response_payload, 500)

@api_view(['POST'])
@is_authorized
def update_properties(request):
    # api to update property data
    try:
        updation_data = request.data['data']
        updation_data = json.loads(updation_data)
        user_id = request.data['userId']
        property_id = updation_data['propertyId']
        updated_image = None
        facilities = json.loads(request.data['facilities'])

        if 'updatedImage' in request.data.keys():
            updated_image = request.data['updatedImage']

        if UserRegistry.objects.filter(user_id=user_id).exists():

            if Property.objects.filter(property_id=property_id).exists():

                Property.objects.filter(property_id=property_id).update(
                property_name = updation_data['propertyName'],
                property_type = updation_data['propertyType'],
                governate = updation_data['propertyCountry'],
                Street=updation_data['propertyStreet'],
                City=updation_data['propertyCity'],
                Block=updation_data['propertyBlock'],
                property_civil_id = updation_data['propertyLicenseNo'],
                property_number = updation_data['propertyNumber'],
                area_insqmtrs = updation_data['propertySize'],
                property_description = updation_data['propertyDescription'],
                built_year = updation_data['propertyBuiltYear'],
                selling_price = updation_data["propertySaleValue"],
                buying_price = updation_data["propertyBuyValue"],
                zip_code = updation_data['propertyZipCode'],
                construction_cost = updation_data['propertyConstructionCost'],
                rentType = updation_data['propertyRentType']
                )


                prop = Property.objects.get(property_id=property_id)
                Status.objects.filter(status_id=prop.status.status_id).update(status=updation_data['propertyStatus'])

                print("line 842", updated_image)
                if updated_image is not None:

                    documents = PropertyDocuments.objects.filter(document_property=prop.property_id).values_list('document_id', 'document_name')

                    image_check = False
                    for doc in documents:
                        if doc[1] == "property image":
                            image_check = True
                            record = PropertyDocuments.objects.get(document_id=doc[0])
                            if record.image != '':
                                if os.path.exists(record.image.path):
                                    os.remove(record.image.path)
                            record.image = updated_image
                            record.save()

                    if not image_check:
                        PropertyDocuments.objects.create(
                        document_property=prop,
                        document_name = 'property image',
                        image = updated_image
                        )
                print(facilities)
                for f in facilities:
                    f_obj = Facilities.objects.get(facility_id=f['id'])
                    if not f['checked']:
                        prop.facilities_available.remove(f_obj)
                    if f['checked']:
                        prop.facilities_available.add(f_obj)
                        
                response_payload = {
                    'message' : "property Updated Successfully",
                    'propertyId' : property_id,
                }
                return Response(response_payload, 200)
            else:
                response_payload = {
                    'message' :  'Property does not exist'
                }
                return Response(response_payload, 401)

        else:
            response_payload = {
                'message' :  'User does not exist'
            }
            return Response(response_payload, 401)
    except Exception as err:
        traceback.print_exc()
        response_payload = {
            'message' : type(err).__name__,
        }
        return Response(response_payload, 500)


@api_view(['GET'])
@is_authorized
def get_landlord_all_units(request):

    # api to get landlord's all units
    try:
        user_id = request.query_params['userId']
        units_to_send = []
        rent_list = []

        if UserRegistry.objects.filter(user_id = user_id).exists():

            landlord_properties = Property.objects.filter(owned_by = user_id, deletedby_user=False).values_list('property_id', 'property_name')[::1]
            if len(landlord_properties) < 1:
                response_payload = {
                    'message' : "No properties found",
                    "unitsData" :  []
                }
                return Response(response_payload, 400)
            for prop in landlord_properties:
                units = Units.objects.filter(unit_property=prop[0], deletedby_user=False)
                units = json.loads(serializers.serialize('json', units))
                for unit in units:
                    units_to_send.append({
                        "propertyId" : prop[0],
                        "propertyName" : prop[1],
                        "unitId" : unit['pk'],
                        "unitsData" : unit['fields'],
                        "status": Status.objects.get(status_id=unit['fields']['unit_status']).status
                    })
                    rent_list.append(float(unit['fields']['unit_rent']))

            response_payload = {
                "message" : "fetched successfully",
                "unitsData" : units_to_send,
            }
            if len(rent_list) > 0:
                response_payload["currentMaxRent"] = max(rent_list)

            return Response(response_payload, 200)
        else:
            response_payload = {
                "message" : "Invalid request",
                "unitsData" : []
            }
            return Response(response_payload, 400)
    except:
        traceback.print_exc()
        response_payload = {
            "message" : "server error"
        }
        return Response(response_payload, 500)

@api_view(['GET'])
@is_authorized
def get_filtered_units(request):
    # api for filtered units data 
    try:
        query_data = request.query_params

        filter_statement = Q()
        if 'type' in query_data.keys():
            filter_statement &= Q(unit_type=query_data['type'])
        if 'status' in query_data.keys():
            filter_statement &= Q(unit_status__in = Status.objects.filter(status=query_data['status']).values_list('status_id', flat=True)[::1])
        if 'property' in query_data.keys():
            filter_statement &= Q(unit_property=query_data['property'])
        if 'rent' in query_data.keys():
            filter_statement &= Q(unit_rent__lte=query_data['rent'])
        
        filter_statement &= Q(deletedby_user = False)

        filtered_data = Units.objects.filter(filter_statement).values()


        filtered_arr = []
        for unit in filtered_data:
            filtered_arr.append({
                "propertyId" : unit['unit_property_id'],
                "propertyName" : Property.objects.get(property_id=unit['unit_property_id']).property_name,
                "unitId" : unit['unit_id'],
                "unitsData" : unit,
                "status": Status.objects.get(status_id=unit['unit_status_id']).status
            })
        
        response_payload = {
            "message" : "fetched successfully",
            "filteredData" :  filtered_arr
        }

        return Response(response_payload, 200)
    except:
        traceback.print_exc()
        response_payload = {
            "message" : "server error"
        }
        return Response(response_payload, 500)

@api_view(['POST'])
@is_authorized
def update_units(request):
    #api for units updation
    try:
        user_id = request.data['userId']
        updation_data = request.data['updatedUnit']

        unit_id = updation_data['unitId']
        if Units.objects.filter(unit_id=unit_id).exists():

            update_prompt = Units.objects.filter(unit_id=unit_id).update(
                unit_name=updation_data['name'],
                unit_type=updation_data['type'],
                unit_bedrooms = updation_data['bedrooms'],
                unit_bathrooms_nos = updation_data['bathrooms'],
                area_insqmts =  updation_data['size'],
                unit_rent = updation_data['rent'],
                unit_category = updation_data['category'],
                unit_kitchens = updation_data['kitchens'],
            )

            stat = Units.objects.get(unit_id=unit_id).unit_status
            Status.objects.filter(status_id=stat.status_id).update(status=updation_data['status'])

            response_payload = {
                "message"  : "Unit updated successfully",
                "unitId" : unit_id
            }

            return Response(response_payload, 200)
        else:
            response_payload = {
                "message"  : "Unit not found",
            }
            return Response(response_payload, 401)
    except:
        traceback.print_exc()
        response_payload = {
            "message" :  'server error'
        }
        return Response(response_payload, 500)



@api_view(['DELETE'])
@is_authorized
def delete_units(request):
    # api for unit deletes
    try:
        user_id = request.query_params["userId"]
        unit_id = request.query_params['unitId']

        if Units.objects.filter(unit_id=unit_id).exists():

            Units.objects.filter(unit_id=unit_id).update(deletedby_user=True)
            response_payload = {
                "message" : "Unit Deleted successfully",
                "unitId" :  unit_id
            }
            return Response(response_payload, 200)
        else:
            response_payload = {
                "message" : "Unit Not found",
                "unitId" :  unit_id
            }
            return Response(response_payload, 400)
    except:
        traceback.print_exc()
        response_payload = {
            "message" : "server error"
        }
        return Response(response_payload, 200)



@api_view(['GET'])
def get_tenant_contract_form_details(request):
    # api for tenants and properties dropdowns(consists of name and ID for both)
    try:
        user_id = request.query_params['userId']
        tenants_data = UserRegistry.objects.filter(reporting_owner=user_id).exclude(firstname="default").values_list("tenant_id", "firstname", "lastname")[::1]
        tenants_array = []
        if len(tenants_data) > 0:
            for t in tenants_data:
                tenants_array.append({
                    "tenantId" : t[0],
                    "tenantName" : t[1] + " " + t[2]
                }) 

        properties_data = Property.objects.filter(owned_by=user_id).values_list("property_id", "property_name")[::1]
        props_arr = []
        if len(properties_data) > 0:
            for p in properties_data:
                props_arr.append({
                    "propertyId" : p[0],
                    "propertyName" : p[1]
                })

        response_payload = {
            "message" : "fetched successfully",
            "tenantsData" : tenants_array,
            "propertiesData" : props_arr
        }

        return Response(response_payload, 200)
    except:
        traceback.print_exc()
        response_payload = {
            "message" : "server error"
        }
        return Response(response_payload, 500)


@api_view(['GET'])
def get_property_units(request):
    
    #api for units id and name(for dropdowns or refernce)
    try:
        user_id = request.query_params['userId']
        property_id = request.query_params['propertyId']

        units_arr = []
        if Property.objects.filter(property_id=property_id).exists():
            related_units = Units.objects.filter(unit_property=property_id).values_list("unit_id", "unit_name")[::1]
            for unit in related_units:
                units_arr.append({
                    "unitId" : unit[0],
                    "unitName" : unit[1]
                })

            response_payload = {
                'message' : "fetched successfully",
                "unitsData" : units_arr
            }
            return Response(response_payload, 200)

        else:
            response_payload = {
                "message" : "Property not found",
                "unitsData" : []
            }
            return Response(response_payload, 400)

    except:
        traceback.print_exc()
        response_payload = {
            "message" : "server error"
        }
        return Response(response_payload, 500)


@api_view(['POST'])
@is_authorized
def create_tenancy_record(request):
    # api for tenancy record creation
    try:
        recieved_data = request.data['tenancyData']
        # print("assign units api",request.data)
        recieved_file = None
        if 'contractDoc' in request.data.keys():
            recieved_file = request.data['contractDoc']

        user_id = request.data['userId']
        property_id = recieved_data['propertyId']
        tenant_id = recieved_data['tenantId']
        unit_id = recieved_data['unitId']

        contract_start = recieved_data['startDate']
        contract_end = recieved_data['endDate']

        if TenancyLease.objects.filter(unit_id=unit_id).exists():
            response_payload = {
                "message" : "Unit already in existing contract!"
            }
            return Response(response_payload, 400)


        contract_time = recieved_data['contractPeriod']

        start_date, end_date = contract_start, contract_end
        dtrange = pd.date_range(start=start_date, end=end_date, freq='d')
        months = pd.Series(dtrange .month)
        starts= months.ne(months.shift(1))

        df = pd.DataFrame([dtrange[starts].strftime('%Y-%m-%d')])
        invoice_dates_list = df.values.tolist()[0]
        print(invoice_dates_list)

        record = TenancyLease.objects.create(
            property_id = Property.objects.get(property_id=property_id),
            unit_id = Units.objects.get(unit_id=unit_id),
            tenant_id = UserRegistry.objects.get(user_id=tenant_id),
            monthly_rent = recieved_data['rent'],
            tenancy_start_date = recieved_data['startDate'],
            tenancy_end_date = recieved_data['endDate'],
            deposit_amount = recieved_data['depositAmount'],
        )
        if record: 
            Units.objects.filter(unit_id=unit_id).update(unit_occupied_by=tenant_id, unit_status="occupied", unit_rent=recieved_data['rent'])
            prop = Property.objects.get(property_id=property_id)
            prop.tenants.add(UserRegistry.objects.get(user_id=tenant_id))

            created_status = Status.objects.create(
                status_type = "tenancy",
                status_type_id = record.tenancy_id,
                status = "active"
            )

            if created_status:

                TenancyLease.objects.filter(tenancy_id=record.tenancy_id).update(status=Status.objects.get(status_id=created_status.status_id))

                if int(recieved_data['depositAmount']) > 0:
                    advance_invoice = Invoices.objects.create(
                        invoice_name = "advance invoice",
                        tenancy_id = TenancyLease.objects.get(tenancy_id=record.tenancy_id),
                        invoice_amount = recieved_data['depositAmount'],
                        payment_type = PayTypes.objects.get(paytype_id=available_payment_types[recieved_data['paymentMode']]),
                        payment_date = invoice_dates_list[0],
                        created_by = UserRegistry.objects.get(user_id=user_id),
                        created_on = datetime.utcnow(),
                        tenant_id = UserRegistry.objects.get(user_id=tenant_id),
                        water_amount = recieved_data['water'],
                        electricity_amount = recieved_data['electricity'],
                        telephone_amount = recieved_data['telephone'],
                        internet_connection = recieved_data['internet']
                    )

                    if advance_invoice:
                        status_record = Status.objects.create(
                        status_type = "invoice",
                        status_type_id = advance_invoice.invoice_id,
                        status = "Due"
                        )
                        if status_record:
                            Invoices.objects.filter(invoice_id=advance_invoice.invoice_id).update(status=Status.objects.get(status_id=status_record.status_id))
                for date in invoice_dates_list:

                    invoice = Invoices.objects.create(
                        invoice_name = "rent invoice",
                        tenancy_id = TenancyLease.objects.get(tenancy_id=record.tenancy_id),
                        invoice_amount = recieved_data['rent'],
                        payment_type = PayTypes.objects.get(paytype_id=available_payment_types[recieved_data['paymentMode']]),
                        payment_date = date,
                        created_by = UserRegistry.objects.get(user_id=user_id),
                        created_on = datetime.utcnow(),
                        discount = recieved_data['discountAmount'],
                        tenant_id = UserRegistry.objects.get(user_id=tenant_id),
                        water_amount = recieved_data['water'],
                        electricity_amount = recieved_data['electricity'],
                        telephone_amount = recieved_data['telephone'],
                        internet_connection = recieved_data['internet']
                    )

                    if invoice:
                        status_record = Status.objects.create(
                        status_type = "invoice",
                        status_type_id = invoice.invoice_id,
                        status = "Due"
                        )
                        if status_record:
                            Invoices.objects.filter(invoice_id=invoice.invoice_id).update(status=Status.objects.get(status_id=status_record.status_id))          


            if recieved_file is not None and record:
                tenancyDocuments.objects.create(
                    document_name = "tenancy contract",
                    document_related_to = TenancyLease.objects.get(tenant_id=record.tenancy_id),
                    document = recieved_file
                )

            response_payload = {
                "message" : "tenancy created successfully",
                "tenancyId" : record.tenancy_id
            }

        return Response(response_payload, 201)
    except Exception as err:
        traceback.print_exc()
        response_payload = {
            "message" : type(err).__name__
        }
        return Response(response_payload, 500)
    

    


@api_view(['GET'])
def get_tenants_data(request):
    # api for all tenants with tenancy
    try:

        user_id = request.query_params['userId']
        tenants_with_tenancy = []
        tenants_data = UserRegistry.objects.filter(user_role=3).order_by("user_id").values()[::1]

        for t in tenants_data:

            tenancy_data = get_tenant_tenancy_data(t['user_id'])
            if len(tenancy_data) == 0:
                tenants_with_tenancy.append({
                    "tenant" : t,
                    "tenancy" : []
                })
            else:
                for i in tenancy_data:
                    tenants_with_tenancy.append({
                        "tenant" : t,
                        "tenancy" : i
                    })
        
        max_tenancy_rent = TenancyLease.objects.aggregate(Max('monthly_rent')).get('monthly_rent__max')
        response_payload = {
            "message" : "fetched successfully",
            "tenantsData" : tenants_with_tenancy,
            "tenancyMaxRent" : max_tenancy_rent
        }
        return Response(response_payload, 200)
    except:
        traceback.print_exc()
        response_payload = {
            "message" : "server error"
        }
        return Response(response_payload, 500)


@api_view(['POST'])
def update_tenants_details(request):
    # api to update tenants data without documents
    try:
        recieved_data = request.data
        user_id = recieved_data['userId']
        tenant_id = recieved_data['tenantId']
        if UserRegistry.objects.filter(tenant_id=tenant_id).exists():

            updation = UserRegistry.objects.filter(tenant_id=tenant_id).update(
                firstname=recieved_data['tenantFirstName'],
                lastname = recieved_data['tenantLastName'],
                tenants_email = recieved_data['tenantEmail'],
                contact_number = recieved_data['tenantContactNumber'],
                tenant_status = recieved_data['tenantStatus'],
                tenant_rent = recieved_data['tenantRent']
            )
            if updation:
                response_payload = {
                    "message" : "Tenants details updated",
                    "tenantId" : tenant_id
                }
                return Response(response_payload, 200)

        else:
            response_payload = {
                "message" : "Tenant not found",
                    "tenantId" : tenant_id
            }
            return Response(response_payload, 400)
        return Response(200)
    except:
        traceback.print_exc()
        response_payload = {
            "message" :  "server error"
        }
        return Response(response_payload, 500)

@api_view(['GET'])
def get_tenants_documents(request):
    #api to fetch tenant document and tenancy contract document
    try:
        landlord_id = request.query_params['userId']
        tenants = UserRegistry.objects.filter(reporting_owner=landlord_id).exclude(firstname="default").values_list('tenant_id','docs')[::1]
        documents_urls = []
        for t in tenants:
            tenancy_id = None
            tenancy_doc = None
            if TenancyLease.objects.filter(tenant_id=t[0]).exists():
                tl = TenancyLease.objects.get(tenant_id=t[0])
                tenancy_id = tl.tenancy_id
                tenancy_doc = str(tl.tenancy_agreement)
            documents_urls.append({
                "tenantId" : t[0],
                "tenantDocument" : str(t[1]),
                "tenancyId" : tenancy_id,
                "tenancyDocument" : tenancy_doc
            })

        response_payload = {
            "message" : "fetched successfully",
            "documentsData" : documents_urls
        }
        return Response(response_payload, 200)
    except:
        traceback.print_exc()
        response_payload = {
            "message" : "server error"
        }
        return Response(response_payload, 500)


@api_view(['POST'])
@is_authorized
def update_tenancy_document(request):

    try:
        recieved_data = request.data
        tenancy_id = recieved_data['tenancyId']
        updated_tenancy_doc = None

        if 'updatedTenancyDoc' in request.data.keys():
            updated_tenancy_doc = request.data['updatedTenancyDoc']
        
        if updated_tenancy_doc is not None:
            if TenancyLease.objects.filter(tenancy_id=tenancy_id).exists():
                tl_obj = TenancyLease.objects.get(tenancy_id=tenancy_id)
                if os.path.exists(str(tl_obj.tenancy_agreement)):
                    os.remove(str(tl_obj.tenancy_agreement))
                tl_obj.tenancy_agreement = updated_tenancy_doc
                tl_obj.save()
        
        response_payload = {
            "message" : "documents updated successfully",
            "tenancyId" : tenancy_id
        }
        return Response(response_payload, 200)
    except:
        traceback.print_exc()
        response_payload = {
            "message" : "server error"
        }
        return Response(response_payload, 500)
    

@api_view(['GET'])
@is_authorized
def serve_contract_document(request):

    try:
        tenancy_id = request.query_params['tenancyId']

        if TenancyLease.objects.filter(tenancy_id=tenancy_id).exists():

            record = TenancyLease.objects.get(tenancy_id=tenancy_id)
            if record.tenancy_agreement == None or record.tenancy_agreement == '':
                response_payload = {
                    "message" : "Contract document Not Found for this tenancy!"
                }
                return Response(response_payload, 400)
            


            response = HttpResponse(record.tenancy_agreement, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=contract_document.pdf'

            return response
        else:
            response_payload = {
                "message" : "contract not found"
            }
            return Response(response_payload, 400)
    except:
        traceback.print_exc()
        response_payload = {
            "message" : "server error"
        }
        return Response(response_payload, 500)


@api_view(['PUT'])
def update_tenancy_status(request):

    try:
        landlord_id = request.query_params['userId']
        tenancy_id = request.query_params['tenancyId']

        if TenancyLease.objects.filter(tenancy_id=tenancy_id).exists():

            tl = TenancyLease.objects.get(tenancy_id=tenancy_id)
            contract_end = tl.tenancy_end_date

            crnt_date = date.today()
            if crnt_date > contract_end:
                tl.tenancy_status = "inactive"
                tl.save()

                response_payload = {
                    "message" : "contract expired",
                    "tenancyId" : tl.tenancy_id
                }
                return Response(response_payload, 200)
            else:
                response_payload = {
                    "message" : "contract valid",
                    "tenancyId" : tl.tenancy_id
                }
                return Response(response_payload, 200)
        else:
            response_payload = {
                "message" : "record not found",
            }
            return Response(response_payload, 400)
    except:
        traceback.print_exc()
        response_payload = {
            "message" : "server error"
        }
        return Response(response_payload, 500)

@api_view(['POST'])
def user_login(request):

    try:
        user_data = request.data
        print(user_data)
        email = user_data['userEmail']
        password = user_data['userPassword']

        if UserRegistry.objects.filter(user_email=email).exists():

            user = UserRegistry.objects.get(user_email=email)
            pass_ = user.user_password

            if password == pass_:
                status, tokens = create_tokens(user.user_id)

                _data = {
                    "accessToken" : tokens['access_token'],
                    "refreshTokenId" : tokens['refresh_token_id'],
                    "userId" : user.user_id,
                    "userRole" : user.user_role.role_name,
                    "userName" : user.user_fullname
                }
                response_payload = {
                    "message" : "Logged In",
                    "userData" : _data
                }


                response = Response(response_payload, 200)

                # response.set_cookie(
                #     key="access_token",
                #     value=tokens['access_token'],
                #     httponly=True,
                #     samesite='Lax',
                #     secure=False
                # )
                # csrf.get_token(request)
                return response
            else:
                response_payload = {
                    "message" : "User Password Incorrect",
                }
                return Response(response_payload, 401)
        else:
            response_payload = {
                "message" : "User Not found",
            }
            return Response(response_payload, 401)

    except:
        traceback.print_exc()
        response_payload = {
            "message" : "Server Error"
        }
        return Response(response_payload, 500)
    


@api_view(['GET'])
def refresh_user_login(request):

    try:
        user_id = request.query_params['userId']
        refresh_token_id = request.query_params['refreshTokenId']

        data, status = return_accesstoken_from_refresh(refresh_token_id, user_id)
        if status:
            return Response({"message" : "login refreshed", "access_tokens" : data}, 200)
        else:
            return Response({"message": "session invalid"}, 401)
    except:
        traceback.print_exc()
        response_payload = {
            "message" : "Server Error"
        }
        return Response(response_payload, 500)


@api_view(['GET'])
def health_check_api(request):

    try:

        return Response(200)
    
    except:
        return Response(200)

@api_view(['GET'])
@is_authorized
def search_properties(request):

    try:
        user_id = request.query_params['userId']
        search_param = request.query_params['searchParam']
        searched_data = Property.objects.filter(owned_by=user_id, property_name__icontains = search_param, deletedby_user=False).order_by('property_id')
        searched_data = json.loads(serializers.serialize('json', searched_data))

        properties = []

        for p in searched_data:
            properties.append({
                "propertyId" : p['pk'],
                "details" : p['fields'],
                "documents": PropertyDocuments.objects.filter(document_property=p['pk']).values(),
                "status" : Status.objects.get(status_id=p['fields']['status']).status
            })
        response_payload = {
            "message" : "fetched",
            "result" : properties
        }
        return Response(response_payload, 200)
    except Exception as err:
        traceback.print_exc()
        response_payload = {
            "message" : type(err).__name__
        }
        return Response(response_payload, 500)

@api_view(['GET'])
@is_authorized
def search_units(request):

    try:
        user_id = request.query_params['userId']
        search_unit_params = request.query_params['searchParam']
        unitsto_send = []
        landlord_properties = Property.objects.filter(owned_by = user_id, deletedby_user=False).values_list('property_id', 'property_name')[::1]
        for prop in landlord_properties:
            units = Units.objects.filter(unit_name__icontains = search_unit_params, unit_property=prop[0], deletedby_user=False)
            units = json.loads(serializers.serialize('json', units))
            for unit in units:
                unitsto_send.append({
                    "propertyId" : prop[0],
                    "propertyName" : prop[1],
                    "unitId" : unit['pk'],
                    "unitsData" : unit['fields'],
                    "status": Status.objects.get(status_id=unit['fields']['unit_status']).status
                })
        response_payload = {
            "message" : "fetched",
            "result" : unitsto_send
        }  
        return Response(response_payload, 200)
    except Exception as err:
        traceback.print_exc()
        response_payload = {
            "message" : type(err).__name__ 
        }
        return Response(response_payload, 500)

@api_view(['GET'])
@is_authorized
def search_tenants(request):

    try:
        query_data = request.query_params['searchParam']
        filter_statement = Q()
        filter_statement |= Q(user_fullname__icontains=query_data)
        filter_statement |= Q(user_contact_number__icontains=query_data)
        searched_results = UserRegistry.objects.filter(filter_statement).exclude(user_role__in=[1,2]).values()

        tenants_with_tenancy = []
        for tenant in searched_results:
            tenancy_data = get_tenant_tenancy_data(tenant['user_id'])
            if len(tenancy_data) == 0:
                tenants_with_tenancy.append({
                    "tenant" : tenant,
                    "tenancy" : []
                })
            else:
                for i in tenancy_data:
                    tenants_with_tenancy.append({
                        "tenant" : tenant,
                        "tenancy" : i
                    })

        response_payload = {
            "message" : "fetched",
            "result" : tenants_with_tenancy
        }
        return Response(response_payload, 200)
    except Exception as err:
        traceback.print_exc()
        response_payload = {
            "message" : type(err).__name__ 
        }
        return Response(response_payload, 500)

@api_view(['GET'])
@is_authorized
def filter_tenants(request):

    try:
        
        query_data = request.query_params
        filter_statement = Q()

        if "property" in query_data.keys() and "floor" not in query_data.keys():
            filter_statement &= Q(user_id__in=TenancyLease.objects.filter(property_id=query_data['property']).values_list('tenant_id', flat=True)[::1])
        if "property" and "unit" and "floor" in query_data.keys():
            filter_statement &= Q(user_id__in=TenancyLease.objects.filter(property_id=query_data['property'], unit_id=query_data['unit']).values_list('tenant_id', flat=True)[::1])
        if "floor" in query_data.keys() and "property" in query_data.keys() and "unit" not in query_data.keys():
            unit_ids = Units.objects.filter(unit_floor=query_data['floor']).values_list('unit_id', flat=True)[::1]
            filter_statement &= Q(user_id__in=TenancyLease.objects.filter(property_id=query_data['property'], unit_id__in=unit_ids).values_list('tenant_id', flat=True)[::1])
        if "nationality" in query_data.keys():
            filter_statement &= Q(user_nationality=query_data['nationality'])
        if "status" in query_data.keys():
            filter_statement &= Q(user_status = query_data['status'])
        if "startDate" in query_data.keys():
            start_dates = query_data['startDate'].split('to')
            filter_statement &= Q(user_id__in=TenancyLease.objects.filter(tenancy_start_date__range=(str(start_dates[0].strip()), str(start_dates[1].strip()))).values_list('tenant_id', flat=True)[::1])
        if "endDate" in query_data.keys():
            end_dates = query_data['endDate'].split('to')
            filter_statement &= Q(user_id__in=TenancyLease.objects.filter(tenancy_end_date__range=(str(end_dates[0].strip()), str(end_dates[1].strip()))).values_list('tenant_id', flat=True)[::1])
        if "rent" in query_data.keys():
            filter_statement &= Q(user_id__in=TenancyLease.objects.filter(monthly_rent__lte=query_data['rent']).values_list('tenant_id', flat=True)[::1])
        
        tenants_results = UserRegistry.objects.filter(filter_statement).exclude(user_role__in = [1, 2]).values()
        tenants_with_tenancy = []
        for tenant in tenants_results:
            tenancy_data = get_tenant_tenancy_data(tenant['user_id'])
            if len(tenancy_data) == 0:
                tenants_with_tenancy.append({
                    "tenant" : tenant,
                    "tenancy" : []
                })
            else:
                for i in tenancy_data:
                    tenants_with_tenancy.append({
                        "tenant" : tenant,
                        "tenancy" : i
                    })

        response_payload = {
            "message" : "fetched",
            "result" : tenants_with_tenancy
        }
        return Response(response_payload, 200)
    except Exception as err:
        traceback.print_exc()
        response_payload = {
            "message" : type(err).__name__
        }
        return Response(response_payload, 500)


@api_view(['POST'])
@is_authorized
def create_landlords(request):

    try:
        request_data = request.data
        user_id = request.data['userId']
        landlord_details = json.loads(request.data['userData'])
        user_image = None
        user_company_logo = None
        user_document = None


        if "userImage" in request_data.keys():
            user_image = request_data['userImage']
        if "userCompanyLogo" in request_data.keys():
            user_company_logo = request_data['userCompanyLogo']
        if "userDocument" in request_data.keys():
            user_document  = request_data['userDocument']


        user = UserRegistry.objects.create(
            user_firstname = landlord_details['firstName'],
            user_lastname = landlord_details['lastName'],
            user_fullname = landlord_details['firstName'] + " " + landlord_details['lastName'],
            user_contact_number = landlord_details['contactNumber'],
            user_email = landlord_details['email'],
            user_nationality = landlord_details['nationality'],
            user_role = Role.objects.get(role_id=available_roles['landlord']),
            user_password = landlord_details['password']
        )

        if user.user_id:
            u1 = UserRegistry.objects.get(user_id=user.user_id)
            ld_obj = Landlord.objects.create(
                landlord_name = landlord_details['firstName'] + " " + landlord_details['lastName'],
                user_id = u1,
                contact_number = landlord_details['contactNumber'],
                email = landlord_details['email'],
                address = landlord_details['landlordAddress'],
                password = landlord_details['password'],
                bank_account_details = {"name" :landlord_details['bankName'], "account_no": landlord_details['bankAccountNo'], "iban_no": landlord_details['bankIbanNo']},
                landlord_type = landlord_details['type'],
                company_name = landlord_details['landlordCompanyName'],
                contact_name = landlord_details['landlordContactPerson'],
                nationality=landlord_details['nationality'],
            )

            if user_image is not None:
                UserDocuments.objects.create(
                    document_name = "user Image",
                    document_user = u1,
                    image = user_image
                )

            if user_company_logo is not None:
                UserDocuments.objects.create(
                    document_name = "landlord company logo",
                    document_user = u1,
                    image = user_company_logo
                )

            if user_document is not None:
                UserDocuments.objects.create(
                    document_name = "landlord document",
                    document_user = u1,
                    document = user_document
                )
            
            
            if ld_obj.landlord_id:
                l1 = Landlord.objects.get(landlord_id=ld_obj.landlord_id)

                if landlord_details['vatId'] != '':
                    l1.VAT_id=landlord_details['vatId']
                    l1.save()
                if landlord_details['comments'] != '':
                    l1.remarks = landlord_details['comments']
                    l1.save()

            
                stat = Status.objects.create(
                    status_type = "UserRegistry",
                    status_type_id = user.user_id,
                    status = landlord_details['status']
                )

                u1.status = Status.objects.get(status_id=stat.status_id)
                u1.save()

        if user and ld_obj:
            response_payload = {
                "message" : "landlord added successfully"
            }
            return Response(response_payload, 201)

    except Exception as err:
        traceback.print_exc()
        response_payload = {
            "message": type(err).__name__
        }
        return Response(response_payload, 500)

@api_view(['GET'])
@is_authorized
def get_landlords_details(request):

    try:
        user_id = request.query_params['userId']
        user_ids = UserRegistry.objects.filter(user_role=2).values_list('user_id', 'status')[::1]
        arr = []
        for user in user_ids:

            data = {}
            ld_qs = Landlord.objects.filter(user_id=user[0])
            if ld_qs:
                ld = json.loads(serializers.serialize('json', ld_qs))
                data['landlordId'] = ld[0]['pk']
                data['landlordDetails'] = ld[0]['fields']
                data['documents']= UserDocuments.objects.filter(document_user=user[0]).values(),
                data['propertyNos'] = Property.objects.filter(owned_by=user[0]).count(),

                if user[1] == None:
                    pass
                else:
                    data["status"] = Status.objects.get(status_id=user[1]).status

                arr.append(data)

        response_payload = {
            "message" : "fetched successfully",
            "landlordData" : arr
        }
        return Response(response_payload, 200)
    except Exception as err:
        traceback.print_exc()
        response_payload = {
            "message": type(err).__name__
        }
        return Response(response_payload, 500)


@api_view(['GET'])
@is_authorized
def get_landlord_page_statistics(request):

    try:
        user_id = request.query_params['userId']
        nos_of_landlords = Landlord.objects.filter(created_by=user_id).count()
        user_statuses = UserRegistry.objects.filter(user_role=2).values_list('status', flat=True)[::1]
        status_count = 0
        units_count = 0
        for stat in user_statuses:
            if stat == None:
                continue
            user_status = Status.objects.get(status_id=stat).status
            if user_status == "Active":
                status_count += 1

        property_count = Property.objects.filter(owned_by=user_id, deletedby_user=False).count()
        all_property_ids = Property.objects.filter(owned_by=user_id, deletedby_user=False).values_list('property_id', flat=True)[::1]
        for p in all_property_ids:
            units_count += Units.objects.filter(unit_property=p, deletedby_user=False).count()

        data = {
            "landlords" : nos_of_landlords,
            "activeLandlords": status_count,
            "properties" :property_count,
            "units": units_count
        }
        
        response_payload = {
            "message" : "fetched successfully",
            "pageData" : data
        }
        return Response(response_payload, 200)
    except Exception as err:
        traceback.print_exc()
        response_payload = {
            "message" : type(err).__name__
        }
        return Response(response_payload, 500)


@api_view(['POST'])
@is_authorized
def update_landlord(request):

    try:
        data = request.data
        landlord_details = json.loads(data['landlordData'])
        ld_id = landlord_details['landlordId']
        ld_user = landlord_details['userId']
        landlord_image = None

        if "landlordImage" in data.keys():
            landlord_image = data['landlordImage']


        if Landlord.objects.filter(landlord_id=ld_id).exists():

            user_updated = UserRegistry.objects.filter(user_id=ld_user).update(
            user_firstname = landlord_details['firstName'],
            user_lastname = landlord_details['lastName'],
            user_fullname = landlord_details['firstName'] + " " + landlord_details['lastName'],
            user_contact_number = landlord_details['contactNumber'],
            user_email = landlord_details['email'],
            user_nationality = landlord_details['nationality'],
            user_password = landlord_details['password']
            )

            if user_updated:
                u1 = UserRegistry.objects.get(user_id=ld_user)
                ld_obj = Landlord.objects.filter(landlord_id=ld_id).update(
                    landlord_name = landlord_details['firstName'] + " " + landlord_details['lastName'],
                    contact_number = landlord_details['contactNumber'],
                    email = landlord_details['email'],
                    address = landlord_details['landlordAddress'],
                    password = landlord_details['password'],
                    bank_account_details = {"name" :landlord_details['bankName'], "account_no": landlord_details['bankAccountNo'], "iban_no": landlord_details['bankIbanNo']},
                    landlord_type = landlord_details['type'],
                    company_name = landlord_details['landlordCompanyName'],
                    contact_name = landlord_details['landlordContactPerson'],
                    nationality=landlord_details['nationality'],

                )


                if landlord_details['vatId'] != '':
                    Landlord.objects.filter(landlord_id=ld_id).update(VAT_id=landlord_details['vatId'])


                added_docs = UserDocuments.objects.filter(document_user=ld_user).values_list("document_id", "document_name")[::1]
                for doc in added_docs:
                    docs = UserDocuments.objects.get(document_id=doc[0])
                    if landlord_image is not None and doc[1] == "user Image":
                        if docs.image != '':
                            if os.path.exists(docs.image.path):
                                os.remove(docs.image.path)
                        docs.image = landlord_image
                        docs.save()

            Status.objects.filter(status_id=u1.status.status_id).update(status=landlord_details['status'])
            response_payload = {
                "message" : "landlord updated successfully",
                "landlordId" : "id"
            }
            return Response(response_payload, 200)
        else:
            response_payload = {
                "message" : "landlord not found!",
                "landlordId" : ld_id
            }
            return Response(response_payload, 400)
    except Exception as err:
        traceback.print_exc()
        response_payload = {
            "message" : type(err).__name__
        }

@api_view(['GET'])
@is_authorized
def get_landlord_documents(request):

    try:
        user_id = request.query_params['userId']
        if UserDocuments.objects.filter(document_user=user_id).exists():
            
            documents_data = UserDocuments.objects.filter(document_user=user_id).values()

            response_payload = {
                "message" : "fetched documents",
                "data" : documents_data
            }
            return Response(response_payload, 200)

    except Exception as err:
        traceback.print_exc()
        response_payload = {
            "message" : type(err).__name__
        }


@api_view(['POST'])
@is_authorized
def add_document(request):

    try:
        user_id = request.data['userId']
        document_name = request.data['documentName']
        document_type = request.data['documentType']
        document = request.data['document']

        if document_type == "Image":
            added = UserDocuments.objects.create(
                document_user = UserRegistry.objects.get(user_id=user_id),
                document_name = document_name,
                image = document
            )
        else:
            added = UserDocuments.objects.create(
                document_user = UserRegistry.objects.get(user_id=user_id),
                document_name = document_name,
                document = document
            )

        if added:
            response_payload = {
                "message" : "Document added successfully",
                "documentId" : added.document_id
            }
            return Response(response_payload, 201)
        else:
            response_payload = {
                "message" : "Document Not added",
            }
            return Response(response_payload, 400)
    except Exception as err:
        traceback.print_exc()
        response_payload = {
            "message" : type(err).__name__
        }
        return Response(response_payload, 500)
    

@api_view(['GET'])
@is_authorized
def download_document(request):

    try:
        document_id = request.query_params['documentId']

        if UserDocuments.objects.filter(document_id=document_id).exists():

            document = UserDocuments.objects.get(document_id=document_id)
            if document.image:
                
                file = str(document.image)
                file_name = file.split('/')[1]
                file_ext = file_name.split('.')
                response = HttpResponse(document.image, content_type=f'image/{file_ext[1]}')
                response['Content-Disposition'] = f'attachment; filename={file_name}'

                return response
            if document.document:

                file = str(document.document)
                file_name = file.split('/')[1]
                file_ext = file_name.split('.')
                response = HttpResponse(document.document, content_type=f'image/{file_ext[1]}')
                response['Content-Disposition'] = f'attachment; filename={file_name}'

                return response
        else:
            response_payload = {
                "message" : "document not found!"
            }
            return Response(response_payload, 400)
    except Exception as err:
        traceback.print_exc()
        response_payload = {
            "message" : type(err).__name__
        }
        return Response(response_payload, 500)
    
@api_view(['POST'])
@is_authorized
def add_facility(request):
    try:
        req_data = request.data
        user_id = req_data['userId']
        facs = req_data['facility']
        fac_id = Facilities.objects.create(
            name = facs['name'],
            included = facs['included'],
            facility_cost = facs['cost'],
            added_by = UserRegistry.objects.get(user_id=user_id)
        )

        if fac_id.facility_id:
            response_payload = {
                "message" : "facility record added"
            }
            return Response(response_payload, 201)
        else:
            response_payload = {
                "message" : "record not added!"
            }
            return Response(response_payload, 400)
    except Exception as err:
        traceback.print_exc()
        response_payload = {
            "message" : type(err).__name__
        }
        return Response(response_payload, 500)
    

@api_view(['GET'])
@is_authorized
def get_facilities(request):

    try:
        user_id = request.query_params['userId']
        facilities = Facilities.objects.filter(added_by=user_id).values()

        response_payload = {
            "message" : "fetched successfully",
            "facilities" : facilities
        }
        return Response(response_payload, 200)
    except Exception as err:
        traceback.print_exc()
        response_payload = {
            "message" : type(err).__name__
        }
        return Response(response_payload, 500)
    

# @api_view(['DELETE'])
# def del_props(request):

#     try:
#         # props = Property.objects.filter(owned_by=request.query_params['userId']).values_list('property_id', flat=True)[::1]
#         # for p in props:
#         #     Property.objects.get(property_id=p).delete()
#         Units.objects.all().delete()

#         return Response(200)

#     except:
#         traceback.print_exc()


@api_view(['GET'])
@is_authorized
def property_documents(request):
    try:

        property_id = request.query_params['propertyId']
        
        documents_list = PropertyDocuments.objects.filter(document_property=property_id).values()
        response_payload = {
            "message": "fetched successfully",
            "documents": documents_list
        }
        return Response(response_payload, 200)
    except Exception as err:
        traceback.print_exc()
        response_payload = {
            "message" : type(err).__name__
        }
        return Response(response_payload, 500)
    
@api_view(['POST'])
@is_authorized
def add_property_document(request):

    try:
        req_data = request.data
        user_id = req_data['userId']
        property_id = req_data['propertyId']
        document = req_data['document']
        document_name = req_data['documentName']
        document_type = req_data['documentType']
        if document_type == "Image":
            added = PropertyDocuments.objects.create(
                document_property = Property.objects.get(property_id=property_id),
                document_name = document_name,
                image = document
            )
        else:
            added = PropertyDocuments.objects.create(
                document_property = Property.objects.get(property_id=property_id),
                document_name = document_name,
                document = document
            )

        if added:
            response_payload = {
                "message" : "Document added successfully",
                "documentId" : added.document_id
            }
            return Response(response_payload, 201)

    except Exception as err:
        traceback.print_exc()
        response_payload = {
            "message" : type(err).__name__
        }
        return Response(response_payload, 500)

@api_view(['GET'])
@is_authorized
def download_property_document(request):

    try:
        document_id = request.query_params['documentId']
        
        if PropertyDocuments.objects.filter(document_id=document_id).exists():

            document = PropertyDocuments.objects.get(document_id=document_id)

            if document.image:
                
                file = str(document.image)
                file_name = file.split('/')[1]
                file_ext = file_name.split('.')
                response = HttpResponse(document.image, content_type=f'image/{file_ext[1]}')
                response['Content-Disposition'] = f'attachment; filename={file_name}'

                return response
            if document.document:

                file = str(document.document)
                file_name = file.split('/')[1]
                file_ext = file_name.split('.')
                response = HttpResponse(document.document, content_type=f'image/{file_ext[1]}')
                response['Content-Disposition'] = f'attachment; filename={file_name}'

                return response
        else:
            response_payload = {
                "message" : "document not found"
            }
            return Response(response_payload, 404)
    except Exception as err:
        traceback.print_exc()
        response_payload = {
            "message" : type(err).__name__
        }
        return Response(response_payload, 500)
    
@api_view(['GET'])
@is_authorized
def get_property_page_statistics(request):

    try:
        user_id = request.query_params['userId']
        properties_count = 0
        units_count = 0
        tenants_count = 0

        properties = Property.objects.filter(owned_by=user_id, deletedby_user=False).values_list('property_id', flat=True)[::1]
        properties_count = len(properties)
        for p in properties:
            units_count += Units.objects.filter(unit_property=p, deletedby_user=False).count()


        response_payload = {
            "message": "fetched successfully",
            "properties": properties_count,
            "units": units_count,
            "tenants": tenants_count
        }
        return Response(response_payload, 200)
        

    except Exception as err:
        traceback.print_exc()
        response_payload = {
            "message" : type(err).__name__
        }
        return Response(response_payload, 500)


@api_view(['GET'])
@is_authorized
def get_units_page_statistics(request):

    try:
        user_id = request.query_params['userId']
        total_units = 0
        units_vacant = 0
        units_occupied = 0
        units_under_maintenance = 0

        properties = Property.objects.filter(owned_by=user_id, deletedby_user=False).values_list('property_id', flat=True)[::1]
        for p in properties:
            total_units += Units.objects.filter(unit_property=p, deletedby_user=False).count()

        units_vacant = Units.objects.filter(unit_status__in=Status.objects.filter(status = "vacant").values_list('status_id', flat=True)[::1], deletedby_user=False).count()
        units_occupied = Units.objects.filter(unit_status__in=Status.objects.filter(status = "occupied").values_list('status_id', flat=True)[::1], deletedby_user=False).count()
        units_under_maintenance = Units.objects.filter(unit_status__in=Status.objects.filter(status = "under maintenance").values_list('status_id', flat=True)[::1], deletedby_user=False).count()

        response_payload = {
            "message": "fetched successfully",
            "totalUnits": total_units,
            "vacantUnits": units_vacant,
            "occupiedUnits": units_occupied,
            "underMaintenanceUnits": units_under_maintenance
        }
        return Response(response_payload, 200)
    except Exception as err:
        traceback.print_exc()
        response_payload = {
            "message" : type(err).__name__
        }
        return Response(response_payload, 500)