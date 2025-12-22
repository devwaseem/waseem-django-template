from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            {
                "placeholder": "you@example.com",
                "autocomplete": "email",
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            {
                "placeholder": "Enter your password",
                "autocomplete": "current-password",
            }
        ),
    )
