from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import filters

from rest_framework.reverse import reverse
from blogs.models import Post
from blogs.serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions


class PostCreateAPIVIEW(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request_data = dict(request.data)
        request_data["author"] = request.user.id
        post_serializer = PostSerializer(data=request_data)
        if post_serializer.is_valid():
            post_serializer.save()

            return Response({'message': 'Blog post created ',
                             'result': {'items': post_serializer.data, }}, status=status.HTTP_201_CREATED)

        return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListAPIVIEW(APIView):
    # # pagination_class = PageNumberPagination
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['body', 'title']

    def get(self, request):
        posts = Post.objects.all().filter(is_active=True)
        paginator = Paginator(posts, 5)
        page = request.GET.get('page', 1)
        result = paginator.get_page(page)

        if int(page) >= 2 and not request.user.is_authenticated:
            return Response({'message': 'You need to login to see more posts'}, status=status.HTTP_401_UNAUTHORIZED)

        post_serializer = PostSerializer(result, many=True, context={'request': request})

        current_page_number = result.number
        if current_page_number != 1:

            previous_page_url = None
            if result.has_previous():
                previous_page_url = reverse('view_post') + f'?page={result.previous_page_number()}'

            next_page_url = None
            if result.has_next():
                next_page_url = reverse('view_post') + f'?page={result.next_page_number()}'

            return Response({'message': 'success',
                             'result': {'items': post_serializer.data, 'previous': previous_page_url,
                                        'next': next_page_url}}, status=status.HTTP_200_OK)

        else:
            previous_page_url = None
            count = int(Post.objects.all().count())
            if count <= 5:
                next_page_url = None

                return Response({'message': 'success', 'error': False,
                                 'result': {'items': post_serializer.data, 'previous': previous_page_url,
                                            'next': next_page_url}}, status=status.HTTP_200_OK)
            next_page_url = reverse('view_post') + f'?page={result.next_page_number()}'
            return Response({'message': 'success',
                             'result': {'items': post_serializer.data, 'previous': previous_page_url,
                                        'next': next_page_url}}, status=status.HTTP_200_OK)


class SearchAPIVIEW(APIView):

    def get(self, request):
        filter_by = request.query_params.get('search')
        if filter_by:
            posts = Post.objects.filter(
                Q(title__icontains=filter_by) | Q(body__icontains=filter_by)).filter(is_active=True)
        else:
            posts = Post.objects.filter(is_active=True)

        post_serializer = PostSerializer(posts, many=True, context={'request': request})

        return Response({'message': 'success',
                         'result': {'items': post_serializer.data, }}, status=status.HTTP_200_OK)


class PostDetailAPIVIEW(APIView):

    def get(self, request, pk):
        try:
            posts = Post.objects.get(pk=pk, is_active=True)
            comments = posts.comment_set.all()
            comments = comments.values('name', 'body')
            post_serializer = PostSerializer(posts)
            return Response({'message': 'success', 'result': {'items': post_serializer.data, 'comments': comments}},
                            status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'message': 'Post does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, ):
        try:
            post = Post.objects.get(pk=pk, is_active=True)

            if self.request.user.id == post.author_id:
                request_data = dict(request.data)
                request_data["author"] = request.user.id
                post_serializer = PostSerializer(post, data=request.data, partial=True)
                if post_serializer.is_valid():
                    post_serializer.save()
                    return Response({'message': 'successfully updated',
                                     'result': {'items': post_serializer.data, }}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': post_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "You do not have permission to update"}, status=status.HTTP_401_UNAUTHORIZED)

        except Post.DoesNotExist:
            return Response({"message": "Post does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        post = Post.objects.filter(pk=pk, is_active=True)
        if post:
            if self.request.user == post[0].author:
                post[0].is_active = False
                post[0].save()

                return Response({'message': 'Successfully Deleted',
                                 }, status=status.HTTP_204_NO_CONTENT
                                )

            return Response({"message": "You do not have permission to delete"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message": 'Post does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class ViewCommentsAPIVIEW(APIView):

    def get(self, request, pk):

        try:

            posts = Post.objects.get(id=pk, )
            post_serializer = PostSerializer(posts)
            comment = posts.comment_set.all().order_by('-id')
            comments = comment.values('name', 'body')

            return Response({'message': 'success',
                             'result': {'items': post_serializer.data, "comment": comments, }},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': "Post does not exist",
                             }, status=status.HTTP_400_BAD_REQUEST)
