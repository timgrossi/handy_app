from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^process_new_user$', views.process_new_user),
    url(r'^process_login$', views.process_login),
    url(r'^process_job$', views.process_job),
    url(r'^process_edit/(?P<id>[0-9]+)$', views.process_edit),
    url(r'^create_job$', views.create),
    url(r'^jobs/(?P<id>[0-9]+)$', views.view_job),
    url(r'^dashboard$', views.dashboard),
    url(r'^jobs/edit/(?P<id>[0-9]+)$', views.edit_job),
    url(r'^logout$', views.logout),
    url(r'^delete/(?P<id>[0-9]+)$', views.delete),
]