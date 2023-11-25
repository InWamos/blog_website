from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Post


def post_list(request: HttpRequest) -> HttpResponse:
    posts = Post.published.all()
    return render(
        request=request, template_name="blog/post/list.html", context={"posts": posts}
    )


def post_detail(
    request: HttpRequest, day: int, month: int, year: int, post_slug: str
) -> HttpResponse:
    post = get_object_or_404(
        klass=Post,
        status=Post.Status.PUBLISHED,
        publish__day=day,
        publish__month=month,
        publish__year=year,
        slug=post_slug,
    )

    return render(
        request=request, template_name="blog/post/detail.html", context={"post": post}
    )
