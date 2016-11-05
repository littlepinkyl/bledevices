from django.contrib import admin
from bson.objectid import ObjectId
from django import forms
from pymongo import MongoClient
from django.shortcuts import render
import datetime
import logging

from django.conf import settings
logger = logging.getLogger('django')
db_conf = settings.DATABASES['default']
client = MongoClient(db_conf['HOST'], int(db_conf['PORT']))
db = eval("client.{0}".format(db_conf['NAME']))
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _


from .models import APObject,Bracelet
#from map.models import Organization

class APObjectAdmin(admin.ModelAdmin):
    readonly_fields=['pk_id','create_on','update_by','update_on','showMap','isWorking','showCreateBy']

    list_display=('pk_id','deviceName','address','isWorking','create_on')
    list_filter=('create_on','status')
    search_fields=['deviceName','address']
    #fields=('pk_id','deviceName','status','gps')
    fieldsets=[
        ('Main Info',{'fields':['pk_id','deviceName','address','floor',('isWorking','status'),'longitude','latitude','showMap']}),
        ('Other Info',{'fields':['create_on','update_on','showCreateBy']})
    ]
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(APObjectAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ['gps',]:
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield
    def save_model(self, request, obj, form, change):
        #save with the time and the operator id
        obj.update_by = ObjectId(request.user.id)
        obj.save()
    def showMap(self,obj):
        if obj.longitude=='' or obj.latitude =='':
            return "None"
        return '<a href="http://m.amap.com/navi/?dest=%s,%s&destName=%s&hideRouteIcon=1&key=c40e5f9819b11b67f76acb50b492cd04" target="_blank" align="center">Position</a>' % (obj.longitude,obj.latitude,obj.deviceName)
    showMap.allow_tags=True

    #search objectid, deviceName


class BraceletAdmin(admin.ModelAdmin):
    readonly_fields = ['pk_id','create_on','update_by','update_on','patientName','patientGender','patientPhone','patientRemark','data','patientRoom','showCreateBy','unregistered']
    #search_fields=['macAddress']
    #Todo:add list_filter with status, type,
    list_filter=('status',)
    fieldsets=[
        ('Main Info',{'fields':['pk_id','deviceName','type','macAddress','className','data',('unregistered','status')]}),
        ('Patient Details',{'fields':['patientName','patientGender','patientRoom','patientPhone','patientRemark'],'classes':['collapse']}),
        ('Other Info',{'fields':['create_on','update_on','showCreateBy']}),
    ]

    list_display=('pk_id','deviceName','type','macAddress','status','showPatientProfile',)
    #search_fields=['deviceName','type','macAddress','patientName','patientPhone']

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(BraceletAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ['data','profile' ]:
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield

    def save_model(self, request, obj, form, change):
        #save with the time and the operator id
        obj.update_by = ObjectId(request.user.id)
        obj.save()
    #search objectid,devicename,type,macAddress, patient name/phone
    def queryset(self,request):
        #qs=super(parklotAdmin,self).queryset(request)
        qs = self.model._default_manager.get_query_set()
        logger.debug('heyheyhey-----{0}'.format(request.GET))
        ###
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)

        # Custom Search
        # 1. Get the query value and clear it from the request
        q = ''
        try:
            q = request.GET['q']
            copy = request.GET.__copy__()
            copy.__delitem__('q')
            request.GET = copy

        except:
            pass

        result_list = []
#
        # Search on main model (parklot)
        if q != '':
            bracelet_obj_list = self.model.objects.filter(deviceName__contains=q)
            bracelet_obj_list |= self.model.objects.filter(type__exact=q)
            bracelet_obj_list |= self.model.objects.filter(macAddress__contains=q)
            bracelet_obj_list |= self.model.objects.filter(patientName__contains=q)
            bracelet_obj_list |= self.model.objects.filter(patientPhone__contains=q)
            #for result in db.bracelet.find({"$or": [{"addr.city": {"$regex":q}}, {"addr.district": {"$regex":q}}]}):
            #    result_list.append(result['_id'])
            #support to search city,district,street
            # for i in db.parklot.find({"addr":{"$elemMatch":{"author":"joe","score":{"$gte":5}}}}):
            #for i in db.parklot.find({"addr":{"$elemMatch":{"$or": [{"city":/q/},{"street":/q/}]    }}}):
            #    pass
            try:
                bracelet_obj_list |= self.model.objects.filter(pk__exact=ObjectId(q))

            except:
                pass
            logger.debug('heyheyhey----resultlo-{0}'.format(bracelet_obj_list))
        else:
            bracelet_obj_list = self.model.objects.all()
            logger.debug('---{0}'.format(bracelet_obj_list))
        for bracelet in bracelet_obj_list:
                result_list.append(bracelet.pk)

        # Search on the other related model (Other Name)
        #other_names_obj_list = OtherName.objects.filter(name__contains=q)
        #for other_name in other_names_obj_list:
        #    result_list.append(other_name.person.pk)
        return qs.filter(pk__in=result_list)
# Register your models here.
admin.site.register(APObject,APObjectAdmin)
admin.site.register(Bracelet,BraceletAdmin)