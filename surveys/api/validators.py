import re
from rest_framework.serializers import ValidationError


def validate_user_id(value):
    # регулярное выражение для проверки идентификационного номера
    pattern = r'^[a-zA-Z0-9]{10}$'
    if not re.match(pattern, value):
        raise ValidationError(
            'Идентификационный номер должен состоять из 10 цифр и/или букв '
            'в любом регистре, без знаков препинания'
        )
