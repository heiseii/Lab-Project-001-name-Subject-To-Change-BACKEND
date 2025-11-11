from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from users.forms import RegisterForm #LoginForm
import json

@csrf_exempt

#Register View
def register_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            form = RegisterForm(data)

            if not form.is_valid():
                return JsonResponse({
                    'success': False,
                    'errors': form.errors,
                }, status=400)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data.get('email')

            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'User already exists'
                }, status=400)

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )

            return JsonResponse({
                'success': True,
                'message': 'User was created successfully',
                'user': {
                    'username': user.username,
                    'email': user.email,
                }
            }, status=201)
        
        except Exception as e:
            
            return JsonResponse ({
                'sucess': False,
                'message':  (str(e))
                }, status = 500)    

    return JsonResponse ({
        'sucess': False,
        'message' : 'Method not allowed'
        }, status = 405)


#Login View
@csrf_exempt
def login_api(request):
    if request.method == 'POST':


        try:

            

            data = json.loads(request.body)
            username = data.get ('username')
            password = data.get ('password')

            user = authenticate(request, username=username, password=password)


            if user is not None:
                login(request, user)
                return JsonResponse({
                    'sucess': True,
                    'message': 'Sucessfull login',
                    'user': {
                    'username': user.username,
                    'email': user.email
                }   
            })
            else: 
                return JsonResponse ({
                'sucess': False,
                'message': 'Incorrect credentials'
            }, status=401)


        except Exception as e:
            return JsonResponse({
                'sucess': False,
                'message': str(e)
            }, status = 500)


        return JsonResponse ({
            'sucess': False,
            'message' : 'Method not allowed'
        }, status = 405)
    

#Logout view
@csrf_exempt
def logout_api(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({
            'success': True,
            'message': 'Logout exitoso'
        })
    
    return JsonResponse({
        'success': False,
        'message': 'Method not allowed'
    }, status=405)
