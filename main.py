from fastapi import FastAPI, Response
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from mangum import Mangum

app = FastAPI()

handler = Mangum(app)

load_dotenv() 
MONGO_DETAILS = os.getenv("DB_URL")
client = MongoClient(MONGO_DETAILS)

database = client.dangoDB
collections_available = database.list_collection_names()


@app.get(
    "/configs",
    response_description="configs for all languages in app",
)
async def retrieve_all_configs():
    collection = database.get_collection("configs")
    cursor = collection.find({}, {'_id': False})
    list_cur = list(cursor)
    return JSONResponse(content=list_cur,status_code=200)

@app.get(
    "/config/{language}",
    response_description="configs for a specific language",
)
async def retrieve_config_for_(language):
    if language in collections_available:
        collection = database.get_collection("configs")
        cursor = collection.find_one({"language":language}, {'_id': False})
        return cursor
    else:
        return Response(status_code=404)
    
@app.get(
    "/versions/{language}",
    response_description="return content of a specific language",
)
async def retrieve_content_versions_for_(language):
    if language in collections_available:
        collection = database.get_collection(language)
        cursor = collection.find({}, {'_id': False, 'content':False})
        list_cur = list(cursor)
        return JSONResponse(content=list_cur,status_code=200)
    else:
        return Response(status_code=404)    

@app.get(
    "/{language}/{type}",
    response_description="return content of a specific language",
)
async def retrieve_only_(language,type):
    if language in collections_available:
        collection = database.get_collection(language)
        if type == "all":
            cursor = collection.find({}, {'_id': False})
            list_cur = list(cursor)
            return JSONResponse(content=list_cur,status_code=200)
        else:
            cursor = collection.find_one({"name":type}, {'_id': False})
            if cursor == None:
                return Response(status_code=404)
            else:
                return cursor
    else:
        return Response(status_code=404)

