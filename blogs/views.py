# from django.db.migrations import serializer
# from django.shortcuts import render, get_object_or_404
# from rest_framework import generics, viewsets, status
#
# from rest_framework.response import Response
#
#
# from blogs.models import Post
# from blogs.permissions import UserPermission
# from blogs.serializers import PostSerializer
#
#
#
#
#
# class PostViewSet(viewsets.ViewSet):
#     permission_classes = (UserPermission,)
#
#     def list(self, request):
#         queryset = Post.objects.all()
#         serializer = PostSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = Post.objects.all()
#         post = get_object_or_404(queryset, pk=pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#
#     def create(self, request, *args, **kwargs):
#         data = request.data.get(
#             "items") if 'items' in request.data else request.data
#         many = isinstance(data, list)
#         serializer =PostSerializer(data=data, many=many)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.pagination import PageNumberPagination
from blogs.models import Post
from blogs.serializers import PostSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions




#Create Posts
class PostCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View all posts

class PostList(APIView):
    pagination_class = PageNumberPagination

    def get(self, request, format=None):
        posts = Post.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True, context={'request': request})
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response


# view post details, update and delete posts
class PostDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):

        posts = self.get_object(pk)
        serializer = PostSerializer(posts)
        return Response(serializer.data)


    def put(self, request, pk, format=None):

        snippet = self.get_object(pk)
        serializer = PostSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):

        snippet = self.get_object(pk)
        snippet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


