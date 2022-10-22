from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

from django.urls import reverse_lazy

from .forms import userRegisterForm, UserFindForm, UserChangeForm
from .models import Avatar

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            data = form.cleaned_data
            username = data.get('username')
            password = data.get('password')
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect('TPFinalMain')
            else:
                messages.info(request, 'Something was wrong!!!')
        else:
            messages.info(request, 'Something was wrong!!!')

    context = {
        'form': AuthenticationForm(),
        'name_submit': 'LogIn',
        'tittle': 'Please write your username and password to log in.'
    }
    return render(request, 'TravelLogUserTemplate/login.html', context)


def user_create(request):
    if request.method == 'POST':
        form = userRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Successful user registration!')
        else:
            messages.info(request, form.errors)

    context = {
        'form': userRegisterForm(),
        'name_submit': 'Create new user',
        'tittle': 'Please write your information to create a new user.'
    }
    return render(request, 'TravelLogUser/login.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_search(request):
    a_buscar = []
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        to_find = User.objects.filter(username__icontains=username) & \
                   User.objects.filter(first_name__icontains=first_name) & \
                   User.objects.filter(last_name__icontains=last_name) & \
                   User.objects.filter(email__icontains=email)
    context = {
        'user_info': UserFindForm(),
        'user': to_find
    }
    return render(request, 'TravelLogUser/user_search.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, username):
    usuario = User.objects.get(username=username)
    usuario.delete()

    return redirect('UserTravelLogSearch')

@login_required()
def user_change(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        usr = UserChangeForm(request.POST or None, request.FILES or None, instance=user)
        if usr.is_valid():
            data = usr.cleaned_data
            usr.save()

            avatar = Avatar.objects.filter(user=user)
            imagen=data.get("imagen")
            if avatar.exists():
                if imagen:
                    avatar = avatar[0]
                    avatar.avatar = imagen
                    avatar.save()

            else:
                avatar = Avatar(user=user, avatar=data.get("image"))
                avatar.save()
            messages.info(request, 'The data has been uploaded successfully!')
        else:
            messages.info(request, usr.errors)

        if request.user.is_superuser:
            return redirect('UserTravelLogChange',username)
        else:
            return redirect('UserTravelLogChange',username)

    usuario_form = UserChangeForm(initial={
           'username': user.username,
           'first_name': user.first_name,
           'last_name': user.last_name,
           'email': user.email,
           'is_staff': user.is_staff,
           'is_active': user.is_active,
           'is_superuser': user.is_superuser
       }
             )
    context = {
        'userform': usuario_form,
        'user': user,
    }

    return render(request, 'UserCoder/userchange.html', context)


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'UserCoder/userchangepass.html'
    success_message = "Your password has been changed successfully."
    success_url = reverse_lazy('UserTravelLogChange')