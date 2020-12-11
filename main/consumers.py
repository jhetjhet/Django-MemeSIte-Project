from channels.generic.websocket import AsyncWebsocketConsumer

from datetime import datetime
from channels.generic.http import AsyncHttpConsumer
from channels.db import database_sync_to_async

from json import dumps as jdumps, loads as jloads

from .models import Post, Rating, PostListened

from asgiref.sync import sync_to_async, async_to_sync
from channels.db import database_sync_to_async

from django.template.loader import render_to_string

from django.core import serializers

class PostUpdateConsumer(AsyncWebsocketConsumer):

	async def connect(self):
		await self.accept()

	async def disconnect(self, close_code):
		if self.scope['user'].is_authenticated:
			await self.delete_disconnect_user_postlistened(self.scope['user'])


	async def receive(self, text_data):
		text_data = jloads(text_data)
		_type = text_data['type']
		if _type == 'post_notif_request' and self.scope['user'].is_authenticated:
			post_unique_name = await self.get_post_unique_name(text_data['pid'])
			await self.listen_to_post(self.scope['user'], post_unique_name)
			await self.channel_layer.group_add(post_unique_name, self.channel_name)
		else:
			await self.close()

	async def post_deletion_broadcast(self, text_data):
		await self.send(jdumps(text_data))

	async def post_rate_update_broadcast(self, text_data):
		await self.send(jdumps(text_data))

	async def post_comment_update_broadcast(self, text_data):
		deserialize_comment = await sync_to_async(serializers.deserialize)('json', text_data['serialize_comment'])
		comment_obj = list(deserialize_comment)[0].object
		text_data['comment_html'] = await sync_to_async(render_to_string)('main/comment.html', context={'comment': comment_obj, 'user':self.scope['user']})
		await self.send(jdumps(text_data))

	async def post_comment_delete_broadcast(self, text_data):
		await self.send(jdumps(text_data))		

	@database_sync_to_async
	def get_post_unique_name(self, pid):
		try:
			return Post.objects.get(pk=pid).get_unique_name()
		except Post.DoesNotExist:
			return None

	@database_sync_to_async
	def delete_disconnect_user_postlistened(self, user):
		post_listened_list = user.postlistened_set.all()
		for post_listened in post_listened_list:
			async_to_sync(self.channel_layer.group_discard)(
				post_listened.post_name,
				self.channel_name
			)
		post_listened_list.delete()

	@database_sync_to_async
	def listen_to_post(self, user, post_name):
		if not PostListened.objects.filter(user=user, post_name=post_name).exists():
			PostListened(user=user, post_name=post_name).save()