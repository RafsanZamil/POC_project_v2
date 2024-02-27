from django.http import Http404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from blog_comments.models import Comment
from blog_comments.serializers import CommentSerializer
from blogs.models import Post


class CreateComment(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request_data = dict(request.data)
        request_data["comment_author"] = request.user.id
        post_id = request_data.get("post")
        post = Post.objects.filter(pk=post_id, is_active=True)
        if post:
            serializer = CommentSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'comment created ',
                                 'result': {'items': serializer.data, }}, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Post does not exist."}, status=status.HTTP_404_NOT_FOUND)


class CommentDetail(APIView):
    model = Comment
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):

        try:
            comment = Comment.objects.get(pk=pk)
            return comment

        except Comment.DoesNotExist:
            raise Http404

    def put(self, request, pk):

        comment = self.get_object(pk, )
        if self.request.user.id == comment.comment_author_id:
            if comment:

                serializer = CommentSerializer(comment, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()

                    return Response({'message': 'successfully updated',
                                     'result': {'items': serializer.data, }}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'invalid', 'result': serializer.errors},
                                    status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": 'No comment found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "You do not have permission to update"}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk, ):

        comment = self.get_object(pk)
        if self.request.user.id == comment.comment_author_id:
            if comment:
                comment.delete()

                return Response({'message': 'successfully deleted',
                                 }, status=status.HTTP_204_NO_CONTENT
                                )

            return Response({"message": 'No comment found', }, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "You do not have permission to delete"}, status=status.HTTP_401_UNAUTHORIZED)
