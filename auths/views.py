import random
import redis
from django.core.mail import EmailMessage, get_connection
from rest_framework.response import Response
from rest_framework.views import APIView
from POC_project_v2 import settings
from .models import CustomUser
from .serializers import MyTokenObtainPairSerializer, ForgotPasswordSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer
from rest_framework import status

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterAPIVIEW(APIView):

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


class VerifyOTPAPIVIEW(APIView):
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

                        return Response({'message': 'OTP verified successfully.'}, status=status.HTTP_200_OK)
                    else:

                        return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Invalid email or otp"}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        stored_otp = redis_client.get(email)
        if stored_otp:
            redis_client.delete(email)
        if CustomUser.objects.filter(email=email).exists():
            with get_connection(

                    host=settings.EMAIL_HOST,
                    port=settings.EMAIL_PORT,
                    username=settings.EMAIL_HOST_USER,
                    password=settings.EMAIL_HOST_PASSWORD,
                    use_tls=settings.EMAIL_USE_TLS
            ) as connection:
                subject = "reset password"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]

                otp = int(random.randint(1000, 9999))
                message = "your otp key for reset password is:  {}".format(otp)
                redis_client.set(email, otp, 36000)

                EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()
                return Response({'Message': "OTP sent Successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Email not found"}, status=status.HTTP_204_NO_CONTENT)


class ChangePasswordAPIView(APIView):
    def post(self, request):
        emails = request.data.get("email")
        stored_otp = redis_client.get(emails)

        if not stored_otp:

            return Response({"message": "Invalid email or otp"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            stored_otp = redis_client.get(emails)
            stored_otp = int(stored_otp.decode("utf-8"))
            submitted_otp = request.data.get("OTP")
            try:
                submitted_otp = int(submitted_otp)

                if stored_otp == submitted_otp:
                    serializer = ForgotPasswordSerializer(data=request.data)
                    if serializer.is_valid():
                        user = request.user
                        if user.check_password(serializer.data.get('old_password')):
                            user.set_password(serializer.data.get('new_password'))
                            user.save()
                            redis_client.delete(emails)
                            return Response({'message': 'Password Changed'}, status=status.HTTP_200_OK)
                        return Response({'message': 'Wrong Password'}, status=status.HTTP_400_BAD_REQUEST)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'OTP Mismatched.'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message': "Enter valid otp"}, status=status.HTTP_400_BAD_REQUEST)
