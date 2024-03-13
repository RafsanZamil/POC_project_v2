from django.urls import path
from feed.views import FollowAPIVIEW, UnfollowAPIVIEW, FeedAPIVIEW, LikeAPIVIEW, UnlikeAPIVIEW, ReactAPIVIEW

urlpatterns = [
    path("follow/<int:pk>/", FollowAPIVIEW.as_view(), name="follow_user"),
    path("unfollow/<int:pk>/", UnfollowAPIVIEW.as_view(), name="unfollow_user"),
    path("feed/", FeedAPIVIEW.as_view(), name="feed_view"),
    path("like/<int:pk>/", LikeAPIVIEW.as_view(), name="like_post"),
    path("unlike/<int:pk>/", UnlikeAPIVIEW.as_view(), name="unlike_post"),
    path("react/<int:pk>/", ReactAPIVIEW.as_view(), name="react_comment"),
]






