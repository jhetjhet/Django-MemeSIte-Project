from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver

from django.conf import settings
from .models import Profile, FollowInfo

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.db.models import F

@receiver(pre_save, sender=Profile)
def delete_left_profile_pictures__post_save(sender, instance, **kwargs):
	try:
		old_profile = Profile.objects.get(pk=instance.pk)
		if old_profile.picture.name != Profile.DEFAULT_PROFILE_PICTURE and old_profile.picture != instance.picture:
			old_profile.picture.delete(save=False)
	except Profile.DoesNotExist:
		pass

@receiver(pre_delete, sender=Profile)
def delete_left_profile_pictures__pre_delete(sender, instance, **kwargs):
	if instance.picture.name != Profile.DEFAULT_PROFILE_PICTURE:
		instance.picture.delete(save=False)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def add_profile_on_new_user(sender, instance, created, **kwargs):
	if created:
		Profile(user=instance).save()

@receiver(post_delete, sender=FollowInfo)
@receiver(post_save, sender=FollowInfo)
def broadcast_user_follow_updates(instance, **kwargs):
	user = instance.following
	if user.followers_count > 0 and not 'created' in kwargs:
		user.followers_count = F('followers_count') - 1
	else:
		user.followers_count = F('followers_count') + 1
	user.save(update_fields=['followers_count'])
	channel_layer = get_channel_layer()
	async_to_sync(channel_layer.group_send)(
		instance.following.username,
		{
			'type': 'user_follow_updates_broadcast',
			'uid': instance.following.id,
			'new_follower_count': instance.following.followers.all().count(),
		}
	)