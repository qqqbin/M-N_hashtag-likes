import json
from django.http import HttpRequest
from django.http.response import HttpResponse
from .forms import PostForm, CommentForm, HashtagForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Hashtag
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.

def base(request):
    return render(request, 'blog/base.html')

def main(request):
    posts = Post.objects
    hashtags = Hashtag.MultipleObjectsReturned
    return render(request, 'blog/main.html', {'posts': posts, 'hashtags':hashtags})

def wirte(request):
    return render(request, 'blog/wirte.html')

def create(request, post=None):
    if request.method == 'POST' :
        form = PostForm(request.POST, request.FILES, instance=post )
        if form.is_valid():
            post = form.save(commit=False)
            post.pub_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('read')
    else:
        form = PostForm
        return render(request, 'blog/write.html', {'form':form})    

def read(request):
    posts = Post.objects
    hashtags = Hashtag.objects
    return render(request, 'blog/read.html', {'posts': posts, 'hashtags':hashtags})

def detail(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = post
            comment.text = form.cleaned_data['text']
            comment.save()
            return redirect('detail', id)
    else : 
        form = CommentForm()
        return render(request, 'blog/detail.html', {'post':post, 'form':form})

def edit(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            return redirect('read')
    
    else :
        form = PostForm(instance=post)
        return render(request, 'blog/edit.html', {'form':form})

def delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('read')

def hashtagform(request, hashtag=None):
    if request.method == 'POST':
        form = HashtagForm(request.POST, instance=hashtag)
        if form.is_valid():
            hashtag = form.save(commit=False)
            if Hashtag.objects.filter(name=form.cleaned_data['name']):
                form = HashtagForm()
                error_message = "이미 존재하는 해시태그 입니다"
                return render(request,'blog/hashtag.html', {'form':form, "error_message":error_message})
            else:
                hashtag.name = form.cleaned_data['name']
                hashtag.save()
            return redirect('read')
    else:
        form = HashtagForm(instance=hashtag)
        return render(request, 'blog/hashtag.html', {'form':form})

def search(request, hashtag_id):
    hashtag = get_object_or_404(Hashtag, id=hashtag_id)
    return render(request, 'blog/search.html', {'hashtag':hashtag})

@login_required
@require_POST
def post_like(request):
    pk = request.POST.get('pk', None)
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    if post.likes_user.filter(id=user.id).exists():
        post.likes_user.remove(user)
        message = '좋아요 취소'
    else : 
        post.like_user.add(user)
        message = '좋아요'
    
    context = {'likes_count':post.count_likes_user(), 'message': message}
    return HttpResponse(json.dumps(context), context_type="application/json")