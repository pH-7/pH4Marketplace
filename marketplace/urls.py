from django.conf.urls import url, include
from django.contrib import admin

from marketplaceapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^gigs/(?P<id>[0-9]+)/$', views.gig_details, name='gig_details'),
    url(r'^social/', include('social_django.urls', namespace='social')),
    url(r'^auth/', include('django.contrib.auth.urls', namespace='auth')),
]
