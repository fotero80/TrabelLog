from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User


class DateImput(forms.DateInput):
    input_type = 'date'

# form asking data to create users
class userRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

# form asking data to search users
class UserFindForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

# form asking data to change users info
class UserChangeForm(UserChangeForm):
    imagen = forms.ImageField(required=False)
