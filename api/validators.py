import re
from django.core.exceptions import ValidationError

def validate_strong_password(value):
    if len(value) < 8:
        raise ValidationError("A senha deve conter pelo menos 8 caracteres.")
    if len(value) > 255:
        raise ValidationError("A senha deve conter menos de 256 caracteres")
    if not re.search(r'[A-Z]', value):
        raise ValidationError("A senha deve conter pelo menos uma letra maiúscula.")
    if not re.search(r'[a-z]', value):
        raise ValidationError("A senha deve conter pelo menos uma letra minúscula.")
    if not re.search(r'\d', value):
        raise ValidationError("A senha deve conter pelo menos um número.")