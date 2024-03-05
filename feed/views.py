from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from auths.models import CustomUser
from blog_comments.models import Comment
from feed.models import FollowUser, Like, ReactComment
from feed.serializers import FollowSerializer, PostCommentSerializer, LikeSerializer, ReactSerializer
from blogs.models import Post


class FollowAPIVIEW(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        request_data = dict()
        request_data["followed_by"] = request.user.id
        user_id = pk
        request_data["user_id"] = user_id
        try:
            user_exists = CustomUser.objects.get(pk=user_id)
            follower_id = request_data.get("followed_by")
            followed_by = FollowUser.objects.filter(user_id=user_exists.id, followed_by=follower_id)
            if followed_by:
                return Response({"message": "You already followed the user"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = FollowSerializer(data=request_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'message': 'You followed someone ',
                                     'result': {'items': serializer.data, }}, status=status.HTTP_201_CREATED)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_404_NOT_FOUND)


class UnfollowAPIVIEW(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        request_data = dict()
        request_data["followed_by"] = request.user.id
        user_id = pk
        request_data["user_id"] = user_id
        try:
            user_exists = CustomUser.objects.get(pk=user_id)
            follower_id = request_data.get("followed_by")
            followed_by = FollowUser.objects.filter(user_id=user_exists.id, followed_by=follower_id)
            if followed_by:
                followed_by.delete()
                return Response({"message": "You unfollowed this person."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "You didn't follow this person."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_404_NOT_FOUND)


class FeedAPIVIEW(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user.id
        following_list = list(FollowUser.objects.filter(followed_by=user).values_list('user_id', flat=True))
        if following_list:
            all_posts = Post.objects.filter(author__id__in=following_list, is_active=True).order_by('-created_at')
            serializer = PostCommentSerializer(all_posts, many=True, partial=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"Message": "Follow someone to see their posts"}, status=status.HTTP_200_OK)


class LikeAPIVIEW(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        request_data = dict()
        request_data["liked_by"] = request.user.id
        post_id = pk
        request_data["post"] = post_id
        author = Post.objects.filter(pk=post_id).values("author_id")
        if author:
            author_id = author[0].get("author_id")
            follower_id = request.user.id
            following_list = list(FollowUser.objects.filter(followed_by=follower_id).values_list("user_id", flat=True))

            if author_id in following_list:
                post_exists = Post.objects.get(pk=post_id)
                liked_by = request_data.get("liked_by")
                liked = Like.objects.filter(post_id=post_exists.id, liked_by=liked_by)
                if liked:
                    return Response({"message": "You already liked the post"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer = LikeSerializer(data=request_data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'message': 'You liked the post ',
                                         'result': {'items': serializer.data, }}, status=status.HTTP_201_CREATED)

                    return Response({serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({"message": "Follow the author to like his posts"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "This Post not exists"}, status=status.HTTP_400_BAD_REQUEST)


class UnlikeAPIVIEW(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        request_data = dict()
        request_data["liked_by"] = int(request.user.id)
        post_id = pk
        request_data["post"] = int(post_id)
        try:
            post_exists = Post.objects.get(pk=post_id)
            liked_by = request_data.get("liked_by")
            liked = Like.objects.filter(post_id=post_exists.id, liked_by=liked_by)
            if liked:
                liked.delete()
                return Response({"message": "You unlike this post"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "You didn't liked this post"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"{e}."}, status=status.HTTP_404_NOT_FOUND)


class ReactAPIVIEW(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        request_data = dict(request.data)
        my_list = ["H", "C", "L", "S"]

        comment_id = pk
        request_data["comment"] = int(comment_id)
        request_data["reacted_by"] = int(request.user.id)
        post_id = Comment.objects.filter(id=comment_id)
        if post_id:
            post_id = post_id[0].post_id
            post_author = Post.objects.filter(id=post_id)[0].author_id            # post_author = author[0].author_id
            following_list = list(
                FollowUser.objects.filter(followed_by=request.user.id).values_list("user_id", flat=True))

            if post_author in following_list:
                react_exists = ReactComment.objects.filter(comment=comment_id, reacted_by=request.user.id)
                if react_exists:
                    return Response({"message": "You already reacted this comment"},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    if str(request_data["reaction"]) in my_list:
                        serializer = ReactSerializer(data=request_data)
                        if serializer.is_valid():
                            serializer.save()

                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                    return Response({"message": "Give Reaction field value between - H,C,S,L "},
                                    status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Follow the author to react on the comment "},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "No post found"}, status=status.HTTP_404_NOT_FOUND)
