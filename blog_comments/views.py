from django.http import Http404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from blog_comments.models import Comment
from blog_comments.serializers import CommentSerializer


class CreateComment(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request_data = dict(request.data)
        request_data["comment_author"] = request.user.id

        serializer = CommentSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'comment created ',
                             'result': {'items': serializer.data, }}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

                serializer = CommentSerializer(comment, data=request.data)
                if serializer.is_valid():
                    serializer.save()

                    return Response({'message': 'successfully updated',
                                     'result': {'items': serializer.data, }}, status=status.HTTP_200_OK)
                return Response({'message': 'serializing failed'})
            return Response({"message": 'No comment found', 'error': False, })

        return Response({"message": "You do not have permission to update"})

    def delete(self, request, pk, ):

        comment = self.get_object(pk)
        if self.request.user.id == comment.comment_author_id:
            if comment:
                comment.delete()

                return Response({'message': 'successfully deleted',
                                 }, status=status.HTTP_204_NO_CONTENT
                                )

            return Response({"message": 'No comment found', 'error': False, })

        return Response({"message": "You do not have permission to delete"})
