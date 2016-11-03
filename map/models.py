from __future__ import unicode_literals
from bson.objectid import ObjectId
from django.db import models
from pymongo import MongoClient
import logging
from django.conf import settings
from djangotoolbox.fields import EmbeddedModelField
#from .forms import ObjectListFloatField,ObjectMixedField
import datetime
# Create your models here.
db_conf = settings.DATABASES['default']
client = MongoClient(db_conf['HOST'], int(db_conf['PORT']))
db = eval("client.{0}".format(db_conf['NAME']))
logger = logging.getLogger('django')

# Create your models here.
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

class Organization(models.Model):
    pk_id=ObjectIdField(max_length=50,verbose_name='Organization Id',db_column='id')
    title=models.CharField(max_length=20)
    address=models.CharField(max_length=50)
    floors=models.IntegerField(default=1)
    longitude=models.FloatField()
    latitude=models.FloatField()
    create_on=models.DateTimeField()
    update_on=models.DateTimeField()
    parent=ObjectIdField(blank=True,max_length=50)

    #bounds
    class Meta:
        db_table='organization'

    def save(self):
        current={
            "title":self.title,
            "address":self.address,
            "floors":self.floors,
            "longitude":self.longitude,
            "latitude":self.latitude,
        }
        if self.parent != '':
            current['parent']=ObjectId(self.parent)
        else:
            current['parent']=''
        organization=db.organization
        pre = organization.find_one({'_id': ObjectId(self.pk)})
        if pre == None:
            now = datetime.datetime.now()
            current['create_on']=now
            current['update_on']=now
            #current['update_by']=self.update_by
            #status

            pre_id = organization.insert_one(current).inserted_id
            # if not exist, insert and print id here, if true then success
        else:
            # if exist, update it manually
            now = datetime.datetime.now()
            current['update_on'] = now
            #current['update_by'] = self.update_by
            #logger.debug('123123123123............')
            res = organization.update_one({'_id': ObjectId(self.pk)},
                                   {'$set': current})
            if res == 1:
                #print '[DEBUG]:save successfully!'
                pass


class Part(models.Model):
    pk_id=ObjectIdField(max_length=50,verbose_name='Part Id',db_column='id')
    title=models.CharField(max_length=20)
    floor=models.IntegerField(blank=True)
    create_on=models.DateTimeField()
    update_on=models.DateTimeField()
    parent=ObjectIdField(blank=True,max_length=50)
    owner=ObjectIdField(blank=True,max_length=50)

    class Meta:
        db_table='part'

    def save(self):
        current={
            "title":self.title,
            "floor":self.floor,
        }
        if self.parent != '':
            current['parent']=ObjectId(self.parent)
        if self.owner != '':
            current['owner']=ObjectId(self.owner)

        part=db.part
        pre = part.find_one({'_id': ObjectId(self.pk)})
        if pre == None:
            now = datetime.datetime.now()
            current['create_on']=now
            current['update_on']=now
            #current['update_by']=self.update_by
            #status

            pre_id = part.insert_one(current).inserted_id
            # if not exist, insert and print id here, if true then success
        else:
            # if exist, update it manually
            now = datetime.datetime.now()
            current['update_on'] = now
            #current['update_by'] = self.update_by
            #logger.debug('123123123123............')
            res = part.update_one({'_id': ObjectId(self.pk)},
                                   {'$set': current})
            if res == 1:
                #print '[DEBUG]:save successfully!'
                pass

class Drawable(models.Model):
    pk_id=ObjectIdField(max_length=50,verbose_name='Drawable Id',db_column='id')
    title=models.CharField(max_length=20)
    type=models.CharField(max_length=20)
    data=models.TextField()
    longitude=models.FloatField()
    latitude=models.FloatField()
    level=models.IntegerField(blank=True)
    create_on=models.DateTimeField(blank=True)
    update_on=models.DateTimeField(blank=True)
    part=ObjectIdField(max_length=50)

    class Meta:
        db_table='drawable'

