from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver

from .models import Post, Rating, Comment, Image

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.core import serializers


@receiver(pre_delete, sender=Image)
def on_image_pre_delete(sender, instance, **kwargs):
	instance.image.delete(save=False)

@receiver(post_delete, sender=Post)
def broadcast_post_deletion(sender, instance, **kwargs):
	channel_layer = get_channel_layer()
	async_to_sync(channel_layer.group_send)(
		instance.get_unique_name(),
		{
			'type': 'post_deletion_broadcast',
			'pid': instance.id,
		}
	)

@receiver(post_save, sender=Rating)
def broadcast_update_post_rate_create_update(sender, instance, created, **kwargs):
	channel_layer = get_channel_layer()
	name = instance.name
	async_to_sync(channel_layer.group_send)(
		instance.post.get_unique_name(),
		{
			'type': 'post_rate_update_broadcast',
			'pid': instance.post.id,
			'name': name,
			'like_count': instance.post.like_count(),
			'dislike_count': instance.post.dislike_count(),
		}
	)

@receiver(post_delete, sender=Rating)
def broadcast_update_post_rate_remove(sender, instance, **kwargs):
	channel_layer = get_channel_layer()
	name = instance.name
	async_to_sync(channel_layer.group_send)(
		instance.post.get_unique_name(),
		{
			'type': 'post_rate_update_broadcast',
			'pid': instance.post.id,
			'name': name,
			'like_count': instance.post.like_count(),
			'dislike_count': instance.post.dislike_count(),
		}
	)

@receiver(post_save, sender=Comment)
def broadcast_update_post_comment_created(sender, instance, created, **kwargs):
	channel_layer = get_channel_layer()

	async_to_sync(channel_layer.group_send)(
		instance.post.get_unique_name(),
		{
			'type': 'post_comment_update_broadcast',
			'pid': instance.post.id,
			'serialize_comment': serializers.serialize('json', [instance]),
			'new_count': instance.post.comment_set.all().count(),
		}
	)

@receiver(post_delete, sender=Comment)
def broadcast_update_post_comment_deleted(sender, instance, **kwargs):
	channel_layer = get_channel_layer()

	async_to_sync(channel_layer.group_send)(
		instance.post.get_unique_name(),
		{
			'type': 'post_comment_delete_broadcast',
			'pid': instance.post.id,
			'cid': instance.id,
			'new_count': instance.post.comment_set.all().count(),
		}
	)