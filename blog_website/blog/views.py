from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from .models import Post


def post_list(request) -> HttpResponse:
    posts = Post.published.all() # type: ignore
    return render(request, "blog/post.list.html", {"posts": posts})
