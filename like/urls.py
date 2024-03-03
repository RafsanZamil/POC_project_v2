from django.urls import path

from like.views import LikeAPIVIEW, UnlikeAPIVIEW

urlpatterns = [
    path("like/<int:pk>/", LikeAPIVIEW.as_view(), name="Like Post"),
    path("unlike/<int:pk>/", UnlikeAPIVIEW.as_view(), name="Unlike Post"),

]
