#-*- coding=utf-8 -*-
from django import forms
import datetime
import json
import logging
logger = logging.getLogger('django')
def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        logger.debug('this is not json---{0}'.format(myjson))
        return False
    return True


class ObjectListFloatField(forms.FloatField):
    def prepare_value(self, value):
        if not value:
            return ''
        newvalue = {}

        for key, val in value.__dict__.items():
            if type(val) is float:
                newvalue[key] = val
        # Integer, Date,  Float,
        return json.dumps(newvalue,indent=4)
    def to_python(self, value):
        if not value:
            return {}
        obj = {}
        if is_json(value):
            obj=json.loads(value)
        return obj

class ObjectMixedField(forms.CharField,forms.IntegerField):
    def prepare_value(self,value):
        if not value:
            return ''

        newvalue = {}

        for key, val in value.__dict__.items():
            if type(val) is unicode or type(val) is int:
                newvalue[key] = val
            elif  type(val) is datetime.datetime :
                newvalue[key] = str(val)
        return json.dumps(newvalue,indent=4)

    def to_python(self,value):
        if not value:
            return {}
        obj={}
        if is_json(value):
            obj=json.loads(value)
            logger.debug('DEBUG:to_python-----{0}'.format(obj))
            #del obj['update_by']
            #del obj['update_on']
        else:
            logger.debug('----{0}'.format("error!!"))
        return obj