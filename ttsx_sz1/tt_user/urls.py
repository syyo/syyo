from django.conf.urls import url
from . import views
urlpatterns=[
    url('^register/$',views.register),
    url('^register_handle/$',views.register_handle),
    url(r'^active(\d+)/$',views.active),
    url('^say_hello/$',views.say_hello),
    url('^center/$',views.center),
    url('^register_name/$',views.register_name),
    url('^login/$',views.login),
    url('^login_handle/$',views.login_handle),
    url('^logout/$',views.logout),
    url('^order/$',views.order),
    url('^site/$',views.site),
    url('^site_handle/$',views.site_handle),
    url('^yzm/$',views.verify_code),
]