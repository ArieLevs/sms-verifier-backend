import datetime
import logging

from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from sms_verifier_app.forms import CSVImportForm
from sms_verifier_app.models import Contacts

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


@login_required()
def upload_contacts(request):
    default_logger.info("upload_contacts request at: " + str(datetime.datetime.now()))
    default_logger.info(str(request))

    tmp_context = context.copy()

    if request.POST:  # If the request if method POST then
        form = CSVImportForm(request.POST, request.FILES)  # Get relevant form from forms.py

        if form.is_valid():  # If form is valid and all data exists in the request then

            contacts_file = request.FILES["filename"]

            # validate contacts file
            if not contacts_file.name.endswith('.csv'):
                default_logger.error('file in not .csv')
                return HttpResponseRedirect('/')

            if contacts_file.multiple_chunks():
                default_logger.error("contacts file is too big ({} MB).".format(contacts_file.size / (1000 * 1000)))
                return HttpResponseRedirect('/')

            # read contacts file and split by newline
            file_data = contacts_file.read().decode("utf-8")
            lines = file_data.split("\n")

            # declare lists for displaying feedback to user
            invalid_contacts_list = []
            duplicate_contacts_list = []
            valid_contacts_list = []

            # iterate over contacts file lines, skipping first (header) line
            for line in lines[1:]:
                # rstrip() id for removing \r if exists
                fields = line.rstrip().split(",")

                # get current contact into a dict with relevant values
                contact_dict = {'first_name': fields[0], 'last_name': fields[1], 'phone_number': fields[2]}

                # since first name is mandatory, it must exist, if not update invalid_contacts_list
                if contact_dict['first_name'] is None or '':
                    default_logger.error('invalid contact {}, '
                                         'first name must be set, skipping record'.format(contact_dict))
                    invalid_contacts_list.append(contact_dict)
                    continue

                # since phone number is mandatory, it must exist, if not update invalid_contacts_list
                if not contact_dict['phone_number']:
                    default_logger.error('invalid contact {}, '
                                         'phone number must be set, skipping record'.format(contact_dict))
                    invalid_contacts_list.append(contact_dict)
                    continue

                # try creating current contact
                p, created = Contacts.objects.get_or_create(
                    first_name=contact_dict['first_name'],
                    last_name=contact_dict['last_name'],
                    phone_number=contact_dict['phone_number'],
                )

                # if created update valid_contacts_list else update duplicate_contacts_list
                if created:
                    default_logger.info('new contact created: {}'.format(contact_dict))
                    valid_contacts_list.append(contact_dict)
                else:
                    default_logger.error('contact {} already exists in the db'.format(contact_dict))
                    duplicate_contacts_list.append(contact_dict)

            default_logger.info('failed contacts are: {}'.format(invalid_contacts_list))
            default_logger.info('duplicate contacts are: {}'.format(duplicate_contacts_list))

            tmp_context['valid_contacts_list'] = valid_contacts_list
            tmp_context['invalid_contacts_list'] = invalid_contacts_list
            tmp_context['duplicate_contacts_list'] = duplicate_contacts_list
        else:
            # The form is not valid, so and error should be returned
            default_logger.error('Form is not valid, return error')
    else:
        default_logger.info('Request is not POST, return help form')
        form = CSVImportForm()

    tmp_context['form'] = form
    # Render list page with the documents and the form
    return render(
        request,
        template_name=settings.BASE_DIR + '/sms_verifier_app/templates/index.html',
        context=tmp_context,
        status=HttpResponse.status_code,
    )


@login_required()
def contacts_list_view(request):
    default_logger.info("contacts_list_view request at: " + str(datetime.datetime.now()))
    default_logger.info(request)

    # return all contacts from database
    contacts_list = Contacts.objects.all()

    temp_context = context.copy()
    temp_context['contacts_list'] = contacts_list

    return render(
        request,
        settings.BASE_DIR + '/sms_verifier_app/templates/contacts_list.html',
        temp_context,
        status=HttpResponse.status_code,
    )
