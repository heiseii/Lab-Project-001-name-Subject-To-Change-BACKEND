from django.shortcuts import render


from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt

#Register View
def register_api(request):
    if request.method == 'POST':
        try:
            
            #Recibir datos del front (Json)

            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email', '')

            #Validar que no se entreguen datos incorrectos

            
            if not username or not password: 
                return JsonResponse({
                    'sucess' : False,
                    'message': 'User and password required'

                }, status=400)  

            
                #Validar que el usuario exista

            if User.objects.filter (username=username).exists():
                return JsonResponse({
                    'sucess' : False,
                    'message': 'User already exists'

                }, status = 400)
            
                #Creacion de usuario exitosa

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            return JsonResponse ({
                    'sucess' : True,
                    'message': 'User was created satisfactorily',
                    
            }, status = 201)
        
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
