#-*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
#from django.views import View
import json
from bson import ObjectId
from pymongo import MongoClient
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime

import logging
logger = logging.getLogger('django')
db_conf = settings.DATABASES['default']
client = MongoClient(db_conf['HOST'], int(db_conf['PORT']))
db = eval("client.{0}".format(db_conf['NAME']))
# Create your views here.

def get_org(request,org_id=''):

    data =[]
    result={}

    logger.debug(request)
    showValue=['title','address','floors','longitude','latitude']
    showValueDict={}
    for i in showValue:
        showValueDict[i] = 1
    if org_id == '':
        for out in db.organization.find({},showValueDict):
            o_id=out['_id'].__str__()
            out['_id']=o_id
            data.append(out)
    else:
        #Todo,also need to add drawable below
        for out in db.organization.find({'_id':ObjectId(org_id)},showValueDict):
            o_id=out['_id'].__str__()
            out['_id']=o_id
            data.append(out)

    result['status']='ok'
    result['data']=data

    return HttpResponse(json.dumps(result,encoding='utf8',indent=4), content_type="application/json")

@csrf_exempt
def post_drawing(request,part_id):
    body={}
    try:
        body = json.loads(request.body)

    except Exception,e:
        logger.debug('---{0}---{1}---{2}'.format(Exception,e,request.body))

    drawing=db.drawable
    now=datetime.datetime.now()
    current={}
    try:
        for i in body['drawing']:
            current=i
            current['create_on']=now
            current['update_on']=now
            current['part']=ObjectId(body['part'])
            #write to db
        pre_id = drawing.insert_one(current).inserted_id
    except Exception,e:
        result={}
        result['status']='Failed'
        current['part']=body['part']
        result['data']=current['data']
        logger.debug('----{0}---{1}---{2}'.format(Exception,e,body))
        return HttpResponse(json.dumps(result,encoding='utf8',indent=4,content_type="application/json"))

    body['status']='ok'
    body['part_id']=part_id

    return HttpResponse(json.dumps(body, encoding='utf8', indent=4), content_type="application/json")
