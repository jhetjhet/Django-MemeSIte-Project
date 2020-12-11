from django.shortcuts import render, get_object_or_404

from django.views.generic import DetailView

from django.http import HttpResponse, Http404
from django.template.loader import render_to_string

from user.forms import CreateAccountForm
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.forms import AuthenticationForm

from json import dumps as jdumps, loads as jloads

from .models import Post, Rating, PostContent, Image, Comment
from .forms import PostForm, CommentForm

def home(request):
	return render(request, 'main/home.html')


def create_post(request):
	if request.method == 'POST' and request.is_ajax() and request.user.is_authenticated:
		response = {}
		postForm = PostForm(request.POST, request.FILES, user=request.user)
		if postForm.is_valid():
			instance = postForm.save()
			response['status'] = 1
			response['message'] = f"Post successfulyy created {instance.date_posted.strftime('%a. %b. %m %Y')}"
			response['post_html'] = render_to_string('main/post.html', context={'post': instance}, request=request)
			response['pid'] = instance.id
		else:
			response['status'] = 0
			response['errors'] = jloads(postForm.errors.as_json())
		return HttpResponse(jdumps(response), content_type="application/json")
	raise Http404()

def delete_post(request):
	if request.method == 'POST' and request.is_ajax() and request.user.is_authenticated:
		pid = request.POST['pid']
		post = get_object_or_404(Post, pk=pid)
		post.delete()
		return HttpResponse(jdumps({'status': 1}), content_type="application/json")
	raise Http404()

def rate_post(request):
	if request.method == 'POST' and request.is_ajax() and request.user.is_authenticated:
		pid = request.POST['pid']
		name = request.POST['name']
		if not name in Rating.RATE_TYPES:
			raise Http404()
		rating = get_object_or_404(Post, pk=pid).make_rate(request.user, name)
		return HttpResponse(jdumps({'active': rating.name if rating else None, 'selected': name}), content_type="application/json")
	else:
		raise Http404()

def request_post_comment(request):
	if request.method == 'GET' and request.is_ajax() and request.user.is_authenticated:
		pid = request.GET['pid']
		last_id = request.GET['last_id']
		include_form = request.GET['include_form']
		max_to_gen = 5
		response = {}

		if include_form:
			response['comment_form'] = render_to_string('main/comment-form.html', context={'pid': pid})

		if last_id == 'start':
			comment_list_all = get_object_or_404(Post, pk=pid).comment_set.all().order_by('-date_commented')
		else:
			comment_list_all = get_object_or_404(Post, pk=pid).comment_set.filter(id__lt=last_id).order_by('-date_commented')
		comment_list = comment_list_all[:max_to_gen]

		response['comments_html'] = "".join([render_to_string('main/comment.html', context={'comment': comment, 'user':request.user}) for comment in comment_list])
		response['last_id'] = comment_list[comment_list.count() - 1].id if comment_list.count() >= max_to_gen else 'end'
		return HttpResponse(jdumps(response), content_type="application/json")
	raise Http404()

def create_comment(request):
	if request.method == 'POST' and request.is_ajax() and request.user.is_authenticated:
		response = {}
		pid = request.POST['pid']
		content = request.POST['content']
		if content:
			comment = request.user.comment_set.create(post_id=pid, text_comment=content)
			response['status'] = 1
			response['date_commented'] = comment.date_commented.strftime('%a. %b. %m %Y, %I %M %p')
		else:
			response['status'] = 0
			response['message'] = 'Empty content'
		return HttpResponse(jdumps(response), content_type="application/json")
	raise Http404()

def delete_comment(request, pk):
	if request.method == 'POST' and request.is_ajax() and request.user.is_authenticated:
		get_object_or_404(Comment, pk=pk).delete()
		return HttpResponse(jdumps({}), content_type="application/json")
	raise Http404()

def request_post(request):
	if request.method == 'GET' and request.is_ajax():
		last_id = request.GET['last_id']
		filter_user = request.GET['filter_user']
		max_to_gen = 5

		if last_id == 'start':
			if filter_user:
				post_list_all = Post.objects.filter(user_id=filter_user)
			else:
				post_list_all = Post.objects.all().order_by('-date_posted')
		else:
			post_list_all = Post.objects.filter(id__lt=last_id).order_by('-date_posted')

		post_list = post_list_all[:max_to_gen]

		post_list_html = []
		post_list_pids = []

		for post in post_list:
			post_list_pids.append(post.id)
			post_list_html.append(
				render_to_string('main/post.html', context={'post': post}, request=request)
			)

		return HttpResponse(jdumps(
				{
					'post_list_html': post_list_html,
					'post_list_pids': post_list_pids,
					'max_lent': len(post_list_all),
					'last_id': post_list[post_list.count() - 1].id if post_list.count() >= max_to_gen else 'end'
				}
			), content_type="application/json")
	raise Http404()
