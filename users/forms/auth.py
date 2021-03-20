import secrets

from django import forms

from users.models import User


class LoginForm(forms.Form):

    login = forms.CharField()
    password = forms.CharField()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(min_length=8)
    password_confirmation = forms.CharField(min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirmation']

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            raise forms.ValidationError(
                'Password do not match',
                code='password_confirmation',
            )
        return password_confirmation

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(user.password)

        user.email_verification_token = secrets.token_urlsafe(16)
        if commit:
            user.save()
        return user
