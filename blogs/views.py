from django.db.models import Q

from rest_framework import filters

from rest_framework.pagination import PageNumberPagination

from blog_comments.serializers import CommentSerializer
from blogs.models import Post
from blogs.serializers import PostSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions


# Create Posts
class PostCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        request_data = dict(request.data)
        request_data["author"] = request.user.id
        serializer = PostSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()

            try:
                return Response({'message': 'Blog post created ', 'error': False, 'code': 201,
                                 'result': {'items': serializer.data, }}, status=status.HTTP_201_CREATED)
            except Exception as e:

                return Response({'message': 'fail', 'error': True, 'code': 500,
                                 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View all posts


class PostList(APIView):
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['body', 'title']

    def get(self, request, format=None):
        posts = Post.objects.all()

        # filter_by = request.query_params.get('search')
        # posts = Post.objects.filter(
        #     Q(
        #         Q(title__icontains=filter_by) |
        #         Q(body__icontains=filter_by)
        #     )
        # )

        paginator = PageNumberPagination()

        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True, context={'request': request})
        try:
            return Response({'message': 'sucess', 'error': False, 'code': 200,
                             'result': {'items': serializer.data, }}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'fail', 'error': True, 'code': 500,
                             })
# Search
class Search(APIView):
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['body', 'title']

    def get(self, request, format=None):

        filter_by = request.query_params.get('search')
        posts = Post.objects.filter(
            Q(
                Q(title__icontains=filter_by) |
                Q(body__icontains=filter_by)
            )
        )

        paginator = PageNumberPagination()

        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True, context={'request': request})
        try:
            return Response({'message': 'sucess', 'error': False, 'code': 200,
                             'result': {'items': serializer.data, }}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'fail', 'error': True, 'code': 500,
                             })

# view post details, update and delete posts
class PostDetail(APIView):
    model = Post
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):

        try:
            return (Post.objects.get(pk=pk))

        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):

        posts = self.get_object(pk)
        serializer = PostSerializer(posts)
        try:
            return Response({'message': 'sucess', 'error': False, 'code': 200,
                             'result': {'items': serializer.data, }}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'fail', 'error': True, 'code': 500,
                             })

    def put(self, request, pk, format=None):

        snippet = self.get_object(pk, )
        if self.request.user == snippet.author:
            if snippet:
                serializer = PostSerializer(snippet, data=request.data)
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

        post = self.get_object(pk)
        if self.request.user == post.author:
            if post:
                post.delete()

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


class ViewComments(APIView):
    model = Post
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):

        try:
            return (Post.objects.get(pk=pk))

        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):

        #posts = self.get_object(pk)
        posts = Post.objects.get(id=pk)
        comments = posts.comment_set.all()
        comments= comments.values('name','body').order_by('id')

        serializer = PostSerializer(posts)
        try:
            return Response({'message': 'sucess', 'error': False, 'code': 200,
                             'result': {'items': comments, }}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'fail', 'error': True, 'code': 500,
                             })