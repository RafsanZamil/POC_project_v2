from django.forms import model_to_dict
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from blogs.models import Post
from feed.models import FollowUser
from like.models import Like
from like.serializers import LikeSerializer


# Create your views here.

class LikeAPIVIEW(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        request_data = dict(request.data)
        request_data["liked_by"] = int(request.user.id)
        post = pk
        request_data["post"] = int(post)

        author = Post.objects.filter(pk=post).values("author_id")
        author = author[0].get("author_id")
        print("author:",author)
        user = request.user.id
        print("user:",user)

        my_list = []
        following = FollowUser.objects.filter(followed_by=user)
        for i in following:
            my_dict = model_to_dict(i)
            my_list.append(my_dict)
        following_list = [i['user_id'] for i in my_list]

        if author in following_list:

            try:
                post_exists = Post.objects.get(pk=post)
                liker = request_data.get("liked_by")
                like = Like.objects.filter(post_id=post_exists.id)
                like = like.filter(liked_by=liker)
                print(like)
                if like.count() > 0:

                    return Response({"message": "already liked the post"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer = LikeSerializer(data=request_data)

                    if serializer.is_valid():
                        serializer.save()
                        return Response({'message': 'You liked the post ',
                                         'result': {'items': serializer.data, }}, status=status.HTTP_201_CREATED)

            except Exception as e:
                print(e)
                return Response({"message": "Post not exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Follow the author to like his posts"}, status=status.HTTP_400_BAD_REQUEST)


class UnlikeAPIVIEW(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        request_data = dict(request.data)
        request_data["liked_by"] = int(request.user.id)
        post = pk
        request_data["post"] = int(post)
        try:
            post_exists = Post.objects.get(pk=post)
            liker = request_data.get("liked_by")
            like = Like.objects.filter(post_id=post_exists.id)
            like = like.filter(liked_by=liker)

            if like.count() > 0:
                like.delete()
                return Response({"message": "You unlike this post"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "You didn't liked this post"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": "The person does not exist."}, status=status.HTTP_404_NOT_FOUND)
