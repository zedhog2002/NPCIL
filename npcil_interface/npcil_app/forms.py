from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Package


class Registerform(UserCreationForm):
    email = forms.EmailField(label = "", widget= forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Email Address'}) )
    first_name = forms.CharField(label = "",max_length=100, widget= forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'First Name'}))
    last_name = forms.CharField(label = "",max_length=100, widget= forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Last Name'}))

    class Meta:
        model = User
        fields = ('email','first_name','last_name','password1','password2')


    def __init__(self, *args, **kwargs):
        super(Registerform, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].label = ''
        self.fields['email'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

class Addrecordform(forms.ModelForm):
    package_id = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Package id", "class": "form-control"}),
        label='Package ID'
    )
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Package name", "class": "form-control"}),
        label='Package name'
    )
    version = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Version", "class": "form-control"}),
        label='Version'
    )
    node_id = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Node Id", "class": "form-control"}),
        label='Node ID'
    )

    class Meta:
        model = Package
        exclude = ('Email',)
