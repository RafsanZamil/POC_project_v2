from django.urls import path
from blogs.views import PostDetailAPIVIEW, PostCreateAPIVIEW, PostListAPIVIEW, ViewCommentsAPIVIEW, SearchAPIVIEW

urlpatterns = [
    path("blog/<int:pk>/", PostDetailAPIVIEW.as_view(), name="post_detail"),
    path("blog/create/", PostCreateAPIVIEW.as_view(), name="create_post"),
    path("blog/", PostListAPIVIEW.as_view(), name="view_post"),
    path("blog/view/", SearchAPIVIEW.as_view(), name="search"),
    path("blog/<int:pk>/comment/", ViewCommentsAPIVIEW.as_view(), name="view_comments")

]

