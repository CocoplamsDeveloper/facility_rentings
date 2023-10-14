from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers
from .models import Property, TenancyLease, Units, UserRegistry, Role, RefreshTokenRegistry
from django.middleware import csrf
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from .decorators import is_authorized, is_admin, is_landlord, is_tenant
from .oauth2 import create_tokens
from django.conf import settings
from facilitymanager.settings import ACCESS_TOKEN_LIFETIME, ALGORITHM, REFRESH_TOKEN_LIFETIME
from datetime import datetime, date
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
cookie_max_age = 3600*24*7

# logic functions 
        
    
def generate_tenants(tenants_data, user_id, tenantFile):

    try:
        tenant = tenants_data
        tenant_file = tenantFile
        if UserRegistry.objects.filter(tenant_email=tenant['userEmail']).exists():
            return "tenant account exists"
        else:
            if UserRegistry.objects.filter(user_id=user_id).exists():
                tt = UserRegistry.objects.create(
                    app_user_id = UserRegistry.objects.get(user_id=user_id),
                    landlord_email = tenant['userEmail'],
                    firstname = tenant['userFirstname'],
                    lastname = tenant['userLastname'],
                    contact_number = tenant['contactNumber'],
                    nationality =  tenant['userNationality'],
                    tenant_status = tenant['userStatus'],
                    tenant_rent = tenant['tenantRent'],
                    previous_address = tenant['previousAddress'],
                )
                tt.save()
                return True, tt.tenant_id
            else:
                return "User does not exist"
    except:
        traceback.print_exc()
        return False
    

def generate_landlord(user_data, user_id):

    try:
        landlord = user_data
        if UserRegistry.objects.filter(landlord_email=landlord['userEmail']).exists():
            return "landlord account exists"
        else:
            if UserRegistry.objects.filter(user_id=user_id).exists():
                ld = UserRegistry.objects.create(
                    app_user_id = UserRegistry.objects.get(user_id=user_id),
                    landlord_email = landlord['userEmail'],
                    firstname = landlord['userFirstname'],
                    lastname = landlord['userLastname'],
                    contact_number = landlord['contactNumber'],
                    nationality =  landlord['userNationality'],
                    landlord_status = "active",
                )
                ld.save()
                return True, ld.landlord_id
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



# @api_view(['GET'])
# def get_landlord(request, id):
#     # api to fetch single landlord with id
#     try:
#         user_id = id
#         if UserRegistry.objects.filter(user_id = user_id).exists():
#             ld_data = UserRegistry.objects.filter(user_role = 2)
#             ld_data = json.loads(serializers.serialize('json', ld_data))


#             if len(ld_data) > 1:
#                 response_payload = {"message": "Multiple landlords with same ID"}
#                 return Response(response_payload, 400)

#             response_payload = {
#                 'landlord_record' : ld_data
#             }
#             return Response(response_payload, 200)
#         else:
#             response_payload = {
#                 'message' : 'landlord does not exist'
#             }
#             return Response(response_payload, 404)
#     except:
#         traceback.print_exc()
#         response_payload = {"message" : "server error"}
#         return Response(response_payload, 500)


# @api_view(['GET'])
# def get_tenant(request, id):
#     # api to fetch single tenant with id
#     try:
#         tid = id
#         if UserRegistry.objects.filter(tenants_id = tid).exists():
#             tenant_data = UserRegistry.objects.filter(tenants_id=tid)
#             tenant_data = json.loads(serializers.serialize('json', tenant_data))


#             if len(tenant_data) > 1:
#                 response_payload = {"message": "Multiple tenants with same ID"}
#                 return Response(response_payload, 400)

#             response_payload = {
#                 "tenant_record" : tenant_data
#             }

#             return Response(response_payload, 200)
#         else:
#             response_payload = {
#                 "message" : "tenant not found"
#             }
#             return Response(response_payload, 404)
#     except:
#         traceback.print_exc()
#         response_payload = {
#             "message" : "server error"
#         }
#         return Response(response_payload, 500)


@api_view(['GET'])
def get_property(request, id):
    # api to fetch single property with id
    try:
        user_id = request.query_params['userId']
        pid = id
        if UserRegistry.objects.filter(landlord_id=user_id).exists():
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
            UserRegistry.objects.filter(user_id=user_id).update(user_status = "loggedout")

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
def create_users(request):
    # api to use for admin for generating landlord and tenants
    try:
        users_data = request.data
        users_role = request.data['userRole']
        if UserRegistry.objects.filter(user_email=users_data['userEmail']).exists():
            response_payload = {
                'message' : "user already exists"
            }
            return Response(response_payload, 400)
        else:
            role_id = available_roles[users_role]
            user = UserRegistry.objects.create(
                user_firstname = users_data['userFirstname'],
                user_lastname = users_data['userLastname'],
                user_fullname = users_data['userFirstname'] + " " + users_data['userLastname'],
                user_contact_number = users_data['contactNumber'],
                user_email = users_data['userEmail'],
                user_nationality = users_data['userNationality'],
                user_role = Role.objects.get(role_id=role_id),
            )
            user.save()


    except:
        traceback.print_exc()
        response_payload = {
                'message' : "server error",
            }
        return Response(response_payload, 500)


@api_view(['POST'])
def create_properties(request):
    # api to create property records in db 
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
        if UserRegistry.objects.filter(landlord_id=landlord_id).exists():
            Property.objects.create(
                property_name = property_data['propertyName'],
                property_type = property_data['propertyType'],
                owned_by = UserRegistry.objects.get(landlord_id=landlord_id),
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
            Nos_of_props = UserRegistry.objects.get(landlord_id=landlord_id).properties_owned
            print(Nos_of_props)
            Nos_of_props += 1
            UserRegistry.objects.filter(landlord_id=landlord_id).update(properties_owned=Nos_of_props)
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
@is_authorized
def landlord_property_list(request):
    # api to get property details(id, name) for dropdowns purpose
    try:

        landlord_id = request.query_params['userId']

        properties = Property.objects.filter(owned_by=landlord_id).values_list('property_id', 'property_name', 'property_type')[::1]
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
                    "propertyType" : prop[2]
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
    # api to get the landlord's properties
    try:
        landlord_id = request.query_params['userId']

        if UserRegistry.objects.filter(landlord_id = landlord_id).exists():

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
    # api to add units entered manually by users
    try:
        recieved_data = request.data
        landlord_id = recieved_data['userId']
        property_id = recieved_data['propertyId']
        units_data = recieved_data['unitsData']
        
        if Property.objects.filter(property_id=property_id).exists():
            if len(units_data) > 0:
                for unit in units_data:
                    unit_beds = unit['Unit Bedrooms']
                    unit_baths = unit['Unit Bathrooms']
                    if unit['Unit Bedrooms'] == "other":
                        unit_beds = 0
                    if unit['Unit Bathrooms'] == "other":
                        unit_baths = 0
                    Units.objects.create(
                        unit_property = Property.objects.get(property_id=property_id),
                        unit_name =  unit['Unit Name/Number'],
                        unit_type = unit['Unit Type'],
                        unit_rent = unit['Unit Rent'],
                        unit_bedrooms = int(unit_beds),
                        unit_bathrooms_nos = int(unit_baths),
                        area_insqmts = unit['Unit Size'],
                        unit_status = unit['Status'],
                        unit_occupied_by= UserRegistry.objects.get(tenant_id=2)
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
    # api to save units data into db from csv/excel file
    try:
        data = json.loads(request.data['data'])
        landlord_id = data['userId'],
        property_id = data['propertyId'],
        property_id = int(property_id[0])
        csv_file = request.FILES['unitscsvfile']

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
                    unit_beds = unit['Unit Bedrooms']
                    unit_baths = unit['Unit Bathrooms']
                    if unit['Unit Bedrooms'] == "other":
                        unit_beds = 0
                    elif type(unit['Unit Bedrooms']) == str:
                        unit_beds = int(unit['Unit Bedrooms'])
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
                        unit_occupied_by= UserRegistry.objects.get(tenant_id=2)
                    )

                os.remove(f'media\{csv_file.name}')
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
def update_properties(request):
    # api to update property data
    try:
        updation_data = request.data['data']
        updation_data = json.loads(updation_data)
        landlord_id = updation_data['userId']
        property_id = updation_data['propertyId']
        updated_image = None
        if 'updatedImage' in request.data.keys():
            print(request.data['updatedImage'])
            updated_image = request.data['updatedImage']

        if UserRegistry.objects.filter(landlord_id=landlord_id).exists():

            if Property.objects.filter(property_id=property_id).exists():

                Property.objects.filter(property_id=property_id).update(
                property_name = updation_data['propertyName'],
                property_type = updation_data['propertyType'],
                owned_by = UserRegistry.objects.get(landlord_id=landlord_id),
                governate = updation_data['governateName'],
                Street=updation_data['propertyStreet'],
                City=updation_data['propertyCity'],
                Block=updation_data['propertyBlock'],
                property_civil_id = updation_data['propertyCivil'],
                property_number = updation_data['propertyNumber'],
                area_insqmtrs = updation_data['propertySize'],
                property_status = updation_data['propertyStatus'],
                property_description = updation_data['propertyDescription'],
                built_year = updation_data['propertyBuiltYear'],
                selling_price = updation_data["propertySaleValue"],
                buying_price = updation_data["propertyBuyValue"]
                )

                if updated_image is not None:

                    previous_image = Property.objects.get(property_id=property_id).property_image
                    if os.path.exists(previous_image.path):
                        os.remove(previous_image.path)
                    image = Property.objects.get(property_id=property_id)
                    image.property_image = updated_image
                    image.save()

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
    except:
        traceback.print_exc()
        response_payload = {
            'message' : "server error",
        }
        return Response(response_payload, 500)


@api_view(['GET'])
def get_landlord_all_units(request):

    # api to get landlord all units
    try:
        user_id = request.query_params['userId']
        units_to_send = []

        if UserRegistry.objects.filter(landlord_id = user_id).exists():

            landlord_properties = Property.objects.filter(owned_by = user_id).values_list('property_id', 'property_name')[::1]
            if len(landlord_properties) < 1:
                response_payload = {
                    'message' : "No properties found",
                    "unitsData" :  []
                }
                return Response(response_payload, 400)
            for prop in landlord_properties:
                units = Units.objects.filter(unit_property=prop[0])
                units = json.loads(serializers.serialize('json', units))
                for unit in units:
                    units_to_send.append({
                        "propertyId" : prop[0],
                        "propertyName" : prop[1],
                        "unitId" : unit['pk'],
                        "unitsData" : unit['fields']
                    })

            response_payload = {
                "message" : "fetched successfully",
                "unitsData" : units_to_send
            }

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

@api_view(['POST'])
def get_filtered_units(request):
    # api for filtered units data 
    try:
        user_id = request.data['userId']
        f_type = None
        f_status = None
        f_property = None

        if 'unitTypeFilter' in request.data:
            f_type = request.data['unitTypeFilter']
        if 'unitStatusFilter' in request.data:
            f_status = request.data['unitStatusFilter']
        if 'unitPropertyFilter' in request.data:
            f_property = request.data['unitPropertyFilter']


        if f_type != None and f_status != None and f_property != None:
            filtered_data = Units.objects.filter(unit_type=f_type, unit_status=f_status, unit_property=f_property).values()

        elif f_type != None and f_status != None and f_property == None:
            filtered_data = Units.objects.filter(unit_type=f_type, unit_status=f_status).values()

        elif f_type != None and f_property != None and f_status == None:
            filtered_data = Units.objects.filter(unit_type=f_type, unit_property=f_property).values()

        elif f_status != None and f_property != None and f_type == None:
            filtered_data = Units.objects.filter(unit_status=f_status, unit_property=f_property).values()
  
        elif f_type != None and f_status == None and f_property == None:
            filtered_data = Units.objects.filter(unit_type=f_type).values()
 
        elif f_type == None and f_property != None and f_status == None:
            filtered_data = Units.objects.filter(unit_property=f_property).values()

        elif f_status != None and f_property == None and f_type == None:
            filtered_data = Units.objects.filter(unit_status=f_status).values()


        filtered_arr = []
        for unit in filtered_data:
            filtered_arr.append({
                "propertyId" : unit['unit_property_id'],
                "propertyName" : Property.objects.get(property_id=unit['unit_property_id']).property_name,
                "unitId" : unit['unit_id'],
                "unitsData" : unit
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
def update_property_units(request):
    #api for units updation
    try:
        user_id = request.data['userId']
        updation_data = request.data['updatedData']

        unit_id = updation_data['unitId']
        if Units.objects.filter(unit_id=unit_id).exists():

            update_prompt = Units.objects.filter(unit_id=unit_id).update(
                unit_name=updation_data['unitName/Number'],
                unit_type=updation_data['unitType'],
                unit_bedrooms = updation_data['unitBedrooms'],
                unit_bathrooms_nos = updation_data['unitBathrooms'],
                area_insqmts =  updation_data['unitSize'],
                unit_status = updation_data['unitStatus'],
                unit_rent = updation_data['unitRent'],
            )

            response_payload = {
                "message"  : "Unit updated successfully",
                "response_data" : {"unitId" : unit_id}
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
def delete_units(request):
    # api for unit deletes
    try:
        print(request.data)
        user_id = request.data["userId"]
        unit_id = request.data['unitId']

        if UserRegistry.objects.filter(landlord_id=user_id).exists():

            if Units.objects.filter(unit_id=unit_id).exists():

                Units.objects.get(unit_id=unit_id).delete()
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
        else:
            response_payload = {
                    "message" : "Invalid request",
                    "unitId" :  unit_id
                }
            return Response(response_payload, 401)
    except:
        traceback.print_exc()
        response_payload = {
            "message" : "server error"
        }
        return Response(response_payload, 200)


@api_view(['POST'])
def create_tenants(request):
    # api for tenant creation
    try:
        recieved_data = json.loads(request.data['data'])
        landlord_id = recieved_data['userId']
        tenants_details = recieved_data
        recieved_file = request.data['tenantDocFile']

        if UserRegistry.objects.filter(landlord_id=landlord_id).exists():

            if UserRegistry.objects.filter(user_email=tenants_details['userEmail']).exists():
                response_payload = {
                    'message' : "user already exists",
                }
                return Response(response_payload, 400)
            else:
                user = UserRegistry.objects.create(
                    user_firstname = tenants_details['userFirstname'],
                    user_lastname = tenants_details['userLastname'],
                    user_contact_number = tenants_details['contactNumber'],
                    user_email = tenants_details['userEmail'],
                    user_nationality = tenants_details['userNationality'],
                    user_role = Role.objects.get(role_id=3),
                )
                user.save()

            if user.user_id is not None:

                if UserRegistry.objects.filter(user_id=user.user_id).exists():
                    tt = UserRegistry.objects.create(
                        app_user_id = UserRegistry.objects.get(user_id=user.user_id),
                        reporting_owner = UserRegistry.objects.get(landlord_id=landlord_id),
                        tenants_email = tenants_details['userEmail'],
                        firstname = tenants_details['userFirstname'],
                        lastname = tenants_details['userLastname'],
                        full_name = tenants_details['userFirstname'] + " " + tenants_details['userLastname'],
                        contact_number = tenants_details['contactNumber'],
                        nationality =  tenants_details['userNationality'],
                        tenant_status = tenants_details['userStatus'],
                        previous_address = tenants_details['previousAddress']
                    )
                    tt.save()
                    
                    if recieved_file:
                        created_ten = UserRegistry.objects.get(tenant_id=tt.tenant_id)
                        created_ten.docs = recieved_file
                        created_ten.save()
                    response_payload = {
                        "message" : "Tenant added successfully"
                    }
                    return Response(response_payload, 201)
        else:
            response_payload = {
                "message" : "Invalid request"
            }
            return Response(response_payload, 403)
    except:
        traceback.print_exc()
        response_payload = {
            "message" : "server error"
        }
        return Response(response_payload, 500)


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
def create_tenancy_record(request):
    # api for tenancy record creation
    try:
        recieved_data = json.loads(request.data['data'])
        if request.data['contractDoc']:
            recieved_file = request.data['contractDoc']

        landlord_id = recieved_data['userId']
        property_id = recieved_data['propertyId']
        tenant_id = recieved_data['tenantId']
        unit_id = recieved_data['unitId']

        if UserRegistry.objects.filter(landlord_id = landlord_id).exists():

            if TenancyLease.objects.filter(unit_id=unit_id).exists():
                response_payload = {
                    "message" : "Unit already in existing contract!"
                }
                return Response(response_payload, 400)

            if TenancyLease.objects.filter(tenant_id = tenant_id).exists():
                response_payload = {
                    "message" : "Tenant already in existing contract!"
                }
                return Response(response_payload, 400)
                
            record = TenancyLease.objects.create(
                property_id = Property.objects.get(property_id=property_id),
                unit_id = Units.objects.get(unit_id=unit_id),
                tenant_id = UserRegistry.objects.get(tenant_id=tenant_id),
                monthly_rent = recieved_data['rent'],
                tenancy_start_date = recieved_data['startDate'],
                tenancy_end_date = recieved_data['endDate'],
                tenancy_status = "active",
            )
            if record: 
                Units.objects.filter(unit_id=unit_id).update(unit_occupied_by=tenant_id, unit_status="occupied")
                prop = Property.objects.get(property_id=property_id)
                prop.UserRegistry.add(UserRegistry.objects.get(tenant_id=tenant_id))
                UserRegistry.objects.filter(tenant_id=tenant_id).update(tenant_rent=recieved_data['rent'])
            
            if recieved_file and record:
                tc = TenancyLease.objects.get(tenancy_id=record.tenancy_id)
                tc.tenancy_agreement = recieved_file
                tc.save()

            response_payload = {
                "message" : "record created successfully",
                "tenancyId" : record.tenancy_id
            }

            return Response(response_payload, 201)
        else:
            response_payload = {
                "message" : "Invalid Request"
            }
            return Response(response_payload, 400)

    except:
        traceback.print_exc()
        response_payload = {
            "message" : "server error"
        }
        return Response(response_payload, 500)


@api_view(['GET'])
def get_tenants_data(request):
    # api for all tenants with tenancy
    try:

        user_id = request.query_params['userId']
        tenants_with_tenancy = []
        tenants_data = UserRegistry.objects.filter(reporting_owner=user_id).exclude(firstname="default").values()[::1]
        for t in tenants_data:
            contract_id = None
            tenant_rent = None
            tenant_contract_start = None
            tenant_contract_end = None
            if TenancyLease.objects.filter(tenant_id=t['tenant_id']).exists():
                tenancy = TenancyLease.objects.get(tenant_id=t['tenant_id'])
                contract_id = tenancy.tenancy_id
                tenant_rent = tenancy.monthly_rent
                tenant_contract_start = tenancy.tenancy_start_date
                tenant_contract_end = tenancy.tenancy_end_date
            tenants_with_tenancy.append({
                "tenantId" : t['tenant_id'],
                "tenantName" : t['full_name'],
                "contactNumber" : t['contact_number'],
                "tenantEmail" : t['tenants_email'],
                "tenantRent" : tenant_rent,
                "ContractStartDate" : tenant_contract_start,
                "ContractEndDate" : tenant_contract_end,
                "tenantStatus" : t['tenant_status'],
                "tenancyContractId" : contract_id
            })

        response_payload = {
            "message" : "fetched successfully",
            "tenantsData" : tenants_with_tenancy
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
def update_tenants_related_documents(request):

    try:
        recieved_data = request.data
        landlord_id = recieved_data['userId']
        tenant_id = recieved_data['tenantId']
        tenancy_id = recieved_data['tenancyId']
        updated_tenant_doc = None
        updated_tenancy_doc = None
        if 'updatedTenantDoc' in request.data.keys():
            updated_tenant_doc = request.data['updatedTenantDoc']
        if 'updatedTenancyDoc' in request.data.keys():
            updated_tenancy_doc = request.data['updatedTenancyDoc']
        
        if updated_tenant_doc is not None:
            if UserRegistry.objects.filter(tenant_id=tenant_id).exists():
                t_obj = UserRegistry.objects.get(tenant_id=tenant_id)

                if os.path.exists(str(t_obj.docs)):
                    os.remove(str(t_obj.docs))
                t_obj.docs = updated_tenant_doc
                t_obj.save()

        if updated_tenancy_doc is not None:
            if TenancyLease.objects.filter(tenancy_id=tenancy_id).exists():
                tl_obj = TenancyLease.objects.get(tenancy_id=tenancy_id)
                if os.path.exists(str(tl_obj.tenancy_agreement)):
                    os.remove(str(tl_obj.tenancy_agreement))
                tl_obj.tenancy_agreement = updated_tenancy_doc
                tl_obj.save()
        
        response_payload = {
            "message" : "documents updated successfully",
            "tenantId" : tenant_id,
            "tenancyId" : tenancy_id
        }
        return Response(response_payload, 200)
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

















































































