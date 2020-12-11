from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import IntegrityError


class Memer(AbstractUser):
	followers_count = models.IntegerField(default=0)

	def do_follow(self, other_memer):
		return self.followers.filter(follower=other_memer).exists()

	def follow_unfollow(self, follower):
		follow_info = FollowInfo.objects.filter(follower=follower, following=self)
		if follow_info.count() == 0:
			try:
				FollowInfo(follower=follower, following=self).save()
				return True
			except IntegrityError:
				pass
		follow_info.delete()
		return False

	def __str__(self):
		return self.username

class FollowInfo(models.Model):
	following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')
	follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followings')
	date_follow = models.DateTimeField(default=timezone.now)

	class Meta:
		unique_together = ['follower', 'following']
		ordering = ['-date_follow']

	def __str__(self):
		return f'{self.follower.username} follows {self.following.username}'


class Profile(models.Model):
	DEFAULT_PROFILE_PICTURE = 'Profile/pictures/default_profile_picture.jpg'
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
	picture = models.ImageField(default=DEFAULT_PROFILE_PICTURE, upload_to='Profile/pictures/')
	background = models.ImageField(default='Profile/background/default_background.jpg', upload_to='Profile/background/')
	about = models.TextField(blank=True, null=True)


class UserManager:
	def __init__(self, user):
		self.user = user

	def add_follower(self, user_to_add):
		if self.user == user_to_add:
			raise ValueError('user cannnot follow itself')
		followers = self.user.followers.filter(user=user_to_add)
		if followers.exists():
			followers.delete()
		else:
			self.user.followers.create(user=user_to_add)
		return self.user.followers.all()