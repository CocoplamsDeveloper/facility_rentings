from functools import wraps
import requests


def is_authorized(func):

    def wrapper_func(func):
        @wraps(func)
        def actual_func(*args, **kwargs):

            try:
                decoded_payload = jwt.decode(token, SECRET_KEY, audience=aud,algorithms=ALGORITHM)
                return decoded_payload, 200
                return func(*args, **kwargs)
            except jwt.InvalidTokenError:
                return {"message" :  "Invalid token"}, 403
            except jwt.ExpiredSignatureError:
                return {"message" : "token expired"}, 403
            except jwt.InvalidAudienceError:
                return {"message" : "Improper User"}, 403
            except:
                traceback.print_exc()
                return {"message" : "server error"}, 500
        
        return actual_func

    return wrapper_func
