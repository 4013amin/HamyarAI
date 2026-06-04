from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatSession, ChatMessage
import json
from django.http import JsonResponse
from .utils import get_ai_response

# Create your views here.

@login_required
def dashboard_view(request):
    return render(request , 'chat/dashboard.html')


@login_required
def start_chat_view(request , agent_type):
    session = ChatSession.objects.filter(user = request.user , agent_type = agent_type).last()

    if not session:
        session = ChatSession.objects.create(user=request.user ,  agent_type=agent_type)

    return redirect('chat_room', session_id=session.id) 


#Chat room
@login_required
def chat_room_view(request, session_id):
    session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    messages = session.messages.all() 
    
    context = {
        'session': session,
        'chat_messages': messages,
    }
    return render(request, 'chat/chat_room.html', context)


@login_required
def send_message_api(request, session_id):
    if request.method == "POST":
        session = get_object_or_404(ChatSession, id=session_id, user=request.user)
        
        # پردازش درخواست ارسالی به صورت JSON
        try:
            data = json.loads(request.body)
            user_text = data.get("message", "").strip()
        except json.JSONDecodeError:
            user_text = request.POST.get("message", "").strip()

        if not user_text:
            return JsonResponse({"error": "پیام خالی است."}, status=400)

        ChatMessage.objects.create(session=session, sender="user", content=user_text)

        ai_reply = get_ai_response(session, user_text)

        ChatMessage.objects.create(session=session, sender="ai", content=ai_reply)

        return JsonResponse({
            "status": "success",
            "reply": ai_reply
        })

    return JsonResponse({"error": "درخواست نامعتبر است."}, status=405)