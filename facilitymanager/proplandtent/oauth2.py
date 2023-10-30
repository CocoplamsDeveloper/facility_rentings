from .models import RefreshTokenRegistry, UserRegistry, Role
from facilitymanager.settings import ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME, SECRET_KEY, ALGORITHM
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta
from .decorators import is_authorized
import os
import base64
import traceback
import jwt



def create_tokens(user_id):

    try:
        user = user_id
        if UserRegistry.objects.filter(user_id=user).exists():
            user_data = UserRegistry.objects.get(user_id=user)
            user_role = user_data.user_role.role_name
            user_firstname = user_data.user_firstname
            user_email = user_data.user_email
            exp_time = datetime.utcnow() + ACCESS_TOKEN_LIFETIME

            payload = {
                "user_name" : user_firstname,
                "user_id" : user,
                "role" : user_role,
                "aud" : user_role,
                "exp" : exp_time
            }
            created_access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
            encoded_string = created_access_token.encode('UTF-8')

            access_token = base64.b64encode(encoded_string)
            access_token = access_token.decode('UTF-8')


            refresh_exp_time = datetime.utcnow() + REFRESH_TOKEN_LIFETIME
            refresh_payload = {
                "user_name" : user_firstname,
                "user_id" : user,
                "role" : user_role,
                "aud" : user_role,
                "exp" : refresh_exp_time
            }

            created_refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm=ALGORITHM)
            rf_encoded_string = created_refresh_token.encode('UTF-8')

            rf_token_bytes = base64.b64encode(rf_encoded_string)
            refresh_token = rf_token_bytes.decode("UTF-8")

            if created_refresh_token:
                crt = RefreshTokenRegistry.objects.create(
                    token = refresh_token,
                    user = UserRegistry.objects.get(user_id=user),
                    created_on = datetime.utcnow(),
                    updated_on = datetime.utcnow(),
                    expire_time = refresh_exp_time,
                    role = user_role,
                    scope = "refresh",
                    status = "valid"
                )
        
            if crt:
                tokens_data = {
                    "access_token" : access_token,
                    "refresh_token" : refresh_token,
                    "refresh_token_id" : crt.id
                }
                return True, tokens_data
        else:
            return False, None
    except:
        traceback.print_exc()


def verify_tokens(token, aud):
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, audience=aud,algorithms=ALGORITHM)
        return decoded_payload, 200
    except jwt.InvalidTokenError:
        return {"message" :  "Invalid token"}, 403
    except jwt.ExpiredSignatureError:
        return {"message" : "token expired"}, 403
    except jwt.InvalidAudienceError:
        return {"message" : "Improper User"}, 401
    except:
        traceback.print_exc()
        return {"message" : "server error"}, 500
    

def create_access_token(user_id):

    try:
        user = user_id
        if UserRegistry.objects.filter(user_id=user).exists():
            user_data = UserRegistry.objects.get(user_id=user)
            user_role = user_data.user_role.role_name
            user_firstname = user_data.user_firstname
            user_email = user_data.user_email
            exp_time = datetime.utcnow() + ACCESS_TOKEN_LIFETIME

            payload = {
                "user_name" : user_firstname,
                "user_id" : user,
                "role" : user_role,
                "aud" : user_role,
                "exp" : exp_time
            }
            created_access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
            encoded_string = created_access_token.encode('UTF-8')

            access_token = base64.b64encode(encoded_string)
            access_token = access_token.decode('UTF-8')

            return access_token
    except:
        traceback.print_exc()


def return_accesstoken_from_refresh(refreshTokenId, user_id):

    try:

        refresh_token = RefreshTokenRegistry.objects.get(token_id=refreshTokenId)
        user_role = refresh_token.role
        message, code = verify_tokens(refresh_token.token, user_role)
        if code ==  401 or code == 403:
            return {}, False

        else:
            access_token = create_access_token(user_id)
            RefreshTokenRegistry.objects.filter(token_id=refreshTokenId).update(status="revoked", updated_on = datetime.utcnow())

            d = {
                "accessToken" : access_token,
                "refreshTokenId" : refreshTokenId
            }

            return d, True

    except:
        traceback.print_exc()
