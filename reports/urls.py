from django.urls import path
from .views import TransitReportView

urlpatterns = [
    path('transit-reports/<int:vehicle_id>/', TransitReportView.as_view(), name='transit-report-retrieve-update-delete'),
]

