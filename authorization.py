import os
from dotenv import load_dotenv
from typing import Dict
import jwt
from fastapi import FastAPI, Request, HTTPException

load_dotenv()
secret_key=os.getenv("SECRET_KEY")

def get_header(request:Request):
    headers_dict=dict(request.headers)
    if "authorization" not in headers_dict:
        raise HTTPException(status_code=401, detail="No Token Found")
    my_jwt=headers_dict["authorization"]
    if not my_jwt.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    removed_bearer_token=remove_bearer(my_jwt)
    try:
        decode = jwt.decode(removed_bearer_token, secret_key, algorithms=["HS256"])          #type:ignore
        return decode["user_name"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        return ("error",e)

    
    
def remove_bearer(jwt_token):
    try:
        return jwt_token.replace("Bearer ","")
    except Exception as e:
        return ("your error is ",e)
    
    
    
    
    
    
