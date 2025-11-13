from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import re

#Valida que solo tenga letras, numeros y guion bajo

def validate_username(value):
    if not re.match(r'^[a-zA-Z0-9_]+$', value):
        raise ValidationError ('The username only must to have letters, numbers and underscore (_).')
    
#Validacion de password

def validate_password_strenght(value):
    if len(value) < 8 or len(value) > 100:
        raise ValidationError ('Password needs to contain min. 8 characters and max. 100 characters')
    
    if not any(c.isalpha() for c in value):
        raise ValidationError ('Password must to contain minimum one letter')
    
    if not any(c.isdigit() for c in value):
        raise ValidationError ('Password must to contain minimum one digit')


#Formulario de registro

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
        validators=[validate_password_strenght],
        error_messages={
            'required': 'The password is obligatory' 
        }
    )
    
    email = forms.EmailField(
        required=False,
        error_messages={
            'invalid': 'Use valid methods'
        }
    )


    def clean_username(self):

        # Esto ''limpia'' los datos ingresados por el usuario
        username = self.cleaned_data.get ('username')

        if User.objects.filter(username==username).exists():
            raise ValidationError(
                'The username already exists'
            ) 
        return username
        

    def clean_email(self):

        # Esto ''limpia'' los datos ingresados por el usuario
        email = self.cleaned_data.get ('email')

        if User.objects.filter(email==email).exists():
            raise ValidationError(
                'The Email already exists'
            )
        return email


#class LoginForm(forms.Form):

    #def login_user_verification(self):
    
        
        
