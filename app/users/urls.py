from django.urls import path
from .views import (
    SendOTPView,
    SignupView,
    UpdatePasswordView,
    RequestOldEmailView,
    RequestNewEmailOTPView,
    VerifyNewEmailView,
    LoginAPIView,
    LogoutView,
    AddModerateur
)

urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('update-password/', UpdatePasswordView.as_view(), name='update_password'),
    path('request-old-email/', RequestOldEmailView.as_view(), name='request_old_email'),
    path('request-new-email/', RequestNewEmailOTPView.as_view(), name='request_new_email'),
    path('add-moderateur/', AddModerateur.as_view(), name='add_moderateur'),
    path('verify-new-email/', VerifyNewEmailView.as_view(), name='verify_new_email'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]


