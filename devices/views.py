#-*- coding: utf-8 -*-
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

@csrf_exempt
def chart(request):
    #db.bracelet
    data={}
    logger.debug('base_dir-------------: {0}'.format(settings.BASE_DIR))
    all=db.bracelet_trace.count()
    list=db.bracelet_trace.distinct("bracelet")
    for bracelet in list:
        data[bracelet]=db.bracelet_trace.find({"bracelet":bracelet}).count()/all
    te=[{'data': [['2013-04-01 00:00:00 UTC', 52.9], ['2013-05-01 00:00:00 UTC', 50.7]], 'name': 'Chrome'},
 {'data': [['2013-04-01 00:00:00 UTC', 27.7], ['2013-05-01 00:00:00 UTC', 25.9]], 'name': 'Firefox'}]
    series=[{
            'name': 'Tokyo',
            'data': [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
        }, {
            'name': 'New York',
            'data': [-0.2, 0.8, 5.7, 11.3, 17.0, 22.0, 24.8, 24.1, 20.1, 14.1, 8.6, 2.5]
        }, {
            'name': 'Berlin',
            'data': [-0.9, 0.6, 3.5, 8.4, 13.5, 17.0, 18.6, 17.9, 14.3, 9.0, 3.9, 1.0]
        }, {
            'name': 'London',
            'data': [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
        }]
    title= {
               'text': 'Monthly Average Temperature',
               'x': -20
           },
    subtitle={
                  'text': 'Source: WorldClimate.com',
                  'x': -20
              },
    xAxis={
               'categories': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
           },
    yAxis={
               'title': {
                   'text': 'Temperature (°C)'
               },
               'plotLines': [{
                   'value': 0,
                   'width': 1,
                   'color': '#808080'
               }]
           },
    tooltip={
                 'valueSuffix': '°C'
             },
    legend={
                'layout': 'vertical',
                'align': 'right',
                'verticalAlign': 'middle',
                'borderWidth': 0
            },

    return render(request,'chart.html',{'data':data,'te':te,
                                        'series':series,'title':title,'subtitle':subtitle,'xAxis':xAxis,
                                        'yAxis':yAxis,'tooltip':tooltip,'legend':legend
                                        })