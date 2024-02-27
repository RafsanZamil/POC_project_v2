from django.urls import path
from auths.views import MyObtainTokenPairView, RegisterAPIVIEW, VerifyOTPAPIVIEW
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterAPIVIEW.as_view(), name='auth_register'),
    path('verify/', VerifyOTPAPIVIEW.as_view(), name='')

]
