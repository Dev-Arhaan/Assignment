from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Reminder
from .serializers import ReminderSerializer

class ReminderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Reminder.objects.all().order_by('-reminder_datetime')
    serializer_class = ReminderSerializer