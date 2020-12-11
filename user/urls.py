from django.urls import path, reverse_lazy

from .views import (
	login_view,
	make_follow,
	create_account_view,
	edit_profile_view,
	profile,
	change_password_view,
	search_user,
	top_users,
)
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView

app_name = 'user'

urlpatterns = [
	path('<int:pk>/profile', profile, name='profile'),
	path('<int:pk>/follow-unfollow', make_follow, name='follow'),
	path('create/', create_account_view, name='create'),
	path('login/', login_view, name='login'),
	path('change-passowrd/', change_password_view, name='change_pass'),

	path('logout/', LogoutView.as_view(next_page="main:home"), name='logout'),
	path('edit/', edit_profile_view, name='edit'),
	path('search/', search_user, name='search'),
	path('tops/', top_users, name='tops'),
]