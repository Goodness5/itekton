from django.urls import path
from .views import FleetListView, FleetDetailView, VerifyOTPView, SendOTPView


urlpatterns = [
    path('fleets/', FleetListView.as_view(), name='fleet-list'),
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('fleets/<int:pk>/', FleetDetailView.as_view(), name='fleet-detail'),
]
