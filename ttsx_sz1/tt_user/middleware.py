'''

    url('^register/$',views.register),
    url('^register_handle/$',views.register_handle),
    url(r'^active(\d+)/$',views.active),
    url('^say_hello/$',views.say_hello),
    url('^center/$',views.center),
    url('^register_name/$',views.register_name),
    url('^login/$',views.login),
    url('^login_handle/$',views.login_handle),
    url('^logout/$',views.logout),
    http://127.0.0.1:8000/user/center/?a=10
    request.path===>/user/center/
    request.get_full_path()==>/user/center/?a=10
'''
class GetPathMiddleware():
    def process_view(self,request,view_func,view_ars,view_kwargs):
        no_path=['/user/register/',
                 '/user/register_handle/',
                 '/user/register_name/',
                 '/user/login/',
                 '/user/login_handle/',
                 '/user/logout/',
                 '/user/yzm/']
        if request.path not in no_path:
            request.session['url_path']=request.get_full_path()
