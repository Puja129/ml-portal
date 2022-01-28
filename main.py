import uvicorn
import shutil
from fastapi import FastAPI, Depends, UploadFile, File, Header
from fastapi.responses import JSONResponse
from geoloc import *


tags_metadata = [
    {
        "name": "uploadfile",
        "description": "Please provide OAuth2-token, Service-Id and upload EC Service Log file in _text/plain_ format.",
    },
]

app = FastAPI(
    title="App to derive geo-locations from EC Service Logs",
    description="""<div style="background-color:white;"><p style="color:black;font-size:30px;padding:10px"><img width="54" alt="ec-logo" src="https://user-images.githubusercontent.com/20440873/131534094-13f07dd0-8245-49b3-8199-ba3b0424b4b2.png">Agent geo-locations from EC Service Logs</p></div>
    This app is designed to provide ability to users to upload EC Service Logs to get the geo-locations of EC agents.
    <img width="935" alt="geo_loc_process_flow" src="https://user-images.githubusercontent.com/20440873/131532775-167e8933-15b6-48b0-b122-bd624a7bbaa1.png">

    **Here are the steps to get 'OAuth2-token':**
    1. Go to 'app-url/v1.2beta/crypto/refreshed' and provide Owner-hash to get the 'refreshed-hash'.
    2. Go to 'sdc-url/v1.2beta/user', click on the lock-symbol, provide 'subscription-id' & 'refreshed-hash' to get authenticated, then click 'execute' to get 'OAuth2 token'.
    """,
    version="1.0.0",
    openapi_tags=tags_metadata
)

@app.post("/uploadfile/{svc_id}", tags=["uploadfile"])
async def upload_log(oauth2_token: str, svc_id: str, file: UploadFile = File(...)):
    chk_tkn = validate_token(oauth2_token)
    if chk_tkn != 200:
        return JSONResponse(status_code=400, content={"message": "invalid token provided in the request"})
    else:
    	if file.content_type == "text/plain":
    		filenm = file.filename
    		with open(f'{file.filename}', "wb") as buffer:
    			shutil.copyfileobj(file.file, buffer)
    		result = parse_ip(oauth2_token, svc_id, filenm)
    		return result
    	else:
    		return JSONResponse(status_code=404, content={"message": "Please upload EC Service Log file in text/plain format"})
