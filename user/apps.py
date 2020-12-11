from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'

    def ready(self):
    	from .signals import (
    		add_profile_on_new_user,
    		delete_left_profile_pictures__post_save,
    		delete_left_profile_pictures__pre_delete,
    		broadcast_user_follow_updates,
    	)