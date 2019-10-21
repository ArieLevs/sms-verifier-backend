
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def phone_number_validator():
    return RegexValidator(regex=r'^\+?1?\d{12,15}$',
                          message="Phone number must be entered in the format of: '+18501234567'. "
                                  "Minimum 12 digits and up to 15 digits allowed.")


def user_profile_data_validator(value):
    first_name = value.cleaned_data.get('first_name')
    last_name = value.cleaned_data.get('last_name')
    if not first_name or not last_name:
        raise ValidationError('First and Last names are mandatory')
