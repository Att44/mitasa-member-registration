from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *


class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
        exclude = ['status','data_created', 'noPekerja',]

class StatusForm(ModelForm):
    class Meta:
        model = Member
        fields = ['status']    
        

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']



class UploadFileForm(forms.Form):
    file = forms.FileField()
    date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))  # New code: Add date field