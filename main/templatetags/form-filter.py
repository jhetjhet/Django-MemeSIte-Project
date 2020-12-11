from django import template

from django.utils.safestring import SafeString
from django.forms.boundfield import BoundField

from main.models import Rating

register = template.Library()

@register.simple_tag(name='attrs')
def attributes(value, *args, **kwargs):
	return value.as_widget(attrs=kwargs)

@register.simple_tag(name='formater')
def formater(value, **kwargs):
	return value%kwargs

@register.filter(name='doLike')
def userDoLike(user, post):
	return post.user_liked(user)

@register.filter(name='doDisLike')
def userDoDisLike(user, post):
	return post.user_disliked(user)

@register.filter(name='doFollow')
def userDoFollow(user, target_user):
	return target_user.do_follow(user)