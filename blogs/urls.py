# posts/urls.py
from django.urls import path

from blogs.views import PostDetail, PostCreate, PostList

urlpatterns = [
    path("blog/<int:pk>", PostDetail.as_view(), name="post_detail"),
    path("blog/create", PostCreate.as_view(), name="create_post"),
    path("blog/", PostList.as_view(), name="view_post"),

]