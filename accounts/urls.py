# urls.py
from django.urls import path, include
from .views import SignupView, SigninView, AdditionalInfoView, UserDetailView, UserListView, CompletePasswordResetView, ResetPasswordView

urlpatterns = [
    
    path('signup/', SignupView.as_view(), name='signup'),
    path('complete_signup/<int:pk>/', AdditionalInfoView.as_view(), name='additional-info'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('password_reset/', ResetPasswordView.as_view(), name='initiate-reset-password'),
    path('complete-reset-password/', CompletePasswordResetView.as_view(), name='complete-reset-password'),
    
]
