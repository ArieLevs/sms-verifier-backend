
import datetime
import logging

from sms_verifier_app.models import Contacts
from django.conf import settings

# REST Framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# Define logger
default_logger = logging.getLogger(settings.PROJECT_NAME)


class ContactsList(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        default_logger.info("ContactsListView request at: " + str(datetime.datetime.now()))

        token = request.auth
        email = token.user

        default_logger.info("request from user: " + str(email))

        # return all contacts from database
        contacts_list = Contacts.objects.all()

        if not contacts_list:
            message = 'failed'
            value = 'no contacts found'
            response_code = status.HTTP_204_NO_CONTENT
            default_logger.info('no contacts found')
        else:
            json_array = []

            # Build Json array from the 'contacts_list' response from the DB
            for contact in contacts_list:
                json_array.append({
                    'first_name': contact.first_name,
                    'last_name': contact.last_name,
                    'phone_number': contact.phone_number,
                })  # Append current contact to the array

                default_logger.info(json_array)
            response_code = status.HTTP_200_OK
            message = 'success'
            value = json_array  # Set the final json array to 'value'

        return Response({'status': message, 'message': value}, status=response_code)
