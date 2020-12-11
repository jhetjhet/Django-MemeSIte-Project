from channels.generic.websocket import AsyncWebsocketConsumer

from json import dumps as jdumps, loads as jloads

from channels.db import database_sync_to_async

class UserUpdatesConsumer(AsyncWebsocketConsumer):

	async def connect(self):
		if self.scope['user'].is_authenticated:
			self.following_username_list = await self.get_user_followings_username_list()
			for username in self.following_username_list:
				await self.channel_layer.group_add(username, self.channel_name)
			await self.accept()
		else:
			await self.close()

	async def disconnect(self, close_code):
		for username in self.following_username_list:
			await self.channel_layer.group_discard(username, self.channel_name)

	async def receive(self, text_data):
		pass


	async def user_follow_updates_broadcast(self, text_data):
		await self.send(jdumps(text_data))

	@database_sync_to_async
	def get_user_followings_username_list(self):
		return [ follow_info.following.username for follow_info in self.scope['user'].followings.all() ]