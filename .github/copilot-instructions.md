# Copilot Instructions - Django Messaging Backend

## Architecture Overview

This is a Django 5.2 messaging application with WebSocket support using Channels.

### Key Components:
- **Users App**: Authentication, user management, conversations & messages
- **Models**: 
  - `User` (Django built-in)
  - `Conversation` (M2M relationship with participants, auto-ordered by `-updated_at`)
  - `Message` (FK to Conversation + User, timestamps, read status)
- **Real-time**: Django Channels with AsyncWebsocketConsumer for WebSocket chat
- **Frontend**: Vite + React (localhost:5173) with CORS enabled

### Data Flow:
1. User authenticates via `/register/` or `/login/` → Session stored
2. Initiate chat: POST `/conversations/create/` with `user1_id`, `user2_id`
3. Fetch conversations: GET `/user/<user_id>/conversations/`
4. Real-time chat: WebSocket connection to `ws/chat/<conversation_id>/` sends/receives JSON messages
5. Historical messages: GET `/conversations/<conversation_id>/messages/`

## Project-Specific Patterns

### API Response Format:
All endpoints return JSON with `success` boolean + data/error:
```json
{
  "success": true,
  "data": {...}
}
```
Use `@csrf_exempt` decorator on views (CORS setup in settings already handles credentials).

### WebSocket Message Format:
```json
{
  "message": "text content",
  "sender_id": 1,
  "sender_username": "john",
  "timestamp": "2025-11-24T10:30:00Z"
}
```

### Conversation Lookup:
Always use `.filter().filter().first()` pattern (see `create_or_get_conversation`) to find conversations by checking both participants exist in same conversation.

## Key Files & Responsibilities

| File | Purpose |
|------|---------|
| `users/models.py` | Conversation, Message schemas with relationships |
| `users/views.py` | REST API endpoints (register, login, conversations, messages) |
| `users/consumers.py` | WebSocket consumer for real-time chat |
| `users/routing.py` | WebSocket URL routing (Channels) |
| `msj_proyect/settings.py` | CHANNEL_LAYERS (InMemory), CORS, INSTALLED_APPS |
| `msj_proyect/asgi.py` | ASGI app for Channels (check if configured) |

## Developer Workflows

### Run Development Server:
```powershell
python manage.py runserver
```
Auto-reloads, WebSocket available at ws://localhost:8000

### Create Database Migrations:
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Common Issues:
- **InMemoryChannelLayer**: Only works in single-process. For production/multi-worker, use Redis (channels-redis)
- **CSRF exempt + CORS**: Frontend can send credentials across origins
- **Message save bug**: `consumers.py` line uses `User.objects.get(id=self.conversation_id)` - should be `Conversation.objects.get(id=self.conversation_id)` (FIX THIS)

## Next Steps Template

When adding features:
1. Add model fields/relations to `users/models.py`
2. Create view with `@csrf_exempt` in `users/views.py`
3. Add URL pattern in `users/urls.py`
4. If real-time needed: extend `ChatConsumer` in `users/consumers.py`
5. Update routing in `users/routing.py` if new WebSocket endpoints
6. Test with frontend at localhost:5173

## Dependencies
- Django 5.2.8 (ORM, auth, sessions)
- Channels 4.2.1 (WebSocket support, async)
- Daphne (ASGI server for Channels)
- django-allauth (OAuth integration)
- django-cors-headers (CORS middleware)

---
*Last updated: Nov 24, 2025 | For DB schema details, see migrations/0001_initial.py*
