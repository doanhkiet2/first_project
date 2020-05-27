from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Create your views here.


def login_view(request, *args, **kwargs):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user_ = form.get_user()
        login(request, user_)
        return redirect("/")
    context = {"form": form, "btn_label": "Login", "title": "login"}
    return render(request, "accounts/auth.html", context)


def logout_view(request, *args, **kwargs):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        logout(request)
        return redirect("/login")
        context = {
            "form": None,
            "btn_label": "Logout",
            "title": "Logout",
            "dicription": "are you sure you want to log out?"}

    return render(request, "accounts/auth.html", context)


def register_view(request, *args, **kwargs):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=True)
        user.set_password(form.cleaned_data.get("password1"))
        # username = form.cleaned_data.get("username")
        # User.objects.Create(username=username)
        # send a confirmation email to verify their account

    context = {
        "form": form,
        "btn_label": "Register",
        "title": "Register"

    }
    return render(request, "accounts/auth.html", context)
