from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#from NeitzModel import settings
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'NeitzModel.views.emmetrop', name='emmetrop'),
    url(r'^colorspace/', 'NeitzModel.views.color', name='colorspace'),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)
