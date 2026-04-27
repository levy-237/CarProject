from django.urls import path
from .views import UserCreateView
from .views import UserDetailView, UserListView,UserMeView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('', UserListView.as_view(), name='user-list'),
    path('me/', UserMeView.as_view(), name='user-me'),
]