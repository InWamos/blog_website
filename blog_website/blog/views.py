from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Post


def post_list(request: HttpRequest) -> HttpResponse:
    posts = Post.published.all()
    return render(
        request=request, template_name="blog/post/list.html", context={"posts": posts}
    )


def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)

    return render(
        request=request, template_name="blog/post/detail.html", context={"post": post}
    )
