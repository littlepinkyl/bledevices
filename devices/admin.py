from django.contrib import admin
from bson.objectid import ObjectId
from django import forms
from pymongo import MongoClient
import datetime
import logging
from django.conf import settings
logger = logging.getLogger('django')
db_conf = settings.DATABASES['default']
client = MongoClient(db_conf['HOST'], int(db_conf['PORT']))
db = eval("client.{0}".format(db_conf['NAME']))
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _


from .models import APObject,bracelet

class APObjectAdmin(admin.ModelAdmin):
    readonly_fields=['pk_id']
    fields=('pk_id','deviceName','status','gps')
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(APObjectAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ['gps',]:
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield
    def save_model(self, request, obj, form, change):
        #save with the time and the operator id
        obj.update_by = ObjectId(request.user.id)
        obj.save()

class braceletAdmin(admin.ModelAdmin):
    readonly_fields = ['pk_id']
    fields=('pk_id','type','macAddress','data','profile','status')
    list_display=('pk_id','type','macAddress','profile','status')


    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(braceletAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ['data','profile' ]:
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield

    def save_model(self, request, obj, form, change):
        #save with the time and the operator id
        obj.update_by = ObjectId(request.user.id)
        obj.save()

# Register your models here.
admin.site.register(APObject,APObjectAdmin)
admin.site.register(bracelet,braceletAdmin)