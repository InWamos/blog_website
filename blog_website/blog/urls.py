from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    # post views
    path(route="", view=views.postListView.as_view(), name="post_list"),
    path(
        route="<int:year>/<int:month>/<int:day>/<slug:post_slug>",
        view=views.post_detail,
        name="post_detail",
    ),
    path("<int:post_id>/share/", views.post_share, name="post_share"),
]
