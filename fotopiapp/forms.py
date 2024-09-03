from django.contrib.auth.models import User
from django import forms
from fotopiapp.models import  UserProfile,Post,Comments,Strories
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    password1= forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model=User
        fields=["username","email", "password1","password2"]

        widgets={

            "username": forms.TextInput(attrs={'class':'form-control'}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
        }

class Loginform (forms.Form ):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude=["user","following","block"]
        
        widgets={
            "dob":forms.DateInput(attrs={"class":"form-control","type":"date"})
        }

class PostUploadForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=["post_image","title"]

        widgets={
            "title":forms.Textarea(attrs={'class':'form-control'}),
            "post_image":forms.FileInput(attrs={'class':'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model=Comments
        fields=["text"]

        widgets={
            "text":forms.Textarea(attrs={'class':'form-control'}),
        }