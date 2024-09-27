from django import forms
from .models import Application, Movie, CustomUser
from django.contrib.auth.forms import UserCreationForm

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['name', 'description', 'age_start', 'age_end', 'gender', 'number_of_people', 'location', 'image', 'last_registration_date']  # Include the new field

    # Optionally, use a date input widget for the 'last_registration_date'
    last_registration_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=True,
    )
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['name', 'email', 'phone', 'age', 'gender', 'photo', 'video']  # Include the video field

class CustomUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'full_name', 'phone_number', 'email', 'profile_image', 'date_of_birth', 'password1', 'password2')

class CustomUserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'date_of_birth', 'profile_image']