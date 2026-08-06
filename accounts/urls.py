from django.urls import path, reverse_lazy
from . import views
from .views import CustomPasswordResetView
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('signup/',views.signup_view,name='signup'),
    path('forget-password/',views.CustomPasswordResetView.as_view(),name='password_reset'),
    
    path('password-reset-done/',
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password-reset-done.html'),
        name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password-reset-confirm.html',
            success_url=reverse_lazy('accounts:password_reset_complete')
        ),
        name='password_reset_confirm'),

    path('password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password-reset-complete.html'),
        name='password_reset_complete'),
      
]