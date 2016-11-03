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

    if org_id == '':
        #get org list
        showValue = ['title', 'address', 'floors', 'longitude', 'latitude']
        showValueDict = {}
        for i in showValue:
            showValueDict[i] = 1
        for out in db.organization.find({},showValueDict):
            o_id=out['_id'].__str__()
            out['_id']=o_id
            data.append(out)
    else:
        #check if objectid valid
        if not ObjectId.is_valid (org_id) :
            return HttpResponse(json.dumps({'status':'Failed','Info':'Wrong para.Plz check whether it\'s valid Id'},indent=4),content_type="application/json")
        else:
            showValuePart = ['title', 'floor', 'floors']
            showValuePartDict = {}
            for i in showValuePart:
                showValuePartDict[i] = 1
            logger.debug(org_id)
            for outComePart in db.part.find({'owner':ObjectId(org_id)},showValuePartDict):
                #logger.debug(outComePart)
                outComePart['drawables']=[]
                showValueDrawable=['title','type','longitude','latitude','data']
                showValueDrawableDict={}
                for i in showValueDrawable:
                    showValueDrawableDict[i]=1
                for outComeDrawble in db.drawable.find({'part':ObjectId(outComePart['_id'])},showValueDrawableDict):
                    o_id=outComeDrawble['_id'].__str__()
                    outComeDrawble['_id']=o_id
                    outComePart['drawables'].append(outComeDrawble)

                o_id=outComePart['_id'].__str__()
                outComePart['_id']=o_id
                data.append(outComePart)
                #logger.debug(data)

    result['status']='ok'
    result['data']=data

    return HttpResponse(json.dumps(result,encoding='utf8',indent=4), content_type="application/json")

@csrf_exempt
def post_drawing(request,part_id):
    #part_id invalid, part_id not exist
    if not ObjectId.is_valid(part_id):
        return HttpResponse(json.dumps({'status':'Failed','Info':'Wrong para.Plz check whether it\'s valid Id'},indent=4),content_type="application/json")
    if db.part.find({'_id':part_id}).count() ==0:
        return HttpResponse(json.dumps({'status':'Failed','Info':'Part Id {0} not exists. plz check again'.format(part_id)},indent=4),content_type="application/json")
    body={}
    re={}
    re['obj_id']=[]
    try:#
        body = json.loads(request.body)

    except Exception,e:
        logger.debug('[1]---{0}---{1}---{2}'.format(Exception,e,request.body))

    drawing=db.drawable
    now=datetime.datetime.now()
    current={}
    pre_id=''

    for i in body['drawing']:
        try:
            current=i

            current['create_on']=now
            current['update_on']=now
            current['part']=ObjectId(body['part'])
            pre_id = drawing.insert_one(current).inserted_id

            if isinstance(pre_id, ObjectId):
                re['obj_id'].append({'pre_id': pre_id.__str__(), "title": current['title']})
            else:
                #
                logger.debug('[ERROR]-----cannot insert :{0}---{1}'.format(current['title'],current))
                re['ERROR'].append(current['title'])
        except Exception,e:
            re['obj_id'].append({'pre_id': pre_id.__str__(), "title": current['title'],"exception":'[{0}]'.format(e)})

    re['status']='ok'
    re['part_id']=part_id

    return HttpResponse(json.dumps(re, encoding='utf8', indent=4), content_type="application/json")
