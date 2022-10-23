# auth.py
from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException
from starlette.status import HTTP_403_FORBIDDEN

api_key_header = APIKeyHeader(name="access_token", auto_error=False)

#This should be replaced with a database of users + API keys but for now we'll just use this list of keys
valid_API_Keys = ["PETER", "MENDEL"]

# This function can be called and checks API keys
async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header in valid_API_Keys:
        return api_key_header   
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )
