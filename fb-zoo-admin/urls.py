from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include(('dashboard.urls', 'fb-zoo-admin'), namespace='dashboard')),
    url(r'^admin/', admin.site.urls),
]
