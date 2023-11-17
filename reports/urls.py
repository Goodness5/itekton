from django.urls import path
from .views import TransitReportInitialView, TransitReportUpdateView,  ReminderInitialView, ReminderUpdateView

urlpatterns = [
    path('transit-reports/<int:vehicle_id>/', TransitReportInitialView.as_view(), name='transit-report-retrieve-update-delete'),
    path('transit-reports/<int:vehicle_id>/<int:report_id>', TransitReportUpdateView.as_view(), name='transit-update-delete'),
    path('reminders/<int:vehicle_id>/', ReminderInitialView.as_view(), name='reminder-retrieve-update-delete'),
    path('reminders/<int:vehicle_id>/<int:reminder_id>/', ReminderUpdateView.as_view(), name='reminder-update-delete'),

    # path('alerts/<int:vehicle_id>/', AlertInitialView.as_view(), name='alert-retrieve-update-delete'),
    # path('alerts/<int:vehicle_id>/<int:alert_id>/', AlertUpdateView.as_view(), name='alert-update-delete'),

    # path('critical-faults/<int:vehicle_id>/', CriticalFaultInitialView.as_view(), name='critical-fault-retrieve-update-delete'),
    # path('critical-faults/<int:vehicle_id>/<int:critical_fault_id>/', CriticalFaultUpdateView.as_view(), name='critical-fault-update-delete'),

    # path('tests/<int:vehicle_id>/', TestInitialView.as_view(), name='test-retrieve-update-delete'),
    # path('tests/<int:vehicle_id>/<int:test_id>/', TestUpdateView.as_view(), name='test-update-delete'),

    # path('registrations/<int:vehicle_id>/', RegistrationInitialView.as_view(), name='registration-retrieve-update-delete'),
    # path('registrations/<int:vehicle_id>/<int:registration_id>/', RegistrationUpdateView.as_view(), name='registration-update-delete'),
]   
