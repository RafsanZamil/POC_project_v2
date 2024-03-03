from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from auths.models import CustomUser
from blog_comments.models import Comment
from blog_comments.serializers import CommentSerializer
from blogs.models import Post
from blogs.serializers import PostSerializer
from feed.models import FollowUser
from feed.serializers import FollowSerializer, PostCommentSerializer
from django.forms.models import model_to_dict

from blogs.models import Post
from blog_comments.models import Comment


# Create your views here


class FollowAPIVIEW(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        request_data = dict(request.data)
        request_data["followed_by"] = request.user.id
        user = pk
        request_data["user_id"] = user
        print(request_data)
        try:
            user_exists = CustomUser.objects.get(pk=user)
            follower = request_data.get("followed_by")

            follow = FollowUser.objects.filter(user_id=user_exists.id)
            follow = follow.filter(followed_by=follower)
            if follow.count() > 0:

                return Response({"message": "already followed the user"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = FollowSerializer(data=request_data)
                if serializer.is_valid():
                    print("true")
                    serializer.save()
                    return Response({'message': 'You followed someone ',
                                     'result': {'items': serializer.data, }}, status=status.HTTP_201_CREATED)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "The person does not exist."}, status=status.HTTP_404_NOT_FOUND)


class UnfollowAPIVIEW(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        request_data = dict(request.data)
        request_data["followed_by"] = request.user.id
        user = pk
        request_data["user_id"] = user
        try:
            user_exists = CustomUser.objects.get(pk=user)
            follower = request_data.get("followed_by")

            follow = FollowUser.objects.filter(user_id=user_exists.id)
            follow = follow.filter(followed_by=follower)
            print(follow)
            if follow.count() > 0:
                follow.delete()
                return Response({"message": "You unfollowed this person."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "You didn't follow this person."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "The person does not exist."}, status=status.HTTP_404_NOT_FOUND)


class FeedAPIVIEW(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def get(self, request):

        user = request.user.id
        my_list = []
        following = FollowUser.objects.filter(followed_by=user)
        for i in following:
            my_dict = model_to_dict(i)
            my_list.append(my_dict)
        following_list = [i['user_id'] for i in my_list]
        if following_list:

            all_posts = Post.objects.filter(author__id__in=following_list,is_active=True)
            serializer = PostCommentSerializer(all_posts, many=True)

            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"Message": "Follow someone to see their posts"}, status=status.HTTP_200_OK)
