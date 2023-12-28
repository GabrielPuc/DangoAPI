from fastapi import FastAPI, Response, Path
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
    "/all",
    response_description="default response when no language was provided",
)
async def retrieve_all():
    return Response(content="no language provided",status_code=400)

@app.get(
    "/all/{language}",
    response_description="all content for a given language",
)
async def retrieve_all(language):
    if language in collections_available:
        collection = database.get_collection(language)
        cursor = collection.find({}, {'_id': False})
        list_cur = list(cursor)
        return JSONResponse(content=list_cur,status_code=200)
    else:
        return Response(status_code=404)

@app.get(
    "/{language}/{type}",
    response_description="specific content given a language and a valid name",
)
async def retrieve_only(language,type):
    if language in collections_available:
        collection = database.get_collection(language)
        cursor = collection.find_one({"name":type}, {'_id': False})
        if cursor == None:
            return Response(status_code=404)
        else:
            return cursor
    else:
        return Response(status_code=404)
    
@app.get(
    "/configs",
    response_description="configs for all languages in app",
)
async def retrieve_all():
    collection = database.get_collection("configs")
    cursor = collection.find({}, {'_id': False})
    list_cur = list(cursor)
    return JSONResponse(content=list_cur,status_code=200)
