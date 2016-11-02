from django.contrib import admin

# Register your models here.
from .models import Organization,Part

class OrganizatoinAdmin(admin.ModelAdmin):
    readonly_fields=['pk_id','create_on','update_on']
    list_display=['pk_id','title','address','floors',]
    fieldsets=[
        ('Main data',{'fields':['pk_id','title','parent','address','floors','longitude','latitude']}),
        ('Other Info',{'fields':['create_on','update_on']})
    ]
class PartAdmin(admin.ModelAdmin):
    readonly_fields = ['pk_id', 'create_on', 'update_on']


    fieldsets = [
        ('Main data', {'fields': ['pk_id', 'title', 'parent', 'owner', 'floor']}),
        ('Other Info', {'fields': ['create_on', 'update_on']})
    ]
admin.site.register(Organization,OrganizatoinAdmin)
admin.site.register(Part,PartAdmin)