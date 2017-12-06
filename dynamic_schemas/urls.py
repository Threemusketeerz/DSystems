from django.conf.urls import url

from . import views


app_name = 'dynamic_schemas'
urlpatterns = [
    url(r'^$', views.SchemaIndexView.as_view(), name='schema_list'),
    # url(r'^(?P<pk>[0-9]+)/$', views.SchemaView, name='schema_detail'),
    url(r'^(?P<pk>[0-9]+)/create/$', views.form_view, name='create_form'),
    # url(r'^(?P<pk>[0-9]+)/(?P<r_pk>[0-9]+)/update/$',
        # views.ResponseUpdate.as_view(), name='update_response'),
    url(r'^(?P<pk>[0-9]+)/(?P<r_pk>[0-9]+)/update/$',
        views.form_update_view, name='update_response'),
    url(r'^(?P<pk>[0-9]+)/responses/$', views.ResponseList.as_view(),
        name='list_responses'),
    url(r'^(?P<pk>[0-9]+)/$', views.SchemaView.as_view(), name='schema_view'),
]

