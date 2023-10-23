# urls.py
from django.urls import path
from .views import SignupView, SigninView, AdditionalInfoView

urlpatterns = [
    
    path('signup/', SignupView.as_view(), name='signup'),
      path('complete_signup/<int:pk>/', AdditionalInfoView.as_view(), name='additional-info'),
    path('signin/', SigninView.as_view(), name='signin'),
]
