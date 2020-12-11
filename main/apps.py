from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
    	from .signals import (
    		on_image_pre_delete,
    		broadcast_post_deletion,
    		broadcast_update_post_rate_create_update,
    		broadcast_update_post_rate_remove,
    		broadcast_update_post_comment_created
    	)