from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from django.contrib.auth.decorators import login_required
from sms_verifier_app import views, views_api


def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)


app_name = 'sms_verifier_app'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # General
    url(r'^login_page/', views.login_page, name='login_page'),
    url(r'^logout_process/', views.logout_process, name='logout_process'),

    url(r'^upload_contacts/', views.upload_contacts, name='upload_contacts'),
    url(r'^contacts_add_view/', views.contacts_add_view, name='contacts_add_view'),
    url(r'^contacts_list_view/', views.contacts_list_view, name='contacts_list_view'),
    url(r'^events_list_view/', views.events_list_view, name='events_list_view'),
    url(r'^broadcasts_list_view/', views.broadcasts_list_view, name='broadcasts_list_view'),
    url(r'^attendance_list_update_view/(?P<event_id>[0-9]+)$',
        views.attendance_list_update_view,
        name='attendance_list_update_view'),

    url(r'^guest/(?P<uuid>[a-z0-9\-]+)/', views.verify_guest_uuid, name='guest_uuid'),
    url(r'^approve_guest/', views_api.ApproveGuestView.as_view(), name='approve_guest'),

    # REST API urls
    url(r'^readiness/', views_api.ReadinessProbe.as_view(), name='readiness'),
    url(r'^liveness/', views_api.LivenessProbe.as_view(), name='liveness'),
    url(r'^contacts_list/', views_api.ContactsList.as_view(), name='contacts_list'),
    url(r'^broadcast_lists/', views_api.BroadcastListView.as_view(), name='broadcast_lists'),
    url(r'^health_check/', views_api.HealthCheckView.as_view(), name='health_check'),

    # Below url will check if user is authorized to view the requested media path
    url(r'^{}(?P<path>.*)$'.format(settings.MEDIA_URL[1:]), protected_serve, {'document_root': settings.MEDIA_ROOT}),
]
