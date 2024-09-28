from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import Like, Post

# Create your views here.


@login_required
def upload(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'upload.html', context={'form':form})


@login_required
def like(request, pk):
    post = Post.objects.get(pk=pk)
    like = Like.objects.create(liker=request.user, post=post)

    return HttpResponseRedirect(reverse('home'))

@login_required
def unlike(request, pk):
    post = Post.objects.get(pk=pk)
    unlike = Like.objects.filter(liker=request.user, post=post)
    print(unlike)

    unlike.delete()

    return HttpResponseRedirect(reverse('home'))