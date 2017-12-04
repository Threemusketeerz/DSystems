from django.conf.urls import url

from . import views


app_name = 'dynamic_schemas'
urlpatterns = [
    url(r'^$', views.SchemaIndexView.as_view(), name='schema_list'),
    # url(r'^(?P<pk>[0-9]+)/$', views.SchemaView, name='schema_detail'),
    url(r'^(?P<pk>[0-9]+)/$', views.form_view),
    url(r'^(?P<pk>[0-9]+)/success/$', views.success_view),
]

