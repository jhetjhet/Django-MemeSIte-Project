from .forms import PostForm

def add_auth_forms(request):
	return {
		'post_form': PostForm()
	}