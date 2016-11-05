#-*- coding: utf-8 -*-

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
    status=models.IntegerField(choices=APStatus,help_text='对于working,暂时无法默认显示读取值,保存前需要修改为非空')
    def isWorking(self):
        return self.status == 0
    isWorking.boolean=True

    floor=models.IntegerField(null=True,default=0)
    address=models.TextField(blank=True)

    #gps = EmbedOverrideFloatField('gps')
    longitude=models.FloatField(blank=True)
    latitude=models.FloatField(blank=True)
    create_on = models.DateTimeField('create_on')
    update_by = ObjectIdField(max_length=50,db_column='update_by',verbose_name='update by',null=True)
    update_on = models.DateTimeField('update_on',null=True)

    class Meta:
        db_table='accesspoint'

    def showCreateBy(self):
        if self.update_by =='':
            return 'None'
        user=db.auth_user
        i = user.find_one({'_id':ObjectId(self.update_by)})
        if i :
            if i['last_name'] or i['first_name']:
                return "%s (%s%s)" % (i['username'],i['last_name'],i['first_name'])
            else:
                return "%s" % (i['username'],)
    showCreateBy.short_description='Create By'


    def save(self):
        current={
            "name":self.deviceName,
            "status":self.status,
            "longitude":self.longitude,
            "latitude":self.latitude,
            "floor":self.floor,
            "address":self.address
        }
        logger.debug('[0]--{0}'.format(self.status))
        AP=db.accesspoint
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
    type=models.CharField(max_length=2,default='01',blank=True)
    macAddress=models.CharField(max_length=17,blank=True)
    data=models.CharField(max_length=60,blank=True)
    className=models.CharField(max_length=50,blank=True,db_column='_class')
    #patientProfile=
    #profile=EmbedOverrideMixedField('patientProfile',blank=True)

    genderChoice=(
        ('F',u'Female'),
        ('M',u'Male'),
        ('O',u'Other'),
        ('',u''),
    )

    patientName=models.CharField(max_length=20,blank=True)
    patientGender=models.CharField(choices=genderChoice,blank=True,max_length=1,null=True)
    patientRemark=models.TextField(blank=True)
    patientPhone=models.CharField(max_length=20,blank=True)
    patientRoom=models.CharField(max_length=30,blank=True)

    BStatus=(
        (0,u'not registered'),
        (1,u'registered'),
        (2,u'not used any more'),
        (3,u'other')
    )
    status=models.IntegerField(choices=BStatus,help_text='若未注册,暂时无法默认显示读取值,保存前需要修改为非空')
    def unregistered(self):
        return self.status == 0
    unregistered.boolean=True
    create_on = models.DateTimeField(db_column='create_on',blank=True,null=True)
    update_by = ObjectIdField(max_length=50,db_column='update_by',verbose_name='update by',blank=True)
    update_on = models.DateTimeField(db_column='update_on',blank=True,null=True)

    class Meta:
        db_table='bracelet'
    def showPatientProfile(self):
        gender=''
        if self.patientName != '' and self.patientGender is not None:
            for i in self.genderChoice:
                if i[0] == self.patientGender:
                    gender=i[1]
                    break
            if gender =='':
                gender='invalid value'
            return "%s/%s/%s" %  (self.patientName,gender,self.patientPhone)
    showPatientProfile.short_description='PatientProfile'

    def showCreateBy(self):
        if self.update_by =='':
            return 'None'
        user=db.auth_user
        i = user.find_one({'_id':ObjectId(self.update_by)})
        if i :
            if i['last_name'] or i['first_name']:
                return "%s (%s%s)" % (i['username'],i['last_name'],i['first_name'])
            else:
                return "%s" % (i['username'],)
    showCreateBy.short_description='Create By'

    def save(self):
        logger.debug('DEBUG:---self.status---{0}'.format(self.status))
        current={
            "type":self.type,
            "macAddress":self.macAddress,
            "deviceName":self.deviceName,
            "status":self.status,
            "className":self.className,
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

