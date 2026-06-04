import openai
from django.conf import settings
from .prompts import SYSTEM_PROMPTS

def get_ai_response(session, user_message_text):
    api_key = getattr(settings, 'OPENAI_API_KEY', None)
    
    if not api_key:
        return (
            f"⚠️ [حالت دمو فعال است]\n\n"
            f"دستیار تخصصی {session.get_agent_type_display()} پیام شما را دریافت کرد: «{user_message_text}»\n\n"
            f"برای دریافت پاسخ‌های واقعی، لطفاً کلید API هوش مصنوعی (مانند OpenAI یا سرویس‌های دیگر) را تنظیم کنید."
        )

    system_prompt = SYSTEM_PROMPTS.get(session.agent_type, SYSTEM_PROMPTS['general'])
    messages = [{"role": "system", "content": system_prompt}]

    history = session.messages.all().order_by('-timestamp')[:10]
    for msg in reversed(history):
        role = "user" if msg.sender == "user" else "assistant"
        messages.append({"role": role, "content": msg.content})

    messages.append({"role": "user", "content": user_message_text})

    try:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message['content']
        except AttributeError:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
    except Exception as e:
        return f"خطا در برقراری ارتباط با سرور هوش مصنوعی: {str(e)}"