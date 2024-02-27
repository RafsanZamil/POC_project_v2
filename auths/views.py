import random
import redis
from django.core.mail import EmailMessage, get_connection
from rest_framework.response import Response
from rest_framework.views import APIView
from POC_project_v2 import settings
from .models import CustomUser
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer
from rest_framework import status

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(APIView):

    def post(self, request):
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
                message = "your otp key is:  {}".format(otp)
                email = request.data.get("email")
                redis_client.set(email, otp, 36000)

                EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()
            return Response({'Message': "User Created Successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTP(APIView):
    def post(self, request):
        emails = request.data.get("email")
        try:
            stored_otp = redis_client.get(emails)
            if not stored_otp:
                return Response({"message": "Invalid email or otp"}, status=status.HTTP_400_BAD_REQUEST)
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

                        return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Invalid email or otp"}, status=status.HTTP_400_BAD_REQUEST)



