from django import forms

from MyRecipes_App.models import Recipe

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

from django.contrib.auth import authenticate


class RegistrationForm(UserCreationForm):

    class Meta:

        model=User

        fields=["username","email","password1","password2"]


class SignInForm(forms.Form):

    username=forms.CharField()

    password=forms.CharField()

    def clean_password(self):
       
       u_name=self.cleaned_data.get("username")

       pwd=self.cleaned_data.get("password")

       user_object=authenticate(username=u_name,password=pwd)

       if user_object==None:
           
           raise ValidationError("Invalid password")
       
       return pwd




class RecipeForm(forms.ModelForm):

    class Meta:

        model=Recipe

        exclude=("created_at","owner",)


    