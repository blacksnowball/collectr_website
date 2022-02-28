from django import forms

class LoginForm(form.Form): 
    email = form.CharField(label="Email", widget=forms.TextInput, max_length=500)
    password = form.CharField(label="Password", widget=forms.PasswordInput, max_length=500)