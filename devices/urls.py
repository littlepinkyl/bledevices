from django.conf.urls import patterns,include,url
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .views import chart

urlpatterns = patterns('',
    #url(r'^admin/', admin.site.urls),
    url(r'^chart$',csrf_exempt(chart)),
)