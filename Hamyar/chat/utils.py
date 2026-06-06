# chat/utils.py

import os
from django.conf import settings
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential
from .prompts import SYSTEM_PROMPTS

def get_ai_response(session, user_message_text):
    token = getattr(settings, 'GITHUB_TOKEN', os.environ.get("GITHUB_TOKEN", None))
    
    if not token:
        return (
            "⚠️ [خطای دسترسی]\n\n"
            "کلید GITHUB_TOKEN یافت نشد. لطفاً ابتدا توکن گیت‌هاب خود را در فایل "
            "settings.py به شکل GITHUB_TOKEN = 'token_shoma' تعریف کنید."
        )

    endpoint = "https://models.github.ai/inference"
    model_name = "deepseek/DeepSeek-V3-0324"  

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )

    system_prompt = SYSTEM_PROMPTS.get(session.agent_type, SYSTEM_PROMPTS['general'])
    
    messages = [
        SystemMessage(content=system_prompt)
    ]

    history = session.messages.all().order_by('-timestamp')[:10]
    for msg in reversed(history):
        if msg.sender == "user":
            messages.append(UserMessage(content=msg.content))
        else:
            messages.append(AssistantMessage(content=msg.content))

    messages.append(UserMessage(content=user_message_text))

    try:
        response = client.complete(
            messages=messages,
            temperature=0.7,   
            top_p=1.0,
            max_tokens=1000,
            model=model_name
        )
        return response.choices[0].message.content
        
    except Exception as e:
        return f"متاسفانه در برقراری ارتباط با سرویس هوش مصنوعی گیت‌هاب خطایی رخ داد: {str(e)}"