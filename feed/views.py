from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from auths.models import CustomUser
from blogs.models import Post
from blogs.serializers import PostSerializer
from feed.models import FollowUser
from feed.serializers import FollowSerializer
from django.forms.models import model_to_dict


# Create your views here

class FollowAPIVIEW(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        request_data = dict(request.data)
        request_data["followed_by"] = request.user.id
        user = pk
        request_data["user_id"] = user
        user_exists = CustomUser.objects.get(pk=user)
        follower = request_data.get("followed_by")
        if user_exists:
            follow = FollowUser.objects.filter(user_id=user_exists.id)
            follow = follow.filter(followed_by=follower)
            if follow.count() > 0:

                return Response({"message": "already followed the user"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = FollowSerializer(data=request_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'message': 'You followed someone ',
                                     'result': {'items': serializer.data, }}, status=status.HTTP_201_CREATED)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "The person does not exist."}, status=status.HTTP_404_NOT_FOUND)


class UnfollowAPIVIEW(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        request_data = dict(request.data)
        request_data["followed_by"] = request.user.id
        user = pk
        request_data["user_id"] = user
        user_exists = CustomUser.objects.get(pk=user)
        follower = request_data.get("followed_by")
        if user_exists:
            follow = FollowUser.objects.filter(user_id=user_exists.id)
            follow = follow.filter(followed_by=follower)
            print(follow)
            if follow.count() > 0:
                follow.delete()
                return Response({"message": "You unfollowed this person."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "You didn't follow this person."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "The person does not exist."}, status=status.HTTP_404_NOT_FOUND)


class FeedAPIVIEW(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def get(self, request):

        global posts
        user = request.user.id
        l = []
        following = FollowUser.objects.filter(followed_by=user)
        for i in following:
            my_dict = model_to_dict(i)
            l.append(my_dict)
        following_list = [i['user_id'] for i in l]

        for i in following_list:
            posts = Post.objects.filter(author=i)

        serializer = PostSerializer(posts, many=True)

        return Response({"posts": serializer.data})
