
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class BooleanField(serializers.Field):
    default_error_messages = {
        'invalid': _('"{input}" is not a valid boolean.')
    }
    initial = None
    TRUE_VALUES = {
        't', 'T',
        'y', 'Y', 'yes', 'YES',
        'true', 'True', 'TRUE',
        'on', 'On', 'ON',
        '1', 1,
        True
    }
    FALSE_VALUES = {
        'f', 'F',
        'n', 'N', 'no', 'NO',
        'false', 'False', 'FALSE',
        'off', 'Off', 'OFF',
        '0', 0, 0.0,
        False
    }
    NULL_VALUES = {'n', 'N', 'null', 'Null', 'NULL', '', None}

    def __init__(self, **kwargs):
        super(BooleanField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            if data in self.TRUE_VALUES:
                return True
            elif data in self.FALSE_VALUES:
                return False
            elif data in self.NULL_VALUES:
                return None
        except TypeError:  # Input is an unhashable type
            pass
        self.fail('invalid', input=data)

    def to_representation(self, value):
        if value in self.NULL_VALUES:
            return None
        if value in self.TRUE_VALUES:
            return True
        elif value in self.FALSE_VALUES:
            return False
        return bool(value)
