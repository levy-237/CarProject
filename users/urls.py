from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserCreateView
from .views import UserDetailView, UserListView,UserMeView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('me/', UserMeView.as_view(), name='user-me'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('', UserListView.as_view(), name='user-list'),
]