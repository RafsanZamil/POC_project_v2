import json
import redis
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from rest_framework.reverse import reverse
from POC_project_v2 import settings
from blog_comments.models import Comment
from blog_comments.serializers import CommentCacheSerializer
from blogs.models import Post
from blogs.serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
import csv
import logging
redis_post = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1)
redis_comment = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=2)


logger = logging.getLogger(__name__)
logger_console = logging.getLogger('console_logger')


def export_to_csv(request):
    posts = Post.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="posts.csv"'
    writer = csv.writer(response)
    writer.writerow(['title', 'body', 'author', 'created_at', 'updated_at', 'is_active'])
    post_fields = posts.values_list('title', 'body', 'author', 'created_at', 'updated_at', 'is_active')
    for post in post_fields:
        writer.writerow(post)
    return response


class CSVUploadAPIView(APIView):
    def post(self, request):
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        if not csv_file.name.endswith('.csv'):
            return Response({'error': 'Uploaded file is not a CSV'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            created = 0
            skipped = 0
            next(reader)
            for row in reader:
                existing_post = Post.objects.filter(title=row['title']).first()
                if existing_post:
                    skipped += 1
                    continue
                serializer = PostSerializer(data=row)
                if serializer.is_valid():
                    serializer.save()
                    created += 1
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                'message': 'CSV data uploaded successfully',
                'created': created,
                'skipped': skipped
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostCreateAPIVIEW(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            request_data = dict(request.data)
            request_data["author"] = request.user.id

            post_serializer = PostSerializer(data=request_data)
            if post_serializer.is_valid():
                post_serializer.save()
                logger.info('Blog post created by user %s', request.user.username)
                return Response({'message': 'Blog post created ',
                                 'result': {'items': post_serializer.data, }}, status=status.HTTP_201_CREATED)

            logger.error('Failed to create blog post: %s', post_serializer.errors)
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception('An unexpected error occurred: %s', str(e))
            return Response({'message': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostListAPIVIEW(APIView):

    def get(self, request):
        posts = Post.objects.all().filter(is_active=True)
        paginator = Paginator(posts, 5)
        page = request.GET.get('page', 1)
        result = paginator.get_page(page)
        print(result)
        if int(page) >= 2 and not request.user.is_authenticated:
            return Response({'message': 'You need to login to see more posts'}, status=status.HTTP_401_UNAUTHORIZED)

        post_serializer = PostSerializer(result, many=True)

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

        post_serializer = PostSerializer(posts, many=True)

        return Response({'message': 'success',
                         'result': {'items': post_serializer.data, }}, status=status.HTTP_200_OK)


class PostDetailAPIVIEW(APIView):

    def get(self, request, pk):
        post_data = redis_post.get(pk)
        comment_data = redis_comment.get(pk)

        if post_data is None:
            try:
                posts = Post.objects.get(pk=pk, is_active=True)

                post_serializer = PostSerializer(posts)
                dict_str_post = json.dumps(post_serializer.data)
                redis_post.set(pk, dict_str_post, 2000)

                comments = Comment.objects.filter(post=pk)
                comment_serializer = CommentCacheSerializer(comments, many=True)
                dict_str_comment = json.dumps(comment_serializer.data)
                redis_comment.set(pk, dict_str_comment, 2000)
                return Response({'message': 'success',
                                 'result': {'posts': post_serializer.data, 'comments': comment_serializer.data}},
                                status=status.HTTP_200_OK,
                                )
            except Post.DoesNotExist:
                logger_console.warning('Post with pk=%s does not exist', pk)
                return Response({'message': 'Post does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        if comment_data is None:
            comments = Comment.objects.filter(post=pk)
            comment_serializer = CommentCacheSerializer(comments, many=True)
            dict_str_comment = json.dumps(comment_serializer.data)
            redis_comment.set(pk, dict_str_comment, 2000)
            logger_console.warning('No comment data found for post with pk=%s', pk)

        comment_data = redis_comment.get(pk)
        comment_data = json.loads(comment_data)
        post_data = json.loads(post_data)
        logger_console.warning('Post data for post with pk=%s', pk)
        return Response({'message': 'success', 'result': {'posts': post_data, 'comments': comment_data}},
                        status=status.HTTP_200_OK)

    def put(self, request, pk, ):
        try:
            post = Post.objects.get(pk=pk, is_active=True)
            if self.request.user.id == post.author_id:
                request_data = dict(request.data)
                request_data["author"] = request.user.id
                post_serializer = PostSerializer(post, data=request.data, partial=True)
                if post_serializer.is_valid():
                    post_serializer.save()
                    post_data = redis_post.get(pk)
                    if post_data is not None:
                        redis_post.delete(pk)

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
                post_data = redis_post.get(pk)
                if post_data is not None:
                    redis_post.delete(pk)
                    redis_comment.delete(pk)

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
            comment = posts.comments.all().order_by('-id')
            comments = comment.values('content')

            return Response({'message': 'success',
                             'result': {'items': post_serializer.data, "comment": comments, }},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': "Post does not exist",
                             }, status=status.HTTP_400_BAD_REQUEST)


