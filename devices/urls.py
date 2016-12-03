from django.conf.urls import patterns,include,url
from .views import ap
from django.views.decorators.csrf import csrf_exempt


urlpatterns = patterns('devices.views',
    #url(r'^admin/', admin.site.urls),
    url(r'^ap',csrf_exempt(ap))

)