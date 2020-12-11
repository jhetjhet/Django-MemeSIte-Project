from django import forms
from .models import Post, PostContent , Image, Comment

from utils.custom_validators import is_valid_image
from django.core.validators import validate_image_file_extension


class PostForm(forms.Form):
	text_field = forms.CharField(widget=forms.Textarea, label="")
	image_field = forms.FileField(label="Add image", widget=forms.FileInput(attrs={
			'multiple': 'multiple',
			'accept': 'image/png,image/gif,image/jpeg'
		}))

	def __init__(self, *args, **kwargs):
		try:
			self.user = kwargs.pop('user')
		except KeyError:
			self.user = None
		super(PostForm, self).__init__(*args, **kwargs)

	def clean(self):
		cleaned_data = self.cleaned_data
		text_field = cleaned_data.get('text_field')
		self.images = self.files.getlist('image_field')
		self.errors.clear()

		if not self.user:
			raise forms.ValidationError('User is required')

		if text_field or len(self.images) > 0:
			for image in self.images:
				validate_image_file_extension(image)
				if not is_valid_image(image):
					self.add_error('image_field', 'image cant open or corrupted')
					break
		else:
			raise forms.ValidationError('Fill atleast one field')
		return cleaned_data

	def save(self):
		instance = Post(user=self.user)
		instance.save()
		postcontent = PostContent(post=instance)
		text_field = self.cleaned_data.get('text_field')
		if text_field:
			postcontent.text_content = text_field
		postcontent.save()
		for image in self.images:
			postcontent.image_set.create(image=image)
		return instance

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = [
			'text_comment'
		]