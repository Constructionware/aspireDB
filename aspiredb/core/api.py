import asyncio
from aiohttp.web_response import json_response
import orjson as json
from os import name
from aiohttp import web
from socket import gethostname, gethostbyname

from aspiredb.database import Controller

port = 9092

semaphore = asyncio.locks.Semaphore(200)
con = Controller()
routes = web.RouteTableDef()

# Introduction
@routes.get('/', name='home')
async def hello(request):
    '''Introduction  Welcome to aspireDb'''
    return web.Response(text=f"aspireDB   Available on host {gethostname()} On The Local Network at {gethostbyname(gethostname())}:{port} ... Enjoy!")

#.................................. DATABASE ................................

#Create Database
@routes.post('/_db/{dbname}', name='create-db')
async def create_db(request):
    '''Creats a new Public Database with name dbname by default.
    and a Private database if kew access: 'private' key password is present.
    '''
    dbn = request.match_info.get('dbname', None)
    data = await request.json()
    if data.get('access') == 'private':
        result = await con.create_database(
            dbname=dbn, 
            access=data.get('access'), 
            password=data.get('password')
        )
    else: result = await con.create_database(dbname=dbn, access=data.get('access'))
    if type(result) == bytes:
        result = json.loads(result)
    return web.json_response(result)

#Get Database Health Report
@routes.get('/_db/{dbname}', name="get-db")
async def get_db(request):
    '''Retreive The Database status report'''
    dbn = request.match_info.get('dbname', None)
    text= f"Sorry we cannot process requests for {dbn} at this time!...Please try again in a few hours."
    return web.Response(text=text)

#Get Databases 
@routes.get('/_db', name="get-dbs")
async def get_dbs(request):
    '''Retreive All Databases '''
    return web.json_response(json.loads(await con.get_databases()))

#Deletes a Database
@routes.delete('/_db/{dbname}', name="delete-db")
async def delete_db(request):
    '''Deletes a database and its contents'''    
    return web.Response(
        text=f"Sorry we cannot process requests for { request.match_info.get('dbname', None) } at this time!...Please try again in a few hours."
        )

#.................................. DOCUMENTS ................................

#Create Document
@routes.post('/_doc/{dbname}', name='create-doc')
async def create_doc(request):
    '''Creats a new Public Database with name dbname by default.
    and a Private database if kew access: 'private' key password is present.
    '''
    dbn = request.match_info.get('dbname', None)
    data = await request.json()
    result = await con.create_document(database=dbn, data=data)
    if type(result) == bytes:
        result = json.loads(result)
    return web.json_response(result)


#Create a Private Document
@routes.post('/_doc/{dbname}/{password}/', name='create-private-doc')
async def create_private_doc(request):
    '''Creats a new Public Database with name dbname by default.
    and a Private database if kew access: 'private' key password is present.
    '''
    dbn = request.match_info.get('dbname', None)
    password = request.match_info.get('password', None)
    data = await request.json()
    result = await con.create_document(dbname=dbn, data=data, password=password)
    if type(result) == bytes:
        result = json.loads(result)
    return web.json_response(result)


#Update Document
@routes.put('/_doc/{dbname}', name='update-doc')
async def update_doc(request):
    '''Updates a document with data provided.'''
    dbn = request.match_info.get('dbname', None)
    data = await request.json()    
    result = await con.update_document(dbname=dbn, doc_id=data.get('_id'), data=data)
    if type(result) == bytes:
        result = json.loads(result)
    return web.json_response(result)


#Retreive a document
@routes.get('/_doc/{dbname}/{doc_id}', name="get-doc")
async def get_doc(request):
    '''Retreive a document form The Database'''
    dbn = request.match_info.get('dbname', None)
    doc_id = request.match_info.get('doc_id', None)
    result = json.loads( await con.get_document(dbname=dbn, doc_id=doc_id))
    return web.json_response(result)


#Retreive Many Documents
@routes.get('/_doc/{dbname}', name="get-docs")
async def get_docs(request):
    '''Retreive all documents form The Database'''
    dbn = request.match_info.get('dbname', None)    
    result = json.loads(await con.get_documents(dbname=dbn))
    return web.json_response(result)


#Clone a document
@routes.get('/_doc/{dbname}/{doc_id}/{clone_id}/', name="clone-doc")
async def clone_doc(request):
    '''Clone a document form The Database'''
    dbname = request.match_info.get('dbname', None)
    doc_id = request.match_info.get('doc_id', None)
    clone_id = request.match_info.get('clone_id', None)
    result = json.loads( await con.clone_doc(dbname=dbname, doc_id=doc_id, clone_id=clone_id))
    return web.json_response(result)


#Delete a Document
@routes.delete('/_doc/{dbname}/{doc_id}', name="delete-doc")
async def delete_doc(request):
    '''Deletes a document'''
    dbn = request.match_info.get('dbname', None)
    doc_id = request.match_info.get('doc_id', None)
    text= f"Sorry we cannot process requests for {dbn} at this time!...Please try again in a few hours."
    return web.Response(text=text)

