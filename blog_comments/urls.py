from django.urls import path
from blog_comments.views import CreateComment, CommentDetail

urlpatterns = [

    path('comment', CreateComment.as_view(), name='create comment'),
    path('comment/<int:pk>', CommentDetail.as_view(), name='comment detail')
]


