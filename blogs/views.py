from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.reverse import reverse
from blog_comments.serializers import CommentSerializer
from blogs.models import Post
from blogs.serializers import PostSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions


class PostCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        request_data = dict(request.data)
        request_data["author"] = request.user.id
        serializer = PostSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()

            try:
                return Response({'message': 'Blog post created ',
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

        p = Post.objects.all()
        paginator = Paginator(p, 5)
        page = request.GET.get('page', 1)
        result = paginator.get_page(page)

        if int(page) >= 2 and not request.user.is_authenticated:
            return Response({'You need to login to see more posts': 'fail', 'error': True, 'code': 400})

        serializer = PostSerializer(result, many=True, context={'request': request})

        current_page_number = result.number
        if current_page_number != 1:

            previous_page_url = None
            if result.has_previous():
                previous_page_url = reverse('view_post') + f'?page={result.previous_page_number()}'

            next_page_url = None
            if result.has_next():
                next_page_url = reverse('view_post') + f'?page={result.next_page_number()}'

            try:
                return Response({'message': 'success', 'error': False, 'code': 200,
                                 'result': {'items': serializer.data, 'previous': previous_page_url,
                                            'next': next_page_url}}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': 'fail', 'error': True, 'code': 500,
                                 })
        else:
            previous_page_url = None
            next_page_url = reverse('view_post') + f'?page={result.next_page_number()}'

            return Response({'items': serializer.data, 'previous': previous_page_url,
                             'next': next_page_url})


class Search(APIView):

    def get(self, request, format=None):
        filter_by = request.query_params.get('search')
        if filter_by:
            posts = Post.objects.filter(
                Q(title__icontains=filter_by) | Q(body__icontains=filter_by))
        else:
            posts = Post.objects.all()


        serializer = PostSerializer(posts, many=True, context={'request': request})
        try:
            return Response({'message': 'success',
                             'result': {'items': serializer.data, }}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'fail', 'error': True, 'code': 500,
                             })


# view post details, update and delete posts
class PostDetail(APIView):

    def get_object(self, pk):

        try:
            posts = Post.objects.get(pk=pk, is_active=True)
            return posts

        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):

        posts = self.get_object(pk)
        comments = posts.comment_set.all()
        comments = comments.values('name', 'body')
        serializer = PostSerializer(posts)
        try:
            return Response({'message': 'success',

                             'result': {'items': serializer.data, 'comments': comments}}, status=status.HTTP_200_OK)
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
                        return Response({'message': 'successfully updated',
                                         'result': {'items': serializer.data, }}, status=status.HTTP_200_OK)
                    except Exception as e:
                        return Response({'message': 'fail', 'error': True, 'code': 400,
                                         })
        return Response({"message": "You do not have permission to update"})

    def delete(self, request, pk, format=None, ):

        post = self.get_object(pk)
        print("post:", post)
        if self.request.user == post.author:
            if post:
                post.is_active = False
                post.save()

                try:
                    return Response({'message': 'successfully deleted',
                                     }, status=status.HTTP_204_NO_CONTENT
                                    )
                except Exception as e:
                    return Response({'message': 'failed', 'error': True, 'code': 500,
                                     })
            return Response({"message": 'No post found', 'error': False, })

        return Response({"message": "You do not have permission to delete"})


class ViewComments(APIView):
    pagination_class = PageNumberPagination

    def get_object(self, pk):

        try:
            post = Post.objects.get(pk=pk)
            return post

        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):

        try:

            posts = Post.objects.get(id=pk)
            serializer = PostSerializer(posts)

            p = posts.comment_set.all().order_by('-id')
            comments = p.values('name', 'body')
            paginator = Paginator(comments, 5)
            page = request.GET.get('page')
            result = paginator.get_page(page)
            serializer2 = CommentSerializer(result, many=True)

            return Response({'message': 'success',
                             'result': {'items': serializer.data, "comment": comments, }},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'post not found', 'error': True,
                             })
