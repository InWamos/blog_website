from calendar import c
import re
from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, CreateView

from .models import Post, PublishedManager
from .forms import EmailPostForm, CommentForm
 
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 5
    template_name = "blog/post/list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["view_type"] = "post_list"
        return context


class TagListView(ListView):
    context_object_name = "posts"
    paginate_by = 5
    template_name = "blog/post/list.html"

    def get_queryset(self) -> PublishedManager:
        tag_slug = self.kwargs.get("tag_slug")
        return Post.published.filter(tags__slug__in=[tag_slug])
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["view_type"] = "tag_list"
        context["tag_name"] = self.kwargs.get("tag_slug")
        return context
    
class PostCommentView(CreateView):
    form_class = CommentForm
    template_name = "blog/post/comment.html"

    def post(self, request: HttpRequest, post_id: int):
        
        self.post_id = post_id
        post = get_object_or_404(
            Post, id=self.post_id, status=Post.Status.PUBLISHED
        )
        form = CommentForm(data=request.POST)
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

        return redirect(post.get_absolute_url())

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            form.send_email(subject, message, "your_account@gmail.com", [cd["to"]])
            sent = True
    else:
        form = EmailPostForm()

    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )


# Obsolete view
def post_list(request: HttpRequest) -> HttpResponse:
    post_list = Post.published.all()

    paginator = Paginator(post_list, 5)
    page_number = request.GET.get("page", 1)

    try:
        posts = paginator.page(page_number)
    except (EmptyPage, PageNotAnInteger):
        posts = paginator.page(paginator.num_pages)

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
    comments = post.comments.filter(active=True) # type: ignore

    return render(
        request=request,
        template_name="blog/post/detail.html",
        context={"post": post, "form": CommentForm(), "comments": comments},
    )
