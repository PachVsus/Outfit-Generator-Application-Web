from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account already uses this email address.")
        return email


class ProfileForm(UserChangeForm):
    password = None
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        duplicate = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists()
        if duplicate:
            raise forms.ValidationError("An account already uses this email address.")
        return email


class AccountDeletionForm(forms.Form):
    REASONS = (
        ("not_useful", "I no longer find the application useful"),
        ("missing_features", "It is missing features I need"),
        ("technical_issues", "I experienced technical problems"),
        ("privacy", "I have privacy concerns"),
        ("switching", "I am switching to another service"),
        ("other", "Other (specify)"),
    )

    reason = forms.ChoiceField(choices=REASONS, widget=forms.RadioSelect, required=False)
    other_reason = forms.CharField(
        required=False,
        max_length=500,
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-control", "placeholder": "Tell us what we could improve"}),
    )
    current_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "current-password"}))

    def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        password = self.cleaned_data["current_password"]
        if not self.user.check_password(password):
            raise forms.ValidationError("Your password is incorrect.")
        return password

    def clean(self):
        cleaned = super().clean()
        if self.data.get("skip"):
            return cleaned
        reason = cleaned.get("reason")
        if not reason:
            self.add_error("reason", "Select a reason or use Skip.")
        if reason == "other" and not cleaned.get("other_reason", "").strip():
            self.add_error("other_reason", "Please specify your reason.")
        return cleaned
