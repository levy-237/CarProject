from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserDetailView, UserCreateView, UserListView, UserCompanyListView, UserMeView, AddSavedSearch, SavedSearchDetailUpdateDelete, SendEmailVerficationCode,VerifyUser, SendPasswordRecoveryEmail, RecoverPassword, ChangePassword

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('me/', UserMeView.as_view(), name='user-me'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('companies/', UserCompanyListView.as_view(), name='user-company-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('', UserListView.as_view(), name='user-list'),
    path('send-user-verification/', SendEmailVerficationCode.as_view(), name='send-user-verification'),
    path('user-verification/', VerifyUser.as_view(), name='user-verification'),
    path('send-user-password-recovery/', SendPasswordRecoveryEmail.as_view(), name='send-user-password-recovery'),
    path('user-password-recovery/', RecoverPassword.as_view(), name='user-password-recovery'),
    path('change-password/', ChangePassword.as_view(), name='change-password'),
    path('savedsearch/', AddSavedSearch.as_view(), name='saved_search-add'),
    path('savedsearch/<int:pk>/', SavedSearchDetailUpdateDelete.as_view(), name='saved_search-detail'),
]