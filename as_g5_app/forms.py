from django import forms
from django.contrib.auth.models import User
from as_g5_app.models import userData
from django_recaptcha.fields import ReCaptchaField
import re
class userForm(forms.ModelForm):
    #password is showing if we want to hide the password we have to write this line 
    password=forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model=User
        # fields="__all__"
        fields=['first_name','last_name','username','email','password','date_joined']
    
class userForm2(forms.ModelForm):
    class Meta:
        model=userData
        fields=['phone_no','gender','zip_code','city','state','profile_pic']
    captcha = ReCaptchaField()
    


    def clean_phone_no(self):
        phone = self.cleaned_data.get('phone_no')
        if phone is None or not re.match(r'^[6-9]\d{9}$', str(phone)):
            raise forms.ValidationError("Enter a valid 10-digit Indian phone number starting with 6–9.")
        return phone

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if gender not in ['Male', 'Female', 'Other']:
            raise forms.ValidationError("Please select a valid gender: Male, Female, or Other.")
        return gender

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get('zip_code')
        if not re.match(r'^\d{6}$', str(zip_code)):
            raise forms.ValidationError("Enter a valid 6-digit Indian ZIP code.")
        return zip_code

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if not city or not city.isalpha():
            raise forms.ValidationError("City name must contain only letters.")
        return city

    def clean_state(self):
        state = self.cleaned_data.get('state')
        if not state or not state.isalpha():
            raise forms.ValidationError("State name must contain only letters.")
        return state

    def clean_profile_pic(self):
        pic = self.cleaned_data.get('profile_pic')
        if pic and pic.size > 5 * 1024 * 1024:  # 5MB limit
            raise forms.ValidationError("Profile picture size should not exceed 5MB.")
        return pic

class updateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','email']
        

class updateForm2(forms.ModelForm):
    class Meta:
        model=userData
        fields=['phone_no','gender','zip_code','city','state','profile_pic']
    
    
class forgetPasswordForm(forms.Form):
    username=forms.CharField(max_length=150)
    password=forms.CharField(max_length=150,widget=forms.PasswordInput)
    confirm_password=forms.CharField(max_length=150,widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if username:
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                raise forms.ValidationError("Username does not exist.")
    
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        # if password != confirm_password:
        #     raise forms.ValidationError("Passwords do not match.")