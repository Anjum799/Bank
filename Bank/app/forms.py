from django import forms
from .models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name','mobile','email','aadhaar','father_name','dob','address','gender','states','photo']
        