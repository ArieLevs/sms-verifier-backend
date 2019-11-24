from sms_verifier_app.models import EventAttendances


def get_not_responded_attendances_for_event(event):
    """
    return a list of EventAttendances objects, where 'is_responded' value is false for current event
    :param event: Event
    :return: list of EventAttendances
    """
    return EventAttendances.objects.filter(event=event, is_responded=False)


def get_attending_attendances_for_event(event):
    """
    return a list of EventAttendances objects, that attended to an event
    :param event:
    :return:
    """
    return EventAttendances.objects.filter(event=event, is_attending=True)
