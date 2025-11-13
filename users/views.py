from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from users.forms import RegisterForm #LoginForm
from users.models import Conversation, Message
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
                'success': False,
                'message':  (str(e))
                }, status = 500)    

    return JsonResponse ({
        'success': False,
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
                    'success': True,
                    'message': 'Sucessfull login',
                    'user': {
                    'username': user.username,
                    'email': user.email
                }   
            })
            else: 
                return JsonResponse ({
                'success': False,
                'message': 'Incorrect credentials'
            }, status=401)


        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status = 500)


    return JsonResponse ({
            'success': False,
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

#View de conversacion
@csrf_exempt

def create_or_get_conversation(request):
    if request.method == 'POST':
        try:

            #definicion de usuarios
            data = json.loads(request.body)
            user1_id = data.get('user1_id')
            user2_id = data.get('user2_id')

            user1 = User.objects.get(id=user1_id)
            user2 = User.objects.get(id=user2_id)

            #busqueda de conversacion existente
            conversation = Conversation.objects.filter(
                participants= user1
            ).filter(
                participants=user2
            ).first()

            #creacion de conversacion si es que no se encuentra ya una
            if not conversation:       
                conversation = Conversation.objects.create()
                conversation.participants.add(user1, user2)
            return JsonResponse ({
                'success': True,
                'conversation_id': conversation.id,
                'created_at': conversation.created_at.isoformat(),
            })
            


        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'User does not exist',
            },status= 404)
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status= 500)

        
    return JsonResponse({
        'success': False,
        'message': 'Method not allowed',
    },status= 405)

@csrf_exempt
#Obtiene todos los mensajes
def get_messages ( request, conversation_id):
    try:
        conversation = Conversation.objects.get(id=conversation_id)
        messages = conversation.messages.all()

#Saca la informacion de los mensajes 
        messages_data = [{
            'id': msg.sender.id,
            'sender': {
                'id': msg.sender.id,
                'username':msg.sender.username
            },
            'is_read': msg.is_read,
            'content':msg.content,
            'timestamp': msg.timestamp.isoformat(),
        }for msg in messages]

        return JsonResponse({
            'success': True,
            'messages': messages_data
        })


    except Conversation.DoesNotExist:
        return JsonResponse ({
            'success': False,
            'message': 'Conversation not found'
        },status = 404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status= 500)

@csrf_exempt
def get_user_conversations(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        conversations = user.conversations.all()

        conversations_data = [{
            'id': conv.id,
            'participants': [{
                'id': p.id,
                'username': p.username
            } for p in conv.participants.exclude(id=user_id)],
            'last_message': conv.messages.last().content if conv.messages.exists() else None,
            'updated_at': conv.updated_at.isoformat()
        } for conv in conversations]

        return JsonResponse({
            'success': True,
            'conversations': conversations_data
        })

    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'User not found'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)