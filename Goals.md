# Remind-me-later API (Django)

## Simplified Problem Statement

Create a Django API endpoint that allows a JavaScript frontend to submit and save reminder information. This information includes:

- Date and time for the reminder
- Message to be sent
- Method of sending (e.g., SMS, Email)

The API should store this data in a database. (Sending the reminder is out of scope.)

---

## Goal

Design and implement a Django API endpoint to accept and store reminder data.

---

## Key Data Points to Handle

- Date of reminder  
- Time of reminder  
- Reminder message (text)  
- Reminder method (e.g., SMS, Email)  

---

## Development Tasks

- [ ] **1. Setup Python Virtual Environment**  
  - Isolate project dependencies  
  - `python -m venv venv`  
  - Activate with:
    - Windows: `.\venv\Scripts\activate`
    - macOS/Linux: `source venv/bin/activate`

- [ ] **2. Install Django and Django REST Framework**  
  - `pip install django djangorestframework psycopg2-binary`

- [ ] **3. Create Django Project**  
  - `django-admin startproject reminder_project .`

- [ ] **4. Create Django App for Reminders**  
  - `python manage.py startapp reminders`

- [ ] **5. Configure Project Settings**  
  - Add to `INSTALLED_APPS`:
    ```python
    'rest_framework',
    'reminders',
    ```

- [ ] **6. Define the Reminder Model**  
  - In `reminders/models.py`:
    ```python
    from django.db import models

    class Reminder(models.Model):
        REMINDER_METHOD_CHOICES = [
            ('EMAIL', 'Email'),
            ('SMS', 'SMS'),
        ]
        reminder_datetime = models.DateTimeField()
        message = models.TextField()
        reminder_method = models.CharField(max_length=10, choices=REMINDER_METHOD_CHOICES, default='EMAIL')
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return f"Reminder for {self.reminder_datetime.strftime('%Y-%m-%d %H:%M')} via {self.reminder_method}"
    ```

- [ ] **7. Create Database Migrations**  
  - `python manage.py makemigrations reminders`  
  - `python manage.py migrate`

- [ ] **8. Create a Serializer**  
  - In `reminders/serializers.py`:
    ```python
    from rest_framework import serializers
    from .models import Reminder
    import datetime

    class ReminderSerializer(serializers.ModelSerializer):
        date = serializers.DateField(write_only=True, input_formats=["%Y-%m-%d", "iso-8601"])
        time = serializers.TimeField(write_only=True, input_formats=["%H:%M", "%H:%M:%S", "iso-8601"])

        class Meta:
            model = Reminder
            fields = ['id', 'date', 'time', 'reminder_datetime', 'message', 'reminder_method', 'created_at', 'updated_at']
            read_only_fields = ['id', 'created_at', 'updated_at', 'reminder_datetime']

        def validate(self, data):
            input_date = data.get('date')
            input_time = data.get('time')

            if not input_date or not input_time:
                raise serializers.ValidationError("Both date and time are required.")

            combined_datetime = datetime.datetime.combine(input_date, input_time)

            if combined_datetime <= datetime.datetime.now():
                raise serializers.ValidationError("Reminder date and time must be in the future.")

            data['reminder_datetime'] = combined_datetime
            return data

        def create(self, validated_data):
            validated_data.pop('date', None)
            validated_data.pop('time', None)
            return super().create(validated_data)
    ```

- [ ] **9. Create API View**  
  - In `reminders/views.py`:
    ```python
    from rest_framework import generics
    from .models import Reminder
    from .serializers import ReminderSerializer

    class ReminderListCreateAPIView(generics.ListCreateAPIView):
        queryset = Reminder.objects.all().order_by('-reminder_datetime')
        serializer_class = ReminderSerializer
    ```

- [ ] **10. Define URL for the API Endpoint**  
  - In `reminders/urls.py`:
    ```python
    from django.urls import path
    from .views import ReminderListCreateAPIView

    urlpatterns = [
        path('reminders/', ReminderListCreateAPIView.as_view(), name='reminder-list-create'),
    ]
    ```

  - In `reminder_project/urls.py`:
    ```python
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/', include('reminders.urls')),
    ]
    ```

- [ ] **11. (Optional) Add Model to Admin Panel**  
  - In `reminders/admin.py`:
    ```python
    from django.contrib import admin
    from .models import Reminder

    @admin.register(Reminder)
    class ReminderAdmin(admin.ModelAdmin):
        list_display = ('reminder_datetime', 'message', 'reminder_method', 'created_at')
        list_filter = ('reminder_method', 'reminder_datetime')
        search_fields = ('message',)
    ```

- [ ] **12. Test the API Endpoint**  
  - Run server: `python manage.py runserver`  
  - POST to: `http://127.0.0.1:8000/api/reminders/`  
  - Example request body:
    ```json
    {
        "date": "2025-12-31",
        "time": "23:59",
        "message": "Happy New Year!",
        "reminder_method": "EMAIL"
    }
    ```
  - Validate:
    - Missing fields
    - Invalid formats
    - Past datetime
    - Invalid reminder method

- [ ] **13. Initialize Git Repository and .gitignore**  
  - `git init`  
  - `.gitignore` content:
    ```
    __pycache__/
    *.py[cod]
    venv/
    env/
    .venv/
    *.log
    db.sqlite3
    media/
    .vscode/
    .idea/
    .DS_Store
    ```

- [ ] **14. Commit Code to Git**  
  - `git add .`  
  - `git commit -m "Initial setup of Django project and reminder API"`

- [ ] **15. Create GitHub Repo and Push Code**  
  - Create repo on GitHub  
  - Link and push:
    ```bash
    git remote add origin <your-github-url.git>
    git branch -M main
    git push -u origin main
    ```

- [ ] **16. Create a README.md**  
  - Include:
    - Project title
    - Description
    - Prerequisites
    - Setup instructions
    - API usage with sample request/response
  - Commit and push

---

This detailed checklist will guide you through building and deploying the Django API for the "Remind-me-later" project.
