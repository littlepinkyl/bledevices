from __future__ import unicode_literals
from bson.objectid import ObjectId
from django.db import models
from pymongo import MongoClient
import logging
from django.conf import settings
from djangotoolbox.fields import EmbeddedModelField
from .forms import ObjectListFloatField,ObjectMixedField
import datetime
# Create your models here.
db_conf = settings.DATABASES['default']
client = MongoClient(db_conf['HOST'], int(db_conf['PORT']))
db = eval("client.{0}".format(db_conf['NAME']))
logger = logging.getLogger('django')

class ObjectIdField(models.CharField):
    """    model Fields for objectID    """
    #http://django-chinese-docs.readthedocs.io/en/latest/howto/custom-model-fields.html?highlight=to_python#django.db.models.Field.to_python
    __metaclass__ = models.SubfieldBase

    def get_prep_value(self,value):
        logger.debug('get_prep_value-------{0}----{1}'.format(value,type(value)))
        if not isinstance(value,ObjectId):
            return ObjectId(value)
        return value

    def to_python(self, value):
        ''' human to python'''
        if not value:#
            return value
        logger.debug('objectid_to_python---------{0}-------{1}'.format(value, type(value)))
        return value

class EmbedOverrideFloatField(EmbeddedModelField):#
    def formfield(self, **kwargs):
        return models.Field.formfield(self, ObjectListFloatField, **kwargs)
class EmbedOverrideMixedField(EmbeddedModelField):#
    def formfield(self, **kwargs):
        return models.Field.formfield(self, ObjectMixedField, **kwargs)
class gps(models.Model):
    ##
    longitude=models.FloatField()
    latitude=models.FloatField()
    def __unicode__(self):
        return "%f,%f" % (self.longitude,self.latitude)

class patientProfile(models.Model):
    name=models.CharField(max_length=10)
    genderChoice=(
        (0,u'Male'),
        (1,u'Female'),
    )
    gender=models.IntegerField(choices=genderChoice)
    remark=models.CharField(max_length=100,blank=True)





class APObject(models.Model):
    pk_id=ObjectIdField(max_length=50,db_column='id',verbose_name='Object ID')
    deviceName=models.CharField(max_length=20,db_column='name',verbose_name='Device name')
    APStatus=(
        (0,u'working'),
        (1,u'not working'),

    )
    status=models.IntegerField(choices=APStatus)
    gps = EmbedOverrideFloatField('gps')
    create_on = models.DateTimeField('create_on')
    update_by = ObjectIdField(max_length=50,db_column='update_by',verbose_name='update by')
    update_on = models.DateTimeField('update_on')
    class Meta:
        db_table='AP'

    def save(self):
        current={
            "name":self.deviceName,
            "status":self.status,
            "gps":{
                "longitude": self.gps.longitude,
                "latitude": self.gps.latitude,
            },
        }
        AP=db.AP
        pre = AP.find_one({'_id': ObjectId(self.pk)})
        if pre == None:
            now = datetime.datetime.now()
            current['create_on']=now
            current['update_on']=now
            current['update_by']=self.update_by
            #status


            pre_id = AP.insert_one(current).inserted_id
            # if not exist, insert and print id here, if true then success
        else:
            # if exist, update it manually
            now = datetime.datetime.now()
            current['update_on'] = now
            current['update_by'] = self.update_by
            #logger.debug('123123123123............')
            res = AP.update_one({'_id': ObjectId(self.pk)},
                                   {'$set': current})
            if res == 1:
                #print '[DEBUG]:save successfully!'
                pass


class bracelet(models.Model):
    pk_id = ObjectIdField(max_length=50, db_column='id', verbose_name='Object ID', blank=True)
    #deviceName=models.CharField(max_length=20,db_column='name',verbose_name='Device name')
    type=models.CharField(max_length=2,default='01')
    macAddress=models.CharField(max_length=17)
    data=models.CharField(max_length=72,blank=True)
    #patientProfile=
    profile=EmbedOverrideMixedField('patientProfile')

    BStatus=(
        (0,u'not registered'),
        (1,u'registered'),
        (2,u'not used any more'),
        (3,u'other')

    )
    status=models.IntegerField(choices=BStatus)
    create_on = models.DateTimeField('create_on')
    update_by = ObjectIdField(max_length=50,db_column='update_by',verbose_name='update by')
    update_on = models.DateTimeField('update_on')

    class Meta:
        db_table='bracelet'

    def save(self):
        current={
            "type":self.type,
            "macAddress":self.macAddress,
            "data":self.data,
            "profile":{
                "name": self.profile.name,
                "gender": self.profile.gender,
                "remark":self.profile.remark,
            },
            "status":self.status,
        }
        bracelet=db.bracelet
        pre = bracelet.find_one({'_id': ObjectId(self.pk)})
        if pre == None:
            now = datetime.datetime.now()
            current['create_on']=now
            current['update_on']=now
            current['update_by']=self.update_by
            #status


            pre_id = bracelet.insert_one(current).inserted_id
            # if not exist, insert and print id here, if true then success
        else:
            # if exist, update it manually
            now = datetime.datetime.now()
            current['update_on'] = now
            current['update_by'] = self.update_by
            #logger.debug('123123123123............')
            res = bracelet.update_one({'_id': ObjectId(self.pk)},
                                   {'$set': current})
            if res == 1:
                #print '[DEBUG]:save successfully!'
                pass
