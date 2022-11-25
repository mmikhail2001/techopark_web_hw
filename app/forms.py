from django import forms
from django.db import IntegrityError
from app import models

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 30)
    password = forms.CharField(max_length = 100, widget = forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_repeat = forms.CharField(widget=forms.PasswordInput)
    # avatar = forms.FileField()
    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password_repeat']

    def clean(self):                    
        password = self.cleaned_data['password']
        password_repeat = self.cleaned_data['password_repeat']
        if password != password_repeat:  
            self.add_error('password', error='')                          
            self.add_error('password_repeat', error='')                          
            raise forms.ValidationError("Passwords do not match")
        return self.cleaned_data
    def save(self):
        self.cleaned_data.pop('password_repeat')
        try:
            return models.User.objects.create_user(**self.cleaned_data)
        except IntegrityError:
            # пользователь уже существует
            return None
        # создаем Profile, привязываем к юзеру, добавляем аву

class SettingsForm(forms.ModelForm):
    # avatar = forms.FileField()
    class Meta:
        model = models.User
        fields = ['username', 'email', 'first_name', 'last_name']
    # save from super class

class AskForm(forms.ModelForm):
    tag_list = forms.CharField()
    # avatar = forms.FileField()
    class Meta:
        model = models.Question
        fields = ['title', 'text', 'tag_list']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = ['text']