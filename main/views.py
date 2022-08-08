from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
from django.contrib.auth.models import Group

@allowed_users(allowed_roles=['admin'])
def register(response): #View when user going register in the system

    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            group = Group.objects.get(name='crew')
            user.groups.add(group)
    else:
        form = RegisterForm()
    return render(response, 'login_and_register/register.html', {
        "form": form,
    })

@login_required
def landing_page(response):

    return render(response, "home/home.html")