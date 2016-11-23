from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_new_user/$', views.add_new_user),
    url(r'^verify_login/$', views.verify_login),
    url(r'^logout_user/$', views.logout_user),
    url(r'^social_login/$', views.social_login),
    url(r'^upload/$', views.upload),
    url(r'^update/$', views.add_audio_details),
    url(r'^send_followers/$', views.send_followers),
    url(r'^profile/(?P<requested_profile_link>[^/]+)/$', views.show_user_profile),
    url(r'^add_follower/$', views.add_follower_to_user),
    url(r'^create_feed/$', views.create_feed),
]