from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ChatSession(models.Model):
    AGENT_CHOICES = [
        ('frontend', 'دستیار فرانت‌اند (Frontend Expert)'),
        ('backend', 'دستیار بک‌اند (Backend Expert)'),
        ('general', 'دستیار عمومی (General Assistant)'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    agent_type = models.CharField(max_length=20, choices=AGENT_CHOICES, verbose_name="نوع ایجنت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان شروع گفتگو")

    def __str__(self):
        return f"{self.user.username} - {self.get_agent_type_display()}"

class ChatMessage(models.Model):
    SENDER_CHOICES = [
        ('user', 'کاربر'),
        ('ai', 'هوش مصنوعی'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages', verbose_name="جلسه چت")
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES, verbose_name="فرستنده")
    content = models.TextField(verbose_name="متن پیام")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="زمان ارسال")

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.get_sender_display()}: {self.content[:30]}..."