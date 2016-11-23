from django import forms

class formSignUp(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form_element_design',
     'placeholder':'Full Name'}),label='')
    username_email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control form_element_design',
        'placeholder':'Email'}),label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form_element_design',
     'placeholder':'Password'}),label='')
    # widgets = {'password': forms.PasswordInput(),}
    
class formLogin(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control form_element_design',
        'placeholder':'Email'}),label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form_element_design',
     'placeholder':'Password'}),label='')