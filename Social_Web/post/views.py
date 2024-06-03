from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .forms import PostForm

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
