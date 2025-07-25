from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def createprofile(sender,instance,created,**kwargs):
	if created:
		Profile.objects.create(user=instance)


@receiver(post_save,sender=User)
def saveprofile(sender,instance,**kwargs):
	instance.profile.save()

#@receiver(post_save, sender=User)
#def update_user_profile(sender, instance, created, **kwargs):
#    if created:
#        Profile.objects.create(user=instance)
#        instance.profile.save()