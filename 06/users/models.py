from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField(max_length=128)
    position = models.CharField(max_length=128)
    subjects = models.CharField(max_length=128)
    image = models.ImageField(upload_to='profile/', default='default.png')

@receiver(post_save, sender=User)
# post_save 이벤트를 발생시켰을 때 해당 이벤트가 일어났다는 사실을 받아,
# 해당 유저 인스턴스와 연결되는 프로필 데이터 생성
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)