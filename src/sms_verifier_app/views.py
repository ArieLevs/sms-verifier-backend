import datetime
import logging

from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect

# Define logger
default_logger = logging.getLogger(settings.PROJECT_NAME)

context = {
    'project_name': settings.PROJECT_NAME,
    'developer': 'Arie Lev',
    'current_year': datetime.datetime.now().year,
    'version': settings.VERSION,
    'hostname': settings.HOSTNAME,
    'environment': settings.ENVIRONMENT,
}


# Render main index page
def index(request):
    default_logger.info("index request at: " + str(datetime.datetime.now()))
    default_logger.info(request)

    return render(
        request,
        settings.BASE_DIR + '/sms_verifier_app/templates/index.html',
        context,
        status=HttpResponse.status_code,
    )


def login_page(request):
    default_logger.info("login_page request at: " + str(datetime.datetime.now()))
    default_logger.info(request)

    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        return render(
            request,
            settings.BASE_DIR + '/sms_verifier_app/templates/login.html',
            context,
            status=HttpResponse.status_code,
        )


def logout_process(request):
    default_logger.info("logout_process request at: " + str(datetime.datetime.now()) + " by user: " + str(request.user))

    logout(request)
    return HttpResponseRedirect('/')
