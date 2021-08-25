from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


@login_required(login_url="/login/")
def home(request):
    return render(request, "home.html", context={"request": request})


def register(request):
    if request.method == "POST":
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, "Account created successfully")
            return redirect("/login/?next=/")
    else:
        f = UserCreationForm()

    return render(request, "registration/register.html", {"form": f})
