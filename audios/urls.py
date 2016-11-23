from django.conf.urls import include,url
from django.contrib import admin

urlpatterns = [
	url(r'^main/',include('main.urls')),
    url(r'^admin/', admin.site.urls),
    url('main/social-auth/',
include('social.apps.django_app.urls', namespace='social')),
]
