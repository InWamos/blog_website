from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render

# Create your views here.
from .models import Post


def post_list(request: HttpRequest) -> HttpResponse:
    posts = Post.published.all()
    return render(
        request=request, template_name="blog/post.list.html", context={"posts": posts}
    )


def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    try:
        post = Post.published.get(id=id)
    except Post.DoesNotExist:
        raise Http404("404 No post found.")

    return render(
        request=request, template_name="blog/post/detail.html", context={"post": post}
    )
