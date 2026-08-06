from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ActivateTokenView, RefreshCookieView, PasswordResetView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateTokenView.as_view(), name='activate_token'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    # path('password_confirm/<uidb64>/<token>/', LogoutView.as_view(), name='logout'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', RefreshCookieView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),


]
