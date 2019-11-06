
import datetime
import logging
from uuid import UUID

from sms_verifier_app.models import Contacts, BroadcastList
from sms_verifier_app.serializers import ApproveGuestSerializer
from sms_verifier_app.views import context
from django.conf import settings

# REST Framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# Define logger
default_logger = logging.getLogger(settings.PROJECT_NAME)


class ContactsList(APIView):
    """
    API will iterate over 'Contacts' model

    A successful call should return:
    {
        "status": "success",
        "message": [
            {
                "first_name": "John",
                "last_name": "Smith",
                "phone_number": "972531234567"
            },
            {
                "first_name": "Alice",
                "last_name": "",
                "phone_number": "972541234567"
            }
        ]
    }
    """
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
    """
    A successful call will return:
    {
        "status": "success",
        "message": [
            {
                "broadcast_name": "br_test_list",
                "event_name": "Wedding on th year",
                "event_date": "2019-11-28",
                "message_content": "Hi {},\r\nThis is a test message content for {}",
                "contacts": [
                    {
                        "first_name": "John",
                        "phone_number": "972531234567",
                        "uuid": "9b64507b-033d-4dd2-aa3f-aab94c82eeb7"
                    },
                    {
                        "first_name": "Alice",
                        "phone_number": "972541234567",
                        "uuid": "0b212b85-ecef-4301-85ec-6495fd2a6f41"
                    }
                ]
            }
        ]
    }
    """
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
                # create list of attendances, of current broadcast list
                attendances_list = [
                    {
                        'first_name': attendance.contact.first_name,
                        'phone_number': attendance.contact.phone_number,
                        'uuid': attendance.uuid,
                    } for attendance in broadcast_list.attendances.all()
                ]

                # Create a list that define an even (message broadcast)
                json_array.append({
                    'broadcast_name': broadcast_list.name,
                    'event_name': broadcast_list.for_event.name,
                    'event_date': broadcast_list.for_event.event_date,
                    'message_content': broadcast_list.for_event.event_message_content,
                    'contacts': attendances_list,
                })

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


# No authentication needed
class ApproveGuestView(APIView):
    """
    This API call will update a guests attendance status,
    once ApproveGuestSerializer is ok, the owner of input uuid status will update
    """
    permission_classes = ()

    @staticmethod
    def post(request):
        serializer = ApproveGuestSerializer(data=request.data)

        # Check format and unique constraint
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        default_logger.info("ApproveGuestView request at: " + str(datetime.datetime.now()))

        data = serializer.data

        try:
            try:
                # Try getting a UUID object for current uuid string received
                uuid_object = UUID(data['uuid'], version=4)
            except ValueError:
                default_logger.info("uuid is not valid")
                message = 'error'
                value = 'uuid is not valid'

                return Response({'status': message, 'message': value}, status=status.HTTP_400_BAD_REQUEST)

            # Next, try getting the relevant guest
            guest = Contacts.objects.get(uuid=uuid_object)

        except Contacts.DoesNotExist:
            default_logger.info("uuid does not exist in db")
            return Response({'status': 'error', 'message': 'uuid does not exist in db'},
                            status=status.HTTP_400_BAD_REQUEST)

        tmp_context = context.copy()
        tmp_context['guest_f_name'] = guest.first_name
        tmp_context['guest_l_name'] = guest.last_name
        tmp_context['uuid'] = guest.uuid

        default_logger.info("{} {}, ")
        print(data)

        response_code = status.HTTP_200_OK
        message = 'success'
        value = ''

        return Response({'status': message, 'message': value}, status=response_code)
