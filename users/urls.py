from django.urls import path
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentListAPIView, UserListAPIView, UserRetrieveAPIView, UserCreateAPIView, UserUpdateAPIView, \
    UserDestroyAPIView, SubscriptionAPIView, PaymentCreateAPIView

app_name = UsersConfig.name


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path("", UserListAPIView.as_view(), name="users_list"),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="users_retrieve"),
    path("<int:pk>/create/", UserCreateAPIView.as_view(), name="users_create"),
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="users_update"),
    path("<int:pk>/delete/", UserDestroyAPIView.as_view(), name="users_delete"),
    path("payments/", PaymentListAPIView.as_view(), name="payments_list"),
    path("payments/create/", PaymentCreateAPIView.as_view(), name="payment_create"),
    path("subscriptions/create/", SubscriptionAPIView.as_view(), name="subscriptions_create")
]
