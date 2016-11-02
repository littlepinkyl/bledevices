from django.conf.urls import patterns,include,url
from .views import post_drawing
from django.views.decorators.csrf import csrf_exempt


urlpatterns = patterns('map.views',
    #url(r'^admin/', admin.site.urls),
    url(r'^org/$','get_org'),
    url(r'^org/(?P<org_id>\S{24})$','get_org'),
    url(r'^(?P<part_id>\S{24})/drawing$',csrf_exempt(post_drawing))

)