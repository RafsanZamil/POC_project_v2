from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from blog_comments.models import Comment
from blog_comments.serializers import CommentSerializer
from blogs.models import Post
from blogs.views import redis_comment


class CreateCommentAPIVIEW(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        request_data = dict(request.data)
        request_data["comment_author"] = request.user.id
        post_id = pk
        request_data["post"] = post_id
        post = Post.objects.filter(pk=post_id, is_active=True)
        if post:
            serializer = CommentSerializer(data=request_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                comment_data = redis_comment.get(pk)
                if comment_data is not None:
                    redis_comment.delete(pk)
                return Response({'message': 'comment created ',
                                 'result': {'items': serializer.data, }}, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Post does not exist."}, status=status.HTTP_404_NOT_FOUND)


class CommentDetailAPIVIEW(APIView):
    model = Comment
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):

        try:
            comment = Comment.objects.get(pk=pk)
            if self.request.user.id == comment.comment_author_id:
                serializer = CommentSerializer(comment, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    post_pk = serializer.data.get('post')
                    comment_data = redis_comment.get(post_pk)
                    if comment_data is not None:
                        redis_comment.delete(post_pk)

                    return Response({'message': 'successfully updated',
                                     'result': {'items': serializer.data, }}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'invalid', 'result': serializer.errors},
                                    status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "You do not have permission to update"}, status=status.HTTP_401_UNAUTHORIZED)
        except Comment.DoesNotExist:
            return Response({"message": 'No comment found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, ):

        comment = Comment.objects.filter(pk=pk)
        if comment:
            if self.request.user.id == comment[0].comment_author_id:
                post_pk = Comment.objects.filter(pk=pk)[0]
                post_pk = post_pk.post_id
                comment_data = redis_comment.get(post_pk)
                if comment_data is not None:
                    redis_comment.delete(post_pk)
                comment.delete()

                return Response({'message': 'successfully deleted',
                                 }, status=status.HTTP_204_NO_CONTENT
                                )

            return Response({"message": "You do not have permission to delete"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message": 'No comment found', }, status=status.HTTP_404_NOT_FOUND)
