from django.conf.urls import url
from sms_verifier_app import views, views_api

app_name = 'sms_verifier_app'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # General
    url(r'^login_page/', views.login_page, name='login_page'),
    url(r'^logout_process/', views.logout_process, name='logout_process'),

    url(r'^upload_contacts/', views.upload_contacts, name='upload_contacts'),
    url(r'^contacts_list_view/', views.contacts_list_view, name='contacts_list_view'),

    # REST API urls
    url(r'^contacts_list/', views_api.ContactsList.as_view(), name='contacts_list'),
    url(r'^broadcast_lists/', views_api.BroadcastListView.as_view(), name='broadcast_lists'),
]
