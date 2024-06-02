from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password

from .forms import NewUserForm, LoginForm
from .models import UserProfile, SocialUser
from post.models import Post

# Create your views here.

def authenticate(username=None, password=None):
    
    user =SocialUser.objects.filter(username=username).first()
    if user is None:
        user = SocialUser.objects.filter(roll=username).first()
    if user is not None:
        if check_password(password,user.password):
            return user
    return None
    

def signup(request):
    form = NewUserForm()
    if request.method == 'POST':
        form = NewUserForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user_profile = UserProfile.objects.create(user=user)
            return HttpResponseRedirect(reverse('account:login'))
    return render(request, 'signup.html', context={'form':form})


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            return render(request, 'login.html', context={'form':form, 'error':"Enter correct information"})
    return render(request, 'login.html', context={'form':form})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('account:login'))


@login_required
def home(request):
    try:
        user_profile = SocialUser.objects.get(user=request.user)
    except:
        user_profile = None

    return render(request, 'home.html', context={'user_profile':user_profile})

@login_required
def user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        user_posts = Post.objects.filter(user=request.user).order_by('-post_created')
        
        
    except:
        user_profile = None
    return render(request, 'profile.html', context={'user_profile':user_profile, 'user_posts':user_posts})