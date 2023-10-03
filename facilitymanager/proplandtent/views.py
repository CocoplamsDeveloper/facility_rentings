from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers
from .models import Landlord, Tenants, Property, TenancyLease, Units,UserRegistry, Role
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
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

    
    
def generate_tenants(tenants_data, user_id, tenantFile):

    try:
        tenant = tenants_data
        tenant_file = tenantFile
        if Tenants.objects.filter(tenant_email=tenant['userEmail']).exists():
            return "tenant account exists"
        else:
            if UserRegistry.objects.filter(user_id=user_id).exists():
                tt = Tenants.objects.create(
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
        if Landlord.objects.filter(landlord_email=landlord['userEmail']).exists():
            return "landlord account exists"
        else:
            if UserRegistry.objects.filter(user_id=user_id).exists():
                ld = Landlord.objects.create(
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
        user_id = request.query_params['userId']
        pid = id
        if Landlord.objects.filter(landlord_id=user_id).exists():
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
            user = UserRegistry.objects.create(
                user_firstname = users_data['userFirstname'],
                user_lastname = users_data['userLastname'],
                user_contact_number = users_data['contactNumber'],
                user_email = users_data['userEmail'],
                user_nationality = users_data['userNationality'],
                user_role = Role.objects.get(role_id=role_id),
            )
            user.save()
            if users_role == "landlord":
                creation, landlord_id = generate_landlord(users_data, user.user_id)
                print("landlord id", landlord_id)
                response_payload = {
                    'message' : "landlord created successfully",
                    'landlordId' : landlord_id
                }
                return Response(response_payload, 201)
            # if users_role == "tenant":
            #     creation, tenant_id = generate_tenants(users_data, user.user_id)
            #     print("tenant id", tenant_id)
            #     response_payload = {
            #         'message' : "tenant created successfully",
            #         'tenantId' : tenant_id
            #     }
            #     return Response(response_payload, 201)
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
                        unit_occupied_by= Tenants.objects.get(tenant_id=2)
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

    try:
        updation_data = request.data['data']
        print(updation_data, "line 693")
        updation_data = json.loads(updation_data)
        landlord_id = updation_data['userId']
        property_id = updation_data['propertyId']
        updated_image = None
        if 'updatedImage' in request.data.keys():
            print(request.data['updatedImage'])
            updated_image = request.data['updatedImage']

        if Landlord.objects.filter(landlord_id=landlord_id).exists():

            if Property.objects.filter(property_id=property_id).exists():

                Property.objects.filter(property_id=property_id).update(
                property_name = updation_data['propertyName'],
                property_type = updation_data['propertyType'],
                owned_by = Landlord.objects.get(landlord_id=landlord_id),
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


    try:
        user_id = request.query_params['userId']
        units_to_send = []

        if Landlord.objects.filter(landlord_id = user_id).exists():

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
            print("inside 1")
        elif f_type != None and f_status != None and f_property == None:
            filtered_data = Units.objects.filter(unit_type=f_type, unit_status=f_status).values()
            print("inside 2")
        elif f_type != None and f_property != None and f_status == None:
            filtered_data = Units.objects.filter(unit_type=f_type, unit_property=f_property).values()
            print("inside 3")
        elif f_status != None and f_property != None and f_type == None:
            filtered_data = Units.objects.filter(unit_status=f_status, unit_property=f_property).values()
            print("inside 4")
        elif f_type != None and f_status == None and f_property == None:
            filtered_data = Units.objects.filter(unit_type=f_type).values()
            print("inside 5")
        elif f_type == None and f_property != None and f_status == None:
            filtered_data = Units.objects.filter(unit_property=f_property).values()
            print("inside 6")
        elif f_status != None and f_property == None and f_type == None:
            filtered_data = Units.objects.filter(unit_status=f_status).values()
            print("inside 7")

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

    try:
        print(request.data)
        user_id = request.data["userId"]
        unit_id = request.data['unitId']

        if Landlord.objects.filter(landlord_id=user_id).exists():

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

    try:
        recieved_data = json.loads(request.data['data'])
        landlord_id = recieved_data['userId']
        tenants_details = recieved_data
        recieved_file = request.data['tenantDocFile']

        if Landlord.objects.filter(landlord_id=landlord_id).exists():

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
                    tt = Tenants.objects.create(
                        app_user_id = UserRegistry.objects.get(user_id=user.user_id),
                        reporting_owner = Landlord.objects.get(landlord_id=landlord_id),
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
                        created_ten = Tenants.objects.get(tenant_id=tt.tenant_id)
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
def get_all_tenants(request):

    try:
        user_id = request.query_params['userId']

        if Landlord.objects.filter(landlord_id=user_id).exists():

            Tenants.objects.filter(reporting_owner=user_id).values()


    except:
        traceback.print_exc()
        response_payload = {
            "message"  : "server error"
        }
        return Response(response_payload, 500)


@api_view(['GET'])
def get_tenant_contract_form_details(request):

    try:
        user_id = request.query_params['userId']
        tenants_data = Tenants.objects.filter(reporting_owner=user_id).exclude(firstname="default").values_list("tenant_id", "firstname", "lastname")[::1]
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

    try:
        recieved_data = json.loads(request.data['data'])
        print(recieved_data)
        if request.data['contractDoc']:
            recieved_file = request.data['contractDoc']

        landlord_id = recieved_data['userId']
        property_id = recieved_data['propertyId']
        tenant_id = recieved_data['tenantId']
        unit_id = recieved_data['unitId']

        if Landlord.objects.filter(landlord_id = landlord_id).exists():

            record = TenancyLease.objects.create(
                property_id = Property.objects.get(property_id=property_id),
                unit_id = Units.objects.get(unit_id=unit_id),
                tenant_id = Tenants.objects.get(tenant_id=tenant_id),
                monthly_rent = recieved_data['rent'],
                tenancy_start_date = recieved_data['startDate'],
                tenancy_end_date = recieved_data['endDate'],
                tenancy_status = "active",
            )
            print(record.tenancy_id)

            return Response(200)
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





































































































