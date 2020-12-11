from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse

from django.http import HttpResponse, Http404

from django.contrib.auth import authenticate, login

from django.contrib.auth.forms import AuthenticationForm
from .forms import CreateAccountForm, ProfileForm

from json import dumps as jdumps, loads as jloads

from .models import Profile, UserManager
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm

from django.db.models import Q

User = get_user_model()

def profile(request, pk):
	user = get_object_or_404(User, pk=pk)
	return render(request, 'main/profile-detail.html', {
			'target_user': user,
		})

def make_follow(request, pk):
	if request.method == 'POST' and request.user.is_authenticated and request.is_ajax():
		memer = get_object_or_404(User, pk=pk)
		do_follow = memer.follow_unfollow(request.user)
		return HttpResponse(jdumps({'do_follow':do_follow, 'new_followers_count': get_object_or_404(User, pk=pk).followers_count}), content_type='application/json')
	raise Http404()
	
def login_view(request):
	if request.method == 'POST' and request.is_ajax():
		response = {}
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user:
			response['status'] = 1
			response['redirect'] = reverse("main:home")
			login(request, user)
			return HttpResponse(jdumps(response), content_type='application/json')
		else:
			response['status'] = 0
			response['message'] = "Invalid username or password."
			return HttpResponse(jdumps(response), content_type='application/json')
	else:
		raise Http404()

def create_account_view(request):
	if request.method == 'POST' and request.is_ajax():
		create_account_form = CreateAccountForm(request.POST)
		if create_account_form.is_valid():
			create_account_form.save()
			return HttpResponse(jdumps({
					'status': 1,
					'message':'Account created successfuly',
				}), content_type='application/json')
		else:
			data = jloads(create_account_form.errors.as_json())
			data['status'] = 0
			return HttpResponse(jdumps(data), content_type='application/json')
	else:
		raise Http404()

def change_password_view(request):
	if not request.user.is_authenticated:
		return Http404()
	context = {}
	context['change_pass_form'] = PasswordChangeForm(user=request.user)
	if request.method == 'POST':
		change_pass_form = PasswordChangeForm(user=request.user, data=request.POST)
		context['change_pass_form'] = change_pass_form
		if change_pass_form.is_valid():
			user = change_pass_form.save()
			login(request, user)
			del context['change_pass_form']
			context['message'] = 'Changing password successfully'
	return render(request, 'user/change-pass.html', context)

def edit_profile_view(request):
	if request.method == 'POST' and request.user.is_authenticated and 'uid' in request.POST:
		profileForm = ProfileForm(request.POST, request.FILES, uid=request.POST['uid'])
		response = jloads(profileForm.errors.as_json())
		if profileForm.is_valid():
			profileForm.save()
			response['status'] = 1
			return HttpResponse(jdumps(response), content_type='application/json')
		response['status'] = 0
		return HttpResponse(jdumps(response), content_type='application/json')
	raise HttpResponse()

def search_user(request):
	if request.method == 'GET' and request.is_ajax():
		max_results = 5
		username = request.GET['username']
		users = User.objects.filter(username__istartswith=username)
		results = []
		for user in users[:max_results]:
			results.append({
				'username': user.username,
				'profile_picture_url': user.profile.picture.url,
				'link': reverse('user:profile', kwargs={'pk':user.id})
			})
		return HttpResponse(jdumps({'results': results, 'results_count': users.count()}), content_type='application/json')

def top_users(request):
	if request.method == 'GET' and request.is_ajax() and request.user.is_authenticated:
		max_results = 5
		top_users_obj = User.objects.filter(followers_count__gt=0).order_by('-followers_count')[:max_results]
		top_users = []
		for user in top_users_obj:
			top_users.append({
				'link': reverse('user:profile', kwargs={'pk':user.id}),
				'profile_picture_url': user.profile.picture.url,
				'username': user.username,
				'followers_count': user.followers_count,
			})
		return HttpResponse(jdumps({'top_users':top_users}), content_type='application/json')