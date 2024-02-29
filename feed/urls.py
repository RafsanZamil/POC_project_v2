from django.urls import path
from feed.views import FollowAPIVIEW, UnfollowAPIVIEW, FeedAPIVIEW

urlpatterns = [
    path("follow/<int:pk>/", FollowAPIVIEW.as_view(), name="Follow User"),
    path("unfollow/<int:pk>/", UnfollowAPIVIEW.as_view(), name="Unfollow User"),
    path("feed/", FeedAPIVIEW.as_view(), name="feed view"),
]
