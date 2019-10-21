
from django.contrib import admin
from django.conf.urls import include, url

urlpatterns = [
    url(r'^', include('sms_verifier_app.urls')),

    # oauth urls
    url(r'^', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # django auth urls
    url('^', include('django.contrib.auth.urls')),
    # Social auth urls
    url('', include('social_django.urls', namespace='social')),

    url(r'^admin/', admin.site.urls),
]
