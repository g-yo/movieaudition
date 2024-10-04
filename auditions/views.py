from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
import logging
from .models import CustomUser, Movie
from .forms import CustomUserCreationForm, MovieForm, ApplicationForm
from django.contrib import messages
logger = logging.getLogger(__name__)
from .models import Application, Movie
from django.db.models import Count
import google.generativeai as genai
from django.http import JsonResponse
from dotenv import load_dotenv
import os
from .forms import CustomUserUpdateForm 
import json
from django.db.models.functions import TruncMonth
from django.db.models import Count, F, Q
from django.utils.timezone import now
import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Feedback
from .forms import FeedbackForm

from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import CustomUserCreationForm
from .models import Movie, Application, Notification
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
# Load environment variables
load_dotenv()

from .models import Movie, Feedback

def movie_list(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # Superuser sees all movies
            movies = Movie.objects.all()
            print(f"Superuser: All Movies: {list(movies.values('name', 'age_start', 'age_end'))}")  # Debug print
        else:
            # Regular user sees movies according to their age
            user_age = request.user.age
            print(f"User Age: {user_age}")  # Debug print
            
            # Filter movies based on age range
            movies = Movie.objects.filter(age_start__lte=user_age, age_end__gte=user_age)
            print(f"Filtered Movies: {list(movies.values('name', 'age_start', 'age_end'))}")  # Debug print
    else:
        # If the user is not authenticated, show all movies
        movies = Movie.objects.all()
        print(f"All Movies: {list(movies.values('name', 'age_start', 'age_end'))}")  # Debug print
    
    # Fetch the latest three feedbacks
    feedbacks = Feedback.objects.all().order_by('-date_submitted')[:3]

    return render(request, 'auditions/movie_list.html', {'movies': movies, 'feedbacks': feedbacks})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'auditions/movie_detail.html', {'movie': movie})

@login_required
def apply_for_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        
        if form.is_valid():
            application = form.save(commit=False)
            application.movie = movie
            application.user = request.user  # Associate the application with the logged-in user
            application.save()
            
            # Prepare the email details
            subject = f"Application Submitted: {movie.name}"
            html_message = render_to_string('emails/application_submitted.html', {'movie': movie, 'user': request.user})
            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [request.user.email]

            # Send the email
            send_mail(
                subject,
                plain_message,
                from_email,
                to_email,
                fail_silently=False,
                html_message=html_message
            )

            messages.success(request, 'Successfully registered! You will be informed if the application is selected. You can check the status from the dashboard.')
            return redirect('apply_for_movie', movie_id=movie.id)
    
    else:
        form = ApplicationForm()

    return render(request, 'auditions/apply_form.html', {'form': form, 'movie': movie})

def application_success(request):
    return render(request, 'auditions/application_success.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            subject = 'Welcome to ACTRS'
            
            # Use a template for the email body (HTML)
            html_message = render_to_string('emails/welcome_email.html', {'user': user})
            plain_message = strip_tags(html_message)  # Fallback to plain text
             
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.email]

            # Send the email using EmailMultiAlternatives for both plain text and HTML content
            email = EmailMultiAlternatives(subject, plain_message, from_email, to_email)
            email.attach_alternative(html_message, "text/html")
            email.send(fail_silently=True)

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('movie_list')
        else:
            form.add_error(None, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'auditions/register.html', {'form': form})

def userlogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    logger.error(f'Admin user attempted to log in through user login: {username}')
                    messages.error(request, "Admins should use the admin login page.")
                else:
                    login(request, user)
                    return redirect('movie_list')
            else:
                logger.error(f'Invalid login attempt for username: {username}')
                form.add_error(None, "Invalid username or password.")
        else:
            logger.error(f'Form is not valid: {form.errors}')
            form.add_error(None, "Please correct the errors below.")
    else:
        form = AuthenticationForm()
    return render(request, 'auditions/login.html', {'form': form})

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user and user.is_superuser:
                login(request, user)
                return redirect('admin_overview')
            else:
                messages.error(request, "Invalid login credentials or not an admin.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = AuthenticationForm()
    return render(request, 'admin/admin_login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('movie_list')

@login_required
def user_profile(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-created_at')
    
    context = {
        'user': user,
        'notifications': notifications,
    }
    return render(request, 'auditions/user_profile.html', context)
def admin_required(function=None):
    return user_passes_test(lambda u: u.is_superuser, login_url='adminlogin')(function)

@login_required
@admin_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == "POST":
        movie.delete()
        return redirect('admin_dashboard')  # Redirect to admin dashboard after deletion
    return HttpResponse("Method not allowed", status=405)

@login_required
def user_dashboard(request):
    # Filter applications for the current logged-in user
    user_applications = Application.objects.filter(user=request.user)
    total_applications = user_applications.count()
    selected_applications = user_applications.filter(selected=True).count()

    context = {
        'total_applications': total_applications,
        'selected_applications': selected_applications,
    }
    return render(request, 'auditions/user_dashboard.html', context)
def movies_by_age(request, age):
    movies = Movie.objects.filter(age__lte=age)
    movie_data = [{'name': movie.name, 'description': movie.description} for movie in movies]
    return JsonResponse({'movies': movie_data})
@login_required
def add_movie(request):
    if not request.user.is_superuser:
        return redirect('admin_login')  # Redirect to admin login if not superuser

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Redirect to admin dashboard after saving
    else:
        form = MovieForm()

    return render(request, 'admin/add_movie.html', {'form': form})


from django.db.models import Count, F
from django.db.models.functions import TruncMonth

@login_required
@admin_required
def admin_dashboard(request):
    # Fetch all movies
    movies = Movie.objects.all()
    
    # Fetch all applications
    applications = Application.objects.all()
    application_count = applications.count()
    selected_application_count = applications.filter(selected=True).count()
    
    # Prepare data for the Applications Over Months chart
    applications_by_month = applications.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
    months_labels = [app['month'].strftime('%B %Y') for app in applications_by_month]
    applications_over_months = [app['count'] for app in applications_by_month]

    # Encode data as JSON
    context = {
        'movies': movies,  # Include movies in the context
        'application_count': application_count,
        'selected_application_count': selected_application_count,
        'months_labels': json.dumps(months_labels),
        'applications_over_months': json.dumps(applications_over_months),
    }

    return render(request, 'admin/admin_dashboard.html', context)
# @login_required
# def add_movie(request):
#     if not request.user.is_superuser:
#         return redirect('admin_login')
    
#     if request.method == 'POST':
#         form = MovieForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('admin_dashboard')  # Redirect to admin dashboard or another page
#     else:
#         form = MovieForm()
    
#     return render(request, 'admin/add_movie.html', {'form': form})


@login_required
def view_applications(request):
    if not request.user.is_superuser:
        return redirect('admin_login')

    applications = Application.objects.all()

    context = {
        'applications': applications,
    }
    return render(request, 'admin/view_applications.html', context)

@login_required
@admin_required  # Custom decorator to check if the user is an admin
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)  # Use the instance to edit
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Redirect to the admin dashboard after saving
    else:
        form = MovieForm(instance=movie)  # Populate the form with the current movie data

    return render(request, 'admin/edit_movie.html', {'form': form, 'movie': movie})

@login_required
@admin_required
def admin_overview(request):
    # Fetch basic data for the overview
    movie_count = Movie.objects.count()
    application_count = Application.objects.count()
    selected_application_count = Application.objects.filter(selected=True).count()

    # Applications Over Months (for the past year)
    applications_by_month = Application.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
    months_labels = [app['month'].strftime('%B %Y') for app in applications_by_month]
    applications_over_months = [app['count'] for app in applications_by_month]

    # Gender distribution data
    gender_data = Application.objects.values('gender').annotate(count=Count('id')).order_by('gender')
    gender_labels = [gender['gender'] for gender in gender_data]
    gender_counts = [gender['count'] for gender in gender_data]

    # Age group data
    age_groups = {
        '0-18': Application.objects.filter(age__lte=18).count(),
        '19-30': Application.objects.filter(age__gte=19, age__lte=30).count(),
        '31-45': Application.objects.filter(age__gte=31, age__lte=45).count(),
        '46+': Application.objects.filter(age__gte=46).count(),
    }
    age_group_labels = list(age_groups.keys())
    age_group_counts = list(age_groups.values())

    # Encode data as JSON to send to the frontend
    context = {
        'movie_count': movie_count,
        'application_count': application_count,
        'selected_application_count': selected_application_count,
        'months_labels': json.dumps(months_labels),
        'applications_over_months': json.dumps(applications_over_months),
        'gender_labels': json.dumps(gender_labels),
        'gender_counts': json.dumps(gender_counts),
        'age_group_labels': json.dumps(age_group_labels),
        'age_group_counts': json.dumps(age_group_counts),
    }

    return render(request, 'admin/admin_overview.html', context)

@login_required
@admin_required
def application_detail(request, application_id):
    # Retrieve the specific application using the provided ID
    application = get_object_or_404(Application, id=application_id)
    
    # Retrieve all applications
    applications = Application.objects.all()
    
    # Prepare context
    context = {
        'application': application,
        'applications': applications
    }
    
    return render(request, 'admin/application_detail.html', context)

@login_required
@admin_required
def application_details(request, application_id):
    # Retrieve the specific application using the provided ID
    application = get_object_or_404(Application, id=application_id)
    
    # Prepare context
    context = {
        'application': application
    }
    
    return render(request, 'admin/application_detail.html', context)

from .models import Notification

@login_required
@admin_required
def select_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    application.selected = True
    application.save()

    # Create a notification for the user
    Notification.objects.create(
        user=application.user,
        message=f"Your application for {application.movie.name} has been selected.",
        is_read=False
    )

    # Prepare the email details
    subject = f"Application Selected: {application.movie.name}"
    html_message = render_to_string('emails/application_selected.html', {'application': application})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [application.user.email]

    # Send the email
    send_mail(
        subject,
        plain_message,
        from_email,
        to_email,
        fail_silently=False,
        html_message=html_message
    )

    return redirect('application_details', application_id=application.id)
@login_required
@admin_required
def reject_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    application.selected = False
    application.save()

    # Create a notification for the user
    Notification.objects.create(
        user=application.user,
        message=f"Your application for {application.movie.name} has been rejected.",
        is_read=False
    )

    # Prepare the email details
    subject = f"Application Rejected: {application.movie.name}"
    html_message = render_to_string('emails/application_rejected.html', {'application': application})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [application.user.email]

    # Send the email
    send_mail(
        subject,
        plain_message,
        from_email,
        to_email,
        fail_silently=False,
        html_message=html_message
    )

    # Show a success message to the admin
    messages.success(request, 'Application rejected successfully.')

    return redirect('application_details', application_id=application.id)
@login_required
def overview(request):
    user = request.user
    print(f"User: {user}")  # Ensure this prints the correct user

    total_applications = Application.objects.filter(user=user).count()
    selected_applications = Application.objects.filter(user=user, selected=True).count()

    print(f"Total Applications: {total_applications}")
    print(f"Selected Applications: {selected_applications}")

    context = {
        'total_applications': total_applications,
        'selected_applications': selected_applications,
    }
    
    return render(request, 'auditions/overview.html', context)
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = CustomUserUpdateForm(instance=request.user)
    return render(request, 'auditions/update_profile.html', {'form': form})

@login_required
def notifications(request):
    # Fetch user notifications
    notifications = Notification.objects.filter(user=request.user, read=False)
    notification_count = notifications.count()
    return render(request, 'auditions/notifications.html', {'notifications': notifications, 'notification_count': notification_count})

from django.shortcuts import render
from .models import Notification

def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    # Mark all notifications as read once viewed
    user_notifications.update(is_read=True)

    return render(request, 'auditions/notifications.html', {'notifications': user_notifications})


import random

def get_random_color():
    colors = ["#FF5733", "#33FF57", "#3357FF", "#FF33A6", "#FFC300", "#DAF7A6", "#C70039", "#900C3F", "#581845"]
    return random.choice(colors)
@login_required
def notifications_view(request):
    # Filter notifications for the current user
    notifications = Notification.objects.filter(user=request.user)

    for notification in notifications:
        notification.background_color = get_random_color()
        notification.font_color = get_random_color()

    context = {
        'notifications': notifications
    }
    return render(request, 'audition/notifications.html', context)
@login_required
def feedback_form_view(request):
    images = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg']
    random_image = random.choice(images)
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('feedback_list')
    else:
        form = FeedbackForm()

    return render(request, 'auditions/feedback_form.html', {'form': form, 'random_image': random_image})

@login_required
def feedback_list_view(request):
    feedbacks = Feedback.objects.all().order_by('-date_submitted')
    return render(request, 'auditions/feedback_list.html', {'feedbacks': feedbacks})
def admin_report(request):
    # Get the current date
    current_date = now()
    
    # Filter applications and registrations for the current month
    start_of_month = current_date.replace(day=1)
    total_registrations = Application.objects.filter(created_at__gte=start_of_month).count()
    
    # Count male and female registrations for this month
    male_registrations = Application.objects.filter(created_at__gte=start_of_month, gender='male').count()
    female_registrations = Application.objects.filter(created_at__gte=start_of_month, gender='female').count()

    # Age distribution
    age_distribution = Application.objects.values('age').annotate(age_count=Count('age')).order_by('age')

    # Find the most common age group for registrations this month
    age_group = Application.objects.filter(created_at__gte=start_of_month) \
                .values('age') \
                .annotate(age_count=Count('age')) \
                .order_by('-age_count') \
                .first()

    # Total number of selected candidates
    selected_candidates = Application.objects.filter(created_at__gte=start_of_month, selected=True).count()

    # Get all user registrations and applications for the table display
    users = CustomUser.objects.all()
    applications = Application.objects.all()

    # Prepare data for the charts
    # Applications Over Months
    months_labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    applications_over_months = [
        Application.objects.filter(created_at__month=i).count() for i in range(1, 13)
    ]
    
    # Gender Chart Data
    gender_labels = ['Male', 'Female']
    gender_counts = [male_registrations, female_registrations]

    # Age Group Chart Data
    age_group_labels = [entry['age'] for entry in age_distribution]
    age_group_counts = [entry['age_count'] for entry in age_distribution]

    context = {
        'total_registrations': total_registrations,
        'male_registrations': male_registrations,
        'female_registrations': female_registrations,
        'age_group': age_group['age'] if age_group else None,
        'selected_candidates': selected_candidates,
        'users': users,
        'age_distribution': age_distribution,
        'applications': applications,

        # Chart Data
        'months_labels': months_labels,
        'applications_over_months': applications_over_months,
        'gender_labels': gender_labels,
        'gender_counts': gender_counts,
        'age_group_labels': age_group_labels,
        'age_group_counts': age_group_counts,
    }

    return render(request, 'admin/admin_report.html', context)
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils import timezone
# from xhtml2pdf import pisa
from .models import Application, CustomUser

def admin_report_pdf(request):
    pass
    # Fetch the context data
    # users = CustomUser.objects.all()
    # applications = Application.objects.all()
    
    # context = {
    #     'now': timezone.now(),
    #     'total_registrations': users.count(),
    #     'male_registrations': users.filter(gender='Male').count(),
    #     'female_registrations': users.filter(gender='Female').count(),
    #     'age_group': '18-25',  # Example value
    #     'selected_candidates': applications.filter(selected=True).count(),
    #     'users': users,
    #     'applications': applications,
    # }
    
    # # Load the template
    # template = get_template('admin/admin_report.html')  # Use the correct template path
    # html = template.render(context)
    
    # # Create a HttpResponse object with PDF content
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="admin_report.pdf"'

    # # Generate PDF
    # pisa_status = pisa.CreatePDF(html, dest=response)

    # # Check for errors
    # if pisa_status.err:
    #     return HttpResponse('We had some errors <pre>' + html + '</pre>')
    # return response