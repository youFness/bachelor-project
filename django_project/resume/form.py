from django import forms
from .models import Resume
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class UpdateResumeForm(forms.ModelForm):
    phone_number=PhoneNumberField(
        widget=PhoneNumberPrefixWidget(initial='FR')
    )

    class Meta:
        model = Resume 
        exclude=('user',)