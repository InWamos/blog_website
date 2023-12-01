from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    # post views
    path(route="", view=views.PostListView.as_view(), name="post_list"),
    path(
        route="<int:year>/<int:month>/<int:day>/<slug:post_slug>",
        view=views.PostDetailView.as_view(),
        name="post_detail",
    ),
    path(route="<int:post_id>/share/", view=views.post_share, name="post_share"),
    path(route="<int:post_id>/comment/", view=views.PostCommentView.as_view(), name="post_comment"),
    path(route="tag/<slug:tag_slug>/", view=views.TagListView.as_view(), name="post_list_by_tag"),
]
