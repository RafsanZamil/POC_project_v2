from django.urls import path
from blog_comments.views import CreateCommentAPIVIEW, CommentDetailAPIVIEW

urlpatterns = [


    path('post/<int:pk>/comment/', CreateCommentAPIVIEW.as_view(), name='create comment'),
    path('comment/<int:pk>/', CommentDetailAPIVIEW.as_view(), name='comment detail'),

]


