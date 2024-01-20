from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post
from blog.forms import CommentForm
# Create your views here.
def index(request):
    posts = Post.objects.filter(published_at__lte=timezone.now())
    return render(request, "blog/index.html", {"posts": posts})



def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    '''
    First, we check if the user is active. 
    Users who are inactive or aren’t logged in (anonymous users) 
    will fail this test and default to having the comment_form variable set to None.
    '''
    if request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                # perform a redirect back to the current Post
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None

    return render(request, 
          "blog/post-detail.html", 
          {"post": post, 'comment_form': comment_form})




