
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

from personalblog.models import Profile

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=200,required=True)

    password1 = forms.CharField(max_length=200,required=True)

    password2 = forms.CharField(max_length=200,required=True)

    email = forms.CharField(max_length=200,required=True)

    first_name = forms.CharField(max_length=200,required=True)


    last_name = forms.CharField(max_length=200,required=True)

    class Meta:
        model = User
        fields = ["first_name","last_name","email","username","password1"]



class LoginForm(AuthenticationForm):

    username = forms.CharField(max_length=200,required=True)

    password1 = forms.CharField(max_length=200,required=True)

    class Meta:
        model = User
        fields = ['username','password']


class UpdateUserForm(forms.ModelForm):

    username = forms.CharField(max_length=200,required=True)

    email = forms.CharField(max_length=200,required=True)



    class Meta:
        model = User
        fields = ["username","email"]


class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["bio","img"]