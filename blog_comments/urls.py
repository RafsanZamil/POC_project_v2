from django.urls import path
from blog_comments.views import CreateCommentAPIVIEW, CommentDetailAPIVIEW

urlpatterns = [


    path('create/comment/<int:pk>/',  CreateCommentAPIVIEW.as_view(), name='create_comment'),
    path('update/comment/<int:pk>/', CommentDetailAPIVIEW.as_view(), name='comment_update'),
    path('delete/comment/<int:pk>/', CommentDetailAPIVIEW.as_view(), name='comment_delete'),

]


