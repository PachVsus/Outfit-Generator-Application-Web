from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import AccountDeletionForm, ProfileForm, SignUpForm
from .models import AccountDeletionFeedback


def signup(request):
    if request.user.is_authenticated:
        return redirect("wardrobe:dashboard")
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("wardrobe:dashboard")
    return render(request, "registration/signup.html", {"form": form})


@login_required
def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your profile was updated.")
        return redirect("accounts:profile")
    return render(request, "accounts/profile.html", {"form": form})


@login_required
def delete_account(request):
    form = AccountDeletionForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        if not request.POST.get("skip"):
            AccountDeletionFeedback.objects.create(
                reason=form.cleaned_data["reason"],
                details=form.cleaned_data.get("other_reason", "").strip(),
            )
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account and wardrobe were permanently deleted.")
        return redirect("home")
    return render(request, "accounts/delete_account.html", {"form": form})
