from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    bio = forms.CharField() 
    class Meta:
        model = User
        fields = ['username','email']
        
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude =['author','profile','like','comments']   

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','bio']     
        
class RatingForm(forms.ModelForm):
    class Meta:
        model = Ratings
        design_rating = forms.IntegerField()
        usability_rating = forms.IntegerField()
        content_rating = forms.IntegerField()
        comment = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control","placeholder": "Leave a comment"}))    
        exclude =['project','author']    