from django.shortcuts import render
from django.urls import path,include
from .views import *
from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('users/', include((router.urls, 'app_name'))),
    
    # path('CustomUserListView/',CustomUserListView.as_view()),
    path('UserRegistrationView/',UserRegistrationView.as_view()),
    path('check_username/', CheckUsernameView.as_view(), name='check_username'),
    path('change-faculty-role/<int:user_id>/', UpdateFacultyRoleView.as_view(), name='update-Faculty-role'),
    path('VerifyOTPView/',VerifyOTPView.as_view()),
    path('verify-ResendOTPView/',VerifyResendOTPView.as_view()),
    path('Otp-ForgotPassword/',ResendOtpForgotPassword.as_view()),
     path('Newpassword-changing/',ChangeNewPassword.as_view()),
     path('admin-dashboard/',FetchAllDetailsDashboard.as_view()),

    path('token/', jwt_views.TokenObtainPairView.as_view(),  name ='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(),  name ='token_refresh'),

    path('logout/', LogoutView.as_view(), name='logout'),
    path('get-user-role/', GetUserRoleView.as_view(), name='get-user-role'),
    path('resend-otp/', ResendOtp.as_view(), name='resend-otp'),
    path('switch-role/', SwitchRoleView.as_view(), name='switch-role'),
    path('profile-details/<int:user_id>/', GetProfileView.as_view(), name='profile-details'),
    path('set-profile-image/<int:user_id>/', ProfileImage.as_view(), name='set-picture'),
    
    path('check-otp-verified/', Check_Otp.as_view(), name='check-confirmation'),
  
   
]
