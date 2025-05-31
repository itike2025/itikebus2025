from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile
from django.contrib.admin import widgets

class UserRegForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields=['username','email','password1','password2']


#class DateInput(forms.DateInput):
    #input_type ='date'
        
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    #Birth_date = forms.DateField(widget=DateInput)
    #Birth_date = forms.DateTimeField(input_formats=['%d/%m/%Y'])
    class Meta:
        model = User
        fields =['username','email','first_name','last_name']
        

        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        #birth_date = forms.DateField(widget=DateInput)
        model = Profile
        fields = ['sex','status','birth_date','user_image']
        
        widgets = {
        'birth_date': forms.DateInput(format='%d/%m/%Y'),
    }

class ContactForm(forms.Form):
    #email = forms.EmailField(required=True)
    enter_your_email = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = User
        fields =['username','email']


