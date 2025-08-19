from django.contrib import admin
from .models import Participant

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'parish', 'archdeaconry', 'role', 'created_at']
    list_filter = ['parish', 'archdeaconry', 'role', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'parish']
