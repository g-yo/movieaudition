from django import forms
from .models import Application, Movie, CustomUser
from django.contrib.auth.forms import UserCreationForm

from django import forms
from .models import Feedback
class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['name', 'description', 'age_start', 'age_end', 'gender', 'number_of_people', 'location_name', 'latitude', 'longitude', 'image']
        widgets = {
            'latitude': forms.HiddenInput(),  # Hidden because it will be filled by the map
            'longitude': forms.HiddenInput(),  # Hidden because it will be filled by the map
        }
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['name', 'email', 'phone', 'age', 'gender', 'photo', 'video', 'cv']  # Include the cv field

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

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_text']