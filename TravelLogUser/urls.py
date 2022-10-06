from django.contrib.auth.views import LogoutView
from django.urls import path
from django.contrib.auth import views as auth_views


from .views import *

urlpatterns = [
    path('Login/', user_login, name='UserLogin'),
    path('Create/', user_create, name='UserCreate'), #revisar si se puede eliminar
    path('Logout/', LogoutView.as_view(template_name='TravelLogUser/logout.html'), name='UserLogOut'),
    path('User/Create/', user_create, name='UserTravelLogCreate'),
    path('User/Search/', user_search, name='UserTravelLogSearch'),
    path('User/Delete/<str:username>', user_delete, name='UserTravelLogDelete'),
    path('User/Change/<str:username>', user_change, name='UserTravelLogChange'),
    path('User/ChangePass/', ChangePasswordView.as_view(), name='UserTravelLogChangePass'),

# Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='TravelLogUser/password_reset.html',
             subject_template_name='TravelLogUser/password_reset_subject.txt',
             email_template_name='TravelLogUser/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='TravelLogUser/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='TravelLogUser/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='TravelLogUser/password_reset_complete.html'
         ),
         name='password_reset_complete'),

]

