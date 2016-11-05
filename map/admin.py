from django.contrib import admin

# Register your models here.
from .models import Organization,Part
from bson import ObjectId

class OrganizatoinAdmin(admin.ModelAdmin):
    readonly_fields=['pk_id','create_on','update_on','showCreateBy']
    list_display=['pk_id','title','address','floors',]
    fieldsets=[
        ('Main data',{'fields':['pk_id','title','parent','address','floors','longitude','latitude']}),
        ('Other Info',{'fields':['create_on','update_on','showCreateBy']})
    ]
    def save_model(self, request, obj, form, change):
        #save with the time and the operator id
        obj.update_by = ObjectId(request.user.id)
        obj.save()
class PartAdmin(admin.ModelAdmin):
    readonly_fields = ['pk_id', 'create_on', 'update_on','showCreateBy']
    list_display=['pk_id','title','floor','parent','owner']

    fieldsets = [
        ('Main data', {'fields': ['pk_id', 'title', 'parent', 'owner', 'floor']}),
        ('Other Info', {'fields': ['create_on', 'update_on','showCreateBy']})
    ]
    def save_model(self, request, obj, form, change):
        #save with the time and the operator id
        obj.update_by = ObjectId(request.user.id)
        obj.save()
admin.site.register(Organization,OrganizatoinAdmin)
admin.site.register(Part,PartAdmin)