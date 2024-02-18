
# Create your views here.
from django.http import Http404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from blog_comments.models import Comment
from blog_comments.serializers import CommentSerializer


class CreateComment(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):

        request_data = dict(request.data)
        request_data["comment_author"] = request.user.id

        serializer = CommentSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()

            try:
                return Response({'message': 'comment created ', 'error': False, 'code': 201,
                                 'result': {'items': serializer.data, }}, status=status.HTTP_201_CREATED)
            except Exception as e:

                return Response({'message': 'fail', 'error': True, 'code': 500,
                                 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# update and delete comments

class CommentDetail(APIView):
    model = Comment
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):

        try:
            return (Comment.objects.get(pk=pk))

        except Comment.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):

        snippet = self.get_object(pk, )
        # print(snippet)
        # print(self.request.user.id, " ",type(self.request.user.id))
        # print(snippet.comment_author_id, " ", type(snippet.comment_author_id))
        if self.request.user.id == snippet.comment_author_id:
            if snippet:

                serializer = CommentSerializer(snippet, data=request.data)
                print("is valid: ", serializer.is_valid())
                if serializer.is_valid():
                    serializer.save()

                    try:
                        return Response({'message': 'successfully updated', 'error': False, 'code': 200,
                                         'result': {'items': serializer.data, }}, status=status.HTTP_200_OK)
                    except Exception as e:
                        return Response({'message': 'fail', 'error': True, 'code': 400,
                                         })
        return Response({"message": "You do not have permission to update"})

    def delete(self, request, pk, format=None, ):

        snippet = self.get_object(pk)
        if self.request.user.id == snippet.comment_author_id:
            if snippet:
                snippet.delete()

                try:
                    return Response({'message': 'successfully deleted', 'code': 204,
                                     }, status=status.HTTP_204_NO_CONTENT
                                    )
                except Exception as e:
                    return Response({'message': 'failed', 'error': True, 'code': 500,
                                     })
            return Response({"message": 'No post found', 'error': False, })
            # return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "You do not have permission to delete"})
