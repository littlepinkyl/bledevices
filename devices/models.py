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
        #logger.debug('get_prep_value-------{0}----{1}'.format(value,type(value)))
        if not isinstance(value,ObjectId):
            return ObjectId(value)
        return value

    def to_python(self, value):
        ''' human to python'''
        if not value:#
            return value
        #logger.debug('objectid_to_python---------{0}-------{1}'.format(value, type(value)))
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
        (1,u'Male'),
        (0,u'Female'),
        (-1,u'None'),
    )
    gender=models.IntegerField(choices=genderChoice,default=-1)
    remark=models.CharField(max_length=100,blank=True)
    def __unicode__(self):
        if self.gender in (0,1):
            #logger.debug("%s---%s" % (self,isinstance(self,patientProfile)))
            return "%s--%s" % (self.name,self.genderChoice[self.gender][1])
        else:
            return "None"



class APObject(models.Model):
    pk_id=ObjectIdField(max_length=50,db_column='id',verbose_name='Object ID')
    deviceName=models.CharField(max_length=20,db_column='name',verbose_name='Device name')
    APStatus=(
        (0,u'working'),
        (1,u'not working'),
    )
    status=models.IntegerField(choices=APStatus)
    #gps = EmbedOverrideFloatField('gps')
    longitude=models.FloatField(blank=True)
    latitude=models.FloatField(blank=True)
    create_on = models.DateTimeField('create_on')
    update_by = ObjectIdField(max_length=50,db_column='update_by',verbose_name='update by')
    update_on = models.DateTimeField('update_on')

    class Meta:
        db_table='AP'



    def save(self):
        current={
            "name":self.deviceName,
            "status":self.status,
            "longitude":self.longitude,
            "latitude":self.latitude,
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


class Bracelet(models.Model):
    pk_id = ObjectIdField(max_length=50, db_column='id', verbose_name='Object ID', blank=True)
    #deviceName=models.CharField(max_length=20,db_column='name',verbose_name='Device name'
    #  )
    # TOdo:serial Id field
    deviceName=models.CharField(max_length=10)
    type=models.CharField(max_length=2,default='01')
    macAddress=models.CharField(max_length=17)
    data=models.CharField(max_length=72,blank=True)
    #patientProfile=
    #profile=EmbedOverrideMixedField('patientProfile',blank=True)

    genderChoice=(
        (0,u'Male'),
        (1,u'Female'),
        (-1,u'Other'),
    )


    patientName=models.CharField(max_length=20,blank=True)
    patientGender=models.IntegerField(choices=genderChoice,blank=True)
    patientRemark=models.TextField(blank=True)
    patientPhone=models.CharField(max_length=20,blank=True)

    BStatus=(
        (0,u'not registered'),
        (1,u'registered'),
        (2,u'not used any more'),
        (3,u'other')
    )
    status=models.IntegerField(choices=BStatus,default=0,blank=True)
    create_on = models.DateTimeField('create_on')
    update_by = ObjectIdField(max_length=50,db_column='update_by',verbose_name='update by')
    update_on = models.DateTimeField('update_on')

    class Meta:
        db_table='bracelet'
    def showPatientProfile(self):
        if self.patientName != '' and self.patientGender is not None:
            return "%s/%s/%s" %  (self.patientName,self.genderChoice[self.patientGender][1],self.patientPhone)
    showPatientProfile.short_description='PatientProfile'

    def save(self):
        logger.debug('DEBUG:---self.status---{0}'.format(self.status))
        current={
            "type":self.type,
            "macAddress":self.macAddress,
            "deviceName":self.deviceName,
            "data":self.data,
            "status":self.status,
            "patientName":self.patientName,
            "patientGender":self.patientGender,
            "patientRemark":self.patientRemark,
            "patientPhone":self.patientPhone,
        }
        bracelet=db.bracelet
        pre = bracelet.find_one({'_id': ObjectId(self.pk)})#
        #if self.status==0 and (self.patientName!= '' or self.patientGender!='' or self.patientPhone!='' or self.patientRemark1!=''):
        #    current['patientName']=''
        #    current['patientPhone']=''
        #    current['patientGender']=''
        #    current['patientRemark']=''
#
        #if self.patientName !='' and self.status !=1:
        #    current["status"]=1


        if pre == None:
            now = datetime.datetime.now()
            current['create_on']=now
            current['update_on']=now
            current['update_by']=self.update_by
            #logger.debug('self.profile---{0}----{1}'.format(self.profile,type(self.profile)))


            #current['status']=0

            #logger.debug('DEBUG:---current[profile]---{0}'.format(current['profile']))
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

