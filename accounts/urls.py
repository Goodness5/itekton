# urls.py
from django.urls import path
from .views import SignupView, SigninView, AdditionalInfoView, UserDetailView, UserListView

urlpatterns = [
    
    path('signup/', SignupView.as_view(), name='signup'),
    path('complete_signup/<int:pk>/', AdditionalInfoView.as_view(), name='additional-info'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/', UserListView.as_view(), name='user-list'),
]
