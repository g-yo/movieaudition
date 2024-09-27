from django.urls import path
from .views import *
from django.contrib import admin
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [


    path('admin/', admin.site.urls),
    path('adminlogin/', views.admin_login, name='adminlogin'),  # Admin login
    path('adminlogin/admin/admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Custom admin dashboard
    path('add_movie/', views.add_movie, name='add_movie'),  # Custom add movie page
    path('view_applications/', view_applications, name='view_applications'),  # Custom view applications page
    path('delete_movie/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('edit_movie/<int:movie_id>/', views.edit_movie, name='edit_movie'),  # Edit movie page
    path('adminlogin/admin/admin_overview', views.admin_overview, name='admin_overview'),
    path('application/<int:application_id>/', application_detail, name='application_detail'),
    path('application/<int:application_id>/', application_details, name='application_details'),
    path('applications/select/<int:application_id>/', select_application, name='select_application'),
    path('applications/reject/<int:application_id>/', reject_application, name='reject_application'),



    path('', movie_list, name='movie_list'),
    path('movie/<int:pk>/', movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/apply/', apply_for_movie, name='apply_for_movie'),
    path('success/', application_success, name='application_success'),
    path('register/', register, name='register'),
    path('userlogin/', views.userlogin, name='userlogin'),  # Regular user login
    path('logout/', user_logout, name='user_logout'),
    path('profile/', user_profile, name='user_profile'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('movies_by_age/<int:age>/', views.movies_by_age, name='movies_by_age'),
    path('overview/', views.overview, name='overview'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('notifications/', views.notifications, name='notifications'),
    path('profile/', views.user_profile, name='user_profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('notifications/', views.notifications, name='notifications'),

    # Password reset (Forgot Password)
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
