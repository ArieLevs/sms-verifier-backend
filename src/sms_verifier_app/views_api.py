
import datetime
import logging

from sms_verifier_app.models import Contacts, BroadcastList
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
        if token:
            email = token.user
        else:
            email = request.user

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

            response_code = status.HTTP_200_OK
            message = 'success'
            value = json_array  # Set the final json array to 'value'
            default_logger.info(json_array)

        return Response({'status': message, 'message': value}, status=response_code)


class BroadcastListView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        default_logger.info("BroadcastListView request at: " + str(datetime.datetime.now()))

        token = request.auth
        if token:
            email = token.user
        else:
            email = request.user

        default_logger.info("request from user: " + str(email))

        # return all broadcasts lists from database
        broadcast_lists = BroadcastList.objects.all()

        if not broadcast_lists:
            message = 'failed'
            value = 'no broadcasts lists found'
            response_code = status.HTTP_204_NO_CONTENT
            default_logger.info('no broadcasts lists found')
        else:
            json_array = []

            # Build Json array from the 'broadcast_lists' response from the DB
            for broadcast_list in broadcast_lists:
                # create list of contact, of current broadcast list
                contact_list = [
                    {
                        'first_name': a.first_name,
                        'phone_number': a.phone_number
                    } for a in broadcast_list.contacts.all()
                ]

                json_array.append({
                    'name': broadcast_list.name,
                    'message_content': broadcast_list.message_content,
                    'contacts': contact_list,
                })  # Append current list to the array

            response_code = status.HTTP_200_OK
            message = 'success'
            value = json_array  # Set the final json array to 'value'
            default_logger.info(json_array)

        return Response({'status': message, 'message': value}, status=response_code)


class HealthCheckView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        default_logger.info("HealthCheckView request at: " + str(datetime.datetime.now()))

        # Get token from request
        token = request.auth
        email = str(token.user)
        default_logger.info("request from user: " + email)

        message = 'success'

        # If all passed OK return user name
        default_logger.info("Success, health_check passed OK")
        return Response({'status': message, 'message': email}, status=status.HTTP_200_OK)
