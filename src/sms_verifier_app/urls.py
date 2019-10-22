from django.conf.urls import url
from . import views

app_name = 'sms_verifier_app'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # General
    url(r'^login_page/', views.login_page, name='login_page'),
    url(r'^logout_process/', views.logout_process, name='logout_process'),

    url(r'^upload_contacts/', views.upload_contacts, name='upload_contacts'),
    url(r'^contacts_list_view/', views.contacts_list_view, name='contacts_list_view')
]
