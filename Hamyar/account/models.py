from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name="درباره من")
    avatar = models.ImageField(upload_to='profile_pics/', blank=True, null=True, verbose_name="تصویر پروفایل")

    def __str__(self):
        return f"پروفایل {self.user.username}"
    

#ساخت به صورت پیشرفض کاربران
@receiver(post_save, sender=User)
def create_user_profile(sender , instanc , created , **kwargs):
    if created:
        Profile.objects.create(user = instanc)


#For Update Profile
@receiver(post_save , sender=User)
def save_user_Profile(sender , instance ,**kwargs):
    instance.Profile.save()
