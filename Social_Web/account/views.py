from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.db.models import Q

from .forms import NewUserForm, LoginForm, EditProfileForm
from .models import UserProfile, SocialUser, Follow
from post.models import Post,Like
from post.forms import PostForm

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
    followed = Follow.objects.filter(follower=request.user)
    posts = Post.objects.filter(Q(user__in = followed.values_list('following')) | Q(user = request.user)).order_by('-post_created')
    likes = Like.objects.filter(liker=request.user)
    liked = likes.values_list('post', flat=True)
    return render(request, 'home.html', context={'posts':posts, 'likes':liked})

@login_required
def user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        user_posts = Post.objects.filter(user=request.user).order_by('-post_created')
        
        
    except:
        user_profile = None
    
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form = PostForm()
    return render(request, 'profile.html', context={'user_profile':user_profile, 'user_posts':user_posts, 'form':form})

@login_required
def search_user(request):
    if request.method == 'GET':
        data = request.GET.get('search')
        results = SocialUser.objects.filter(username__icontains = data)

    return render(request, 'home.html', context={'results':results})

@login_required
def other_profile(request,username):
    other_user = SocialUser.objects.get(username=username)
    user_posts = Post.objects.filter(user=other_user).order_by('-post_created')
    followed = Follow.objects.filter(follower=request.user, following=other_user)

    if other_user == request.user:
        return HttpResponseRedirect(reverse('account:profile'))

    return render(request, 'other_profile.html', context={'other_user': other_user, 'user_posts':user_posts, 'followed':followed} )


@login_required
def follow_user(request, username):
    other_user = SocialUser.objects.get(username=username)
    followed = Follow.objects.filter(follower=request.user, following=other_user)
    if not followed :
        follow = Follow(follower=request.user, following=other_user)
        follow.save()


    return HttpResponseRedirect(reverse('account:other_profile', kwargs={'username': username}))

@login_required
def unfollow_user(request, username):
    other_user = SocialUser.objects.get(username=username)
    followed = Follow.objects.filter(follower=request.user, following=other_user)
    if followed:
        followed.delete()
    return HttpResponseRedirect(reverse('account:other_profile', kwargs={'username': username}))


@login_required
def edit_profile(request):
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user = request.user)

    form = EditProfileForm(instance=user_profile)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES,instance=user_profile)
        if form.is_valid():
            form.save(commit=True)
            
            
            return HttpResponseRedirect(reverse('account:profile'))
    return render(request, 'upload.html', context={'form':form})
