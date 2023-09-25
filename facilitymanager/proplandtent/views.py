from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers
from .models import Landlord, Tenants, Property, TenancyLease, Units,UserRegistry, Role
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
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


# logic functions 
    


# def save_uploaded_files(request, folder_name, file_name):
#     try:
#         if request.method == 'POST':
#             uploaded_files = request.FILES['file']
#             with open(f'media/documents/{folder_name}/{file_name}', 'wb+') as destination:
#                 for chunk in uploaded_files.chunks():
#                     destination.write(chunk)
            
#     except:
#         traceback.print_exc()

    
    
def create_tenants(tenants_data):

    try:
        data = tenants_data
        tenants_creation = Tenants.objects.create(
            firstname = data['firstName'],
            lastname = data['lastName'],
            contact_number = data['contactNumber'],
            tenant_email = data['tenantEmail'],
            nationality = data['nationality'],
            previous_address = data['previousAddress'],
            tenant_rent = data['tenantRentAmount'],
        )

        if tenants_creation:
            return True

    except:
        return False
    

def create_units(units_data, propertyid, tenant_id):

    try:
        data = units_data
        unit_creation = Units.objects.create(
            unit_property = Property.objects.get(property_id=propertyid),
            unit_name = data['unitName'],
            unit_number = data['unitNumber'],
            unit_floor = data['unitFloor'],
            unit_bathroom_nos = data['unitbathrooms'],
            area_insqmts = data['areasqmtrs'],
            unit_occupied_by = data['unitOccupiedBy'],
            unit_status = data['unoccupied'],
        )
        if unit_creation:
            return True
        else:
            return False
    except:
        traceback.print_exc()
        return False

def generate_landlord(user_data):

    try:
        landlord = user_data
        if Landlord.objects.filter(landlord_email=landlord['user_email']).exists():
            return "landlord account exists"
        else:
            if UserRegistry.objects.filter(user_id=landlord['user_id']).exists():
                Landlord.objects.create(
                    app_user_id = UserRegistry.objects.get(user_id=landlord['user_id']),
                    landlord_email = landlord['user_email'],
                    firstname = landlord['user_firstname'],
                    lastname = landlord['user_lastname'],
                    contact_number = landlord['user_contact_number'],
                    nationality =  landlord['user_nationality'],
                    landlord_status = "active",
                    landlord_password = landlord['user_password']
                )
                return True
            else:
                return "User does not exist"
    except:
        traceback.print_exc()
        return False



# APIs

@api_view(['GET'])
def get_user(request, id):

    try:
        uid = id
        if UserRegistry.objects.filter(user_id = uid).exists():
            users_data = Landlord.objects.filter(user_id=uid)
            users_data = json.loads(serializers.serialize('json', users_data))


            if len(users_data) > 1:
                response_payload = {"message": "Multiple Users with same ID"}
                return Response(response_payload, 400)

            response_payload = {
                'landlord_record' : users_data
            }
            return Response(response_payload, 200)
        else:
            response_payload = {
                'message' : 'landlord does not exist'
            }
            return Response(response_payload, 404)
    except:
        traceback.print_exc()
        response_payload = {"message" : "server error"}
        return Response(response_payload, 500)



@api_view(['GET'])
def get_landlord(request, id):

    try:
        lid = id
        if Landlord.objects.filter(landlord_id = lid).exists():
            ld_data = Landlord.objects.filter(landlord_id=lid)
            ld_data = json.loads(serializers.serialize('json', ld_data))


            if len(ld_data) > 1:
                response_payload = {"message": "Multiple landlords with same ID"}
                return Response(response_payload, 400)

            response_payload = {
                'landlord_record' : ld_data
            }
            return Response(response_payload, 200)
        else:
            response_payload = {
                'message' : 'landlord does not exist'
            }
            return Response(response_payload, 404)
    except:
        traceback.print_exc()
        response_payload = {"message" : "server error"}
        return Response(response_payload, 500)


@api_view(['GET'])
def get_tenant(request, id):

    try:
        tid = id
        if Tenants.objects.filter(tenants_id = tid).exists():
            tenant_data = Tenants.objects.filter(tenants_id=tid)
            tenant_data = json.loads(serializers.serialize('json', tenant_data))


            if len(tenant_data) > 1:
                response_payload = {"message": "Multiple tenants with same ID"}
                return Response(response_payload, 400)

            response_payload = {
                "tenant_record" : tenant_data
            }

            return Response(response_payload, 200)
        else:
            response_payload = {
                "message" : "tenant not found"
            }
            return Response(response_payload, 404)
    except:
        traceback.print_exc()
        response_payload = {
            "message" : "server error"
        }
        return Response(response_payload, 500)


@api_view(['GET'])
def get_property(request, id):

    try:
        pid = id
        if Property.objects.filter(property_id=pid).exists():
            property_data = Property.objects.filter(property_id=pid)
            property_data = json.loads(serializers.serialize('json', property_data))

            if len(property_data) > 1:
                response_payload = {"message": "Multiple properties with same ID"}
                return Response(response_payload, 400)

            response_payload = {
                "property_data" : property_data
            }
            return Response(response_payload, 200)
        
        else:
            response_payload = {"message": 'Property Not Found'}
            return Response(response_payload, 404)
    except:
        traceback.print_exc()
        response_payload = {
            "message" : "server error"
        }
        return Response(response_payload, 500)
    
@api_view(['GET'])
def get_tenancy(request, id):

    try:
        tenancy_id = id
        if TenancyLease.objects.filter(tenancy_id=tenancy_id).exists():
            tenancy_data = TenancyLease.objects.filter(tenancy_id=tenancy_id)
            tenancy_data = json.loads(serializers.serialize('json', tenancy_data))

            if len(tenancy_data) > 1:
                response_payload = {"message": "Multiple tenancy with same ID"}
                return Response(response_payload, 400)

            response_payload = {
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
def get_units(request, id):

    try:
        unit_id = id
        if Units.objects.filter(unit_id=unit_id).exists():
            units_data = TenancyLease.objects.filter(unit_id=unit_id)
            units_data = json.loads(serializers.serialize('json', units_data))

            if len(units_data) > 1:
                response_payload = {"message": "Multiple units with same ID"}
                return Response(response_payload, 400)

            response_payload = {
                "tenancy_data" : units_data
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
    

@api_view(['POST'])
def landlord_login(request):

    try:
        user_data = request.data
        email = user_data['userEmail']
        password = user_data['userPassword']

        if UserRegistry.objects.filter(user_email=email).exists():

            if Landlord.objects.filter(landlord_email=email).exists():
                ld_data = Landlord.objects.get(landlord_email=email)

                if password == ld_data.landlord_password:
                    Landlord.objects.filter(landlord_email=email).update(landlord_status="loggedin")

                    response_payload = {
                        'message' : "Logged In Successfully",
                        'user_id' : ld_data.landlord_id,
                        'user_first_name' : ld_data.firstname, 
                        'user_last_name' : ld_data.lastname,
                        'user_status' : ld_data.landlord_status
                    }        

                    return Response(response_payload, 200)

            else:
                response_payload = {
                    'message' : 'User does not exists'
                }
                return Response(response_payload, 401)
            
        else:
            response_payload = {
                'message' : 'Invalid User'
            }
            return Response(response_payload, 401)

    except:
        traceback.print_exc()
        response_payload = {
        "message" : "server error"
        }
        return Response(response_payload, 500)


@api_view(['GET'])
def landlord_logout(request):

    try:
        landlord_id = request.query_params['userId']
        if Landlord.objects.filter(landlord_id=landlord_id).exists():
            Landlord.objects.filter(landlord_id=landlord_id).update(landlord_status = "loggedout")

            response_payload = {
                'message' : "Loggedout successfully",
                'landlord_id' : landlord_id,
                'status'  : Landlord.objects.get(landlord_id=landlord_id).landlord_status
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
def create_users(request):

    try:
        users_data = request.data
        users_role = request.data['userRole']
        if UserRegistry.objects.filter(user_email=users_data['userEmail']).exists():
            response_payload = {
                'message' : "user already exists",
            }
            return Response(response_payload, 400)
        else:
            role_id = available_roles[users_role]
            UserRegistry.objects.create(
                user_firstname = users_data['userFirstname'],
                user_lastname = users_data['userLastname'],
                user_contact_number = users_data['contactNumber'],
                user_email = users_data['userEmail'],
                user_nationality = users_data['userNationality'],
                user_role = Role.objects.get(role_id=role_id),
                user_password = users_data['userPassword']
            )

            if users_role == "landlord":
                creation = generate_landlord(users_data)

            if creation:

                response_payload = {
                    'message' : "user created successfully",
                }
                return Response(response_payload)
            else:
                response_payload = {
                    'message' : creation
                }
                return Response(response_payload)

    except:
        traceback.print_exc()
        response_payload = {
                'message' : "server error",
            }
        return Response(response_payload, 500)


@api_view(['POST'])
def create_properties(request):

    try:
        data = request.data
        property_data = data['data']
        property_photo = data['image']
        property_data = json.loads(property_data)
        print(property_data, property_photo)
        if "propertySaleValue" in property_data.keys():
            property_salevalue = float(property_data["propertySaleValue"])
        if "propertyBuyValue" in property_data.keys():
            property_buyvalue = float(property_data["propertyBuyValue"])

        landlord_id = property_data['userId']
        if Landlord.objects.filter(landlord_id=landlord_id).exists():
            Property.objects.create(
                property_name = property_data['propertyName'],
                property_type = property_data['propertyType'],
                owned_by = Landlord.objects.get(landlord_id=landlord_id),
                governate = property_data['governateName'],
                Street=property_data['propertyStreet'],
                City=property_data['propertyCity'],
                Block=property_data['propertyBlock'],
                property_civil_id = property_data['propertyCivil'],
                property_number = property_data['propertyNumber'],
                area_insqmtrs = property_data['propertySize'],
                property_image = property_photo,
                property_status = property_data['propertyStatus'],
                property_description = property_data['propertyDescription'],
                built_year = property_data['propertyBuiltYear'],
                selling_price = property_salevalue,
                buying_price = property_buyvalue
            )
            Nos_of_props = Landlord.objects.get(landlord_id=landlord_id).properties_owned
            print(Nos_of_props)
            Nos_of_props += 1
            Landlord.objects.filter(landlord_id=landlord_id).update(properties_owned=Nos_of_props)
            response_payload = {
                "message" : "success" 
            }
            return Response(response_payload, 200)
        else:
            response_payload = {
                    "message" : "Invalid request" 
                }
            return Response(response_payload, 400)
    except:
        traceback.print_exc()
        response_payload = {
                'message' : "server error",
            }
        return Response(response_payload, 500)


@api_view(['GET'])
def landlord_property_list(request):

    try:
        landlord_id = request.query_params['userId']

        properties = Property.objects.filter(owned_by=landlord_id).values_list('property_id', 'property_name')[::1]
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
                    "propertyName" : prop[1]
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
def get_landlord_properties_data(request):

    try:
        landlord_id = request.query_params['userId']

        if Landlord.objects.filter(landlord_id = landlord_id).exists():

            properties_data = Property.objects.filter(owned_by=landlord_id)
            properties_data = serializers.serialize('json', properties_data)
            properties_data = json.loads(properties_data)

            if len(properties_data) > 0:

                response_payload = {
                    "message" : "fetched successfully",
                    "propertiesData" : properties_data
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
    
@api_view(['POST'])
def add_units(request):

    try:
        recieved_data = request.data
        landlord_id = recieved_data['userId']
        property_id = recieved_data['propertyId']
        units_data = recieved_data['unitsData']
        
        if Property.objects.filter(property_id=property_id).exists():
            if len(units_data) > 0:
                for unit in units_data:
                    Units.objects.create(
                        unit_property = Property.objects.get(property_id=property_id),
                        unit_name =  unit['Unit Name/Number'],
                        unit_type = unit['Unit Type'],
                        unit_rent = unit['Unit Rent'],
                        unit_bedrooms = int(unit['Unit Bedrooms']),
                        unit_bathrooms_nos = int(unit['Unit Bathrooms']),
                        area_insqmts = unit['Unit Size'],
                        unit_status = unit['Status'],
                        unit_occupied_by= Tenants.objects.get(tenant_id=2)
                    )

                response_payload = {
                    "message" : "Units Data updated!"
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
def get_units_from_csv(request):

    try:
        data = json.loads(request.data['data'])
        landlord_id = data['userId'],
        property_id = data['propertyId'],
        csv_file = request.FILES['unitscsvfile']

        print(property_id, "line 610")

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

        
        if Property.objects.filter(property_id=property_id[0]).exists():
            if len(data_to_send) > 0:
                for unit in data_to_send:
                    unit_beds = unit['Unit Bedrooms']
                    unit_baths = unit['Unit Bathrooms']
                    if type(unit['Unit Bedrooms']) == str:
                        unit_beds = 0
                    if type(unit['Unit Bathrooms']) == str:
                        unit_baths = 0
                    Units.objects.create(
                        unit_property = Property.objects.get(property_id=property_id),
                        unit_name =  unit['Unit Name/Number'],
                        unit_type = unit['Unit Type'],
                        unit_rent = unit['Unit Rent'],
                        unit_bedrooms = unit_beds,
                        unit_bathrooms_nos = unit_baths,
                        area_insqmts = unit['Unit Size'],
                        unit_status = unit['Status'],
                        unit_occupied_by= Tenants.objects.get(tenant_id=2)
                    )
                response_payload = {
                    "message" : "Units Data updated!"
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
























































































































