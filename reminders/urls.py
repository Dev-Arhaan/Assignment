from django.urls import path
from .views import ReminderListCreateAPIView

urlpatterns = [
    path('reminders/', ReminderListCreateAPIView.as_view(), name='reminder-list-create'),
]