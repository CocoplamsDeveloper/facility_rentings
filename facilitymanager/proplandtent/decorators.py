from functools import wraps
from .models import RefreshTokenRegistry, UserRegistry, Role
from rest_framework.response import Response
from facilitymanager.settings import SECRET_KEY, ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME, ALGORITHM
import jwt
from datetime import datetime, timedelta
import json
import base64
import os
import traceback
import requests
from rest_framework import exceptions
from django.conf import settings




def is_authorized(func):

    @wraps(func)
    def wrapper_func(request, *args, **kwargs):

        try:
            enc_token = request.META['HTTP_AUTHORIZATION']
            if enc_token == "" or enc_token == None:
                return Response({"message" : "Not Authorized"}, 401)
            enc_token = str.replace(str(enc_token), 'Bearer ', '')
            token_bytes = enc_token.encode('UTF-8')
            token_string = base64.b64decode(token_bytes)
            token = token_string.decode('UTF-8')
            user_id = None
            if request.method == 'GET' or request.method == 'PUT' or request.method == 'DELETE':
                user_id = request.query_params['userId']
            else:
                user_id = request.data['userId']
            if UserRegistry.objects.filter(user_id=user_id).exists():
                aud = UserRegistry.objects.get(user_id = user_id).user_role
                role = aud.role_name
                decoded_payload = jwt.decode(token, SECRET_KEY, audience=role, algorithms=ALGORITHM)
                return func(request, *args, **kwargs)
            else:
                return Response({"message" : "User Not Found"}, 401)
        except jwt.InvalidTokenError:
            return Response({"message" :  "Invalid session"}, 403)
        except jwt.ExpiredSignatureError:
            return Response({"message" : "Session expired"}, 403)
        except jwt.InvalidAudienceError:
            return Response({"message" : "User not authorized"}, 401)
        except:
            traceback.print_exc()
            return Response({"message" : "Server error"}, 500)
        
    return wrapper_func


def is_admin(func):

    @wraps(func)
    def admin_checker(request, *args, **kwargs):

        try:
            user_id = None
            if request.method == 'GET' or request.method == 'PUT' or request.method == 'DELETE':
                user_id = request.query_params['userId']
            else:
                user_id = request.data['userId']

            if user_id is None:
                return Response({"message" : "User not found"}, 401)
            
            user_role = UserRegistry.objects.get(user_id=user_id).user_role
            role = user_role.role_name

            if role == "admin":
                return func(request, *args, **kwargs)
            else:
                return Response({"message" : "User Not authorized"}, 401)
        except:
            traceback.print_exc()
            return Response({"message" : "Server error"}, 500)
    return admin_checker


def is_landlord(func):

    @wraps(func)
    def landlord_checker(request, *args, **kwargs):

        try:
            user_id = None
            if request.method == 'GET' or request.method == 'PUT' or request.method == 'DELETE':
                user_id = request.query_params['userId']
            else:
                user_id = request.data['userId']

            if user_id is None:
                return Response({"message" : "User not found"}, 401)
            
            user_role = UserRegistry.objects.get(user_id=user_id).user_role
            role = user_role.role_name

            if role == "landlord":
                return func(request, *args, **kwargs)
            else:
                return Response({"message" : "User not authorized"}, 401)
        except:
            traceback.print_exc()
            return Response({"message" : "Server error"}, 500)
    return landlord_checker


def is_tenant(func):

    @wraps(func)
    def tenant_checker(request, *args, **kwargs):

        try:
            user_id = None
            if request.method == 'GET' or request.method == 'PUT' or request.method == 'DELETE':
                user_id = request.query_params['userId']
            else:
                user_id = request.data['userId']

            if user_id is None:
                return Response({"message" : "User not found"}, 401)
            
            user_role = UserRegistry.objects.get(user_id=user_id).user_role
            role = user_role.role_name

            if role == "tenant":
                return func(request, *args, **kwargs)
            else:
                return Response({"message" : "User not authorized"}, 401)
        except:
            traceback.print_exc()
            return Response({"message" : "Server error"}, 500)
    return tenant_checker