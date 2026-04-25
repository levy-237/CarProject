from django.urls import path
from .views import UserCreateView
from .views import UserDetailView, UserListView,UserMeView

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='user-create'),
    path('detail/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('', UserListView.as_view(), name='user-list'),
    path('me/', UserMeView.as_view(), name='user-me'),
]