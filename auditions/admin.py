from django.contrib import admin
from .models import Movie, Application, CustomUser

class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'age_start', 'age_end', 'gender', 'number_of_people', 'location', 'last_registration_date')
    list_filter = ('gender', 'location', 'last_registration_date')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('movie', 'name', 'email', 'phone', 'age', 'gender', 'selected')
    list_filter = ('selected',)
    actions = ['approve_application', 'reject_application']

    def approve_application(self, request, queryset):
        queryset.update(selected=True)
        self.message_user(request, "Selected application(s) successfully.")
    
    def reject_application(self, request, queryset):
        queryset.update(selected=False)
        self.message_user(request, "Rejected application(s) successfully.")

    approve_application.short_description = "Approve selected applications"
    reject_application.short_description = "Reject selected applications"

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'email', 'date_of_birth')
    search_fields = ('username', 'full_name', 'email')
