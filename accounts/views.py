from django.shortcuts import render
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from allauth.account.views import LoginView, SignupView, LogoutView
from allauth.account.forms import LoginForm, SignupForm

from news.models import Author

# Create your views here.

class Signup(SignupView):
    template_name = 'accounts/signup.html'
    form_class = SignupForm


class Login(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

class Logout(LogoutView):
    template_name = 'accounts/logout.html'

@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
        Author.objects.create(user = user)
    return redirect('/')

