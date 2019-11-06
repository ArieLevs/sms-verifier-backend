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
    url(r'^events_list_view/', views.events_list_view, name='events_list_view'),
    url(r'^broadcasts_list_view/', views.broadcasts_list_view, name='broadcasts_list_view'),

    url(r'^guest/(?P<uuid>[a-z0-9\-]+)/', views.verify_guest_uuid, name='guest_uuid'),
    url(r'^approve_guest/', views_api.ApproveGuestView.as_view(), name='approve_guest'),

    # REST API urls
    url(r'^contacts_list/', views_api.ContactsList.as_view(), name='contacts_list'),
    url(r'^broadcast_lists/', views_api.BroadcastListView.as_view(), name='broadcast_lists'),
    url(r'^health_check/', views_api.HealthCheckView.as_view(), name='health_check'),
]
