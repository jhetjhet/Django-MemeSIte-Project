from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	date_posted = models.DateTimeField(default=timezone.now)

	def like_count(self):
		return self.rating_set.filter(name=Rating.LIKE).count()

	def dislike_count(self):
		return self.rating_set.filter(name=Rating.DISLIKE).count()

	def user_liked(self, user):
		try:
			rating = self.rating_set.get(user=user)
			return rating.name == Rating.LIKE
		except (Rating.DoesNotExist, Rating.MultipleObjectsReturned):
			return False

	def user_disliked(self, user):
		try:
			rating = self.rating_set.get(user=user)
			return rating.name == Rating.DISLIKE
		except (Rating.DoesNotExist, Rating.MultipleObjectsReturned):
			return False

	def make_rate(self, user, rate_name):
		if not rate_name in Rating.RATE_TYPES:
			raise ValueError('rate name not in default rate types')
		try:
			rating = user.rating_set.get(post_id=self.id)
			if rating.name == rate_name:
				rating.delete()
				return None
			rating.name = rate_name
			rating.save()
			return rating
		except Rating.DoesNotExist:
			return user.rating_set.create(post_id=self.id, name=rate_name)

	def get_unique_name(self):
		return f"{self.user.username}_post_{self.id}"

	def __str__(self):
		return f"{self.user.username} Post"

class Rating(models.Model):
	LIKE = 'like'
	DISLIKE = 'dislike'
	RATE_TYPES = [LIKE, DISLIKE]

	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
	name = models.CharField(max_length=32, null=True, blank=True)

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
	text_comment = models.TextField()
	date_commented = models.DateTimeField(default=timezone.now)

	def get_dic(self):
		return {
			'user':{
				'url': reverse('user:profile', kwargs={'id':self.user.id}),
				'id': self.user.id,
				'username': self.user.username,
				'picture_url': self.user.profile.picture.url,
			},
			'comment':{
				'id': self.pk,
				'date_commented': self.date_commented.strftime('%a. %b. %m %Y, %I %M %p'),
				'text_comment': self.text_comment,
			}
		}

class PostContent(models.Model):
	post = models.OneToOneField(Post, on_delete=models.CASCADE, primary_key=True)
	text_content = models.TextField(blank=True, null=True)

class Image(models.Model):
	post_content = models.ForeignKey(PostContent, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='PostContent/images/')

class PostListened(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	post_name = models.CharField(max_length=200)