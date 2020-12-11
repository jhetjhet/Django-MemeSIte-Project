from django.urls import path

#views
from .views import (
	home,
	create_post,
	delete_post,
	rate_post,
	request_post_comment,
	create_comment,
	delete_comment,
	request_post
)

app_name = 'main'

urlpatterns = [
	path('', home, name='home'),
	path('post/create/', create_post, name='post-upload'),
	path('post/delete/', delete_post, name='post-delete'),
	path("post/rate/", rate_post, name='post-rate'),
	path('post/comment/request/', request_post_comment, name='post-comment-request'),
	path('post/comment/create/', create_comment, name='post-comment'),
	path('post/comment/<int:pk>/delete/', delete_comment, name='post-comment-delete'),
	path('post/request/', request_post, name='post-request'),
]