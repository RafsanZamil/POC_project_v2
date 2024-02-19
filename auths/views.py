import random
import redis
from django.core.mail import EmailMessage, get_connection
import secrets
from rest_framework.response import Response
from rest_framework.views import APIView
from POC_project_v2 import settings
from .models import CustomUser
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer
from rest_framework import status, permissions


redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)



class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(APIView):

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            with get_connection(

                    host=settings.EMAIL_HOST,
                    port=settings.EMAIL_PORT,
                    username=settings.EMAIL_HOST_USER,
                    password=settings.EMAIL_HOST_PASSWORD,
                    use_tls=settings.EMAIL_USE_TLS
            ) as connection:
                subject = "verification"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.data.get("email"), ]
                otp = int(random.randint(1000, 9999))
                print(otp)
                message = "your otp key is:  {}".format(otp)
                email = request.data.get("email")
                print(email)
                redis_client.set(email, otp, 36000)

                EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()
            return Response({'Message': "User Created Successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTP(APIView):
    def post(self, request, Format=None):
        emails = request.data.get("email")
        try:
            stored_otp = redis_client.get(emails)
            if not stored_otp:
                return Response({"message": "Invalid email or otp"}, status=401)
            else:
                stored_otp = redis_client.get(emails)
                stored_otp = int(stored_otp.decode("utf-8"))

                submitted_otp = request.data.get("otp")
                if submitted_otp:
                    submitted_otp = int(submitted_otp)

                    if stored_otp == submitted_otp:
                        user = (CustomUser.objects.filter(email=emails).values("id"))
                        user.update(is_active=True)
                        redis_client.delete(emails)
                        print(user)

                        return Response({'message': 'OTP verified successfully.'}, status=status.HTTP_200_OK)
                    else:

                        # OTP is invalid
                        return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Invalid email or otp"}, status=401)

class Logout(APIView):
    permission_classes = IsAuthenticated

    def post(self, request, format=None):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
