from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Member

@receiver(pre_save, sender=Member)
def create_user_for_profile(sender, instance, **kwargs):
    if not instance.user_id:
        username = str(instance.noPekerja)
        password = str(instance.noPekerja)
        user = User.objects.create_user(username=username, password=password)
        instance.user = user