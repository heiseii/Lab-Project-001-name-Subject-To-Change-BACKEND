from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re

#Valida que solo tenga letras, numeros y guion bajo
def validate_username(value):
    if not re.match(r'^[a-zA-Z0-9_]+$', value):
        raise ValidationError ('The username only must to have letters, numbers and underscore (_).')
    
#Validacion de password

def validate_password_lenght(value):
    if len(value) < 8 and len(value) > 100:
        raise ValidationError ('Password needs to contain min. 8 characters and max. 100 characters')
    
    if not any(c.isalpha() for c in value):
        raise ValidationError ('Password must to contain minimum one letter')
    
    if not any(c.isdigit() for c in value):
        raise ValidationError ('Password must to contain minimum one digit')


#Formulario

class RegisterForm(forms.Form):
    username = forms.CharField(
        min_length=3,
        max_length=20,
        validators=[validate_username],
        error_messages={
            'required': 'The user is necessary',
            'min_lenght': 'The username needs to have at least 3 characters.',
            'max_lenght': 'The username cannot exceed 20 characters.'
        }
    )

    password = forms.CharField(
        min_length=8,
        validators=[validate_password_lenght],
        error_messages={
            'required': 'The password is obligatory' 
        }
)
    
