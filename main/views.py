from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
from django.contrib.auth.models import Group, User
from django.utils.text import slugify
from appdirs import unicode
from django.contrib import messages

from .forms import RegisterForm, CustomerForm, UserprofileForm
from manage_product.models import Manage_product
from .models import Customer, Userprofile
from manage_product.models import Add_to_cart


@allowed_users(allowed_roles=['admin'])
def register(response):  # View when user going register in the system
    if response.method == "POST":
        form = RegisterForm(response.POST)
        form_p = UserprofileForm(response.POST)
        if form.is_valid() and form_p.is_valid():
            user = form.save(commit=False)
            user.save()
            group = Group.objects.get(name='crew')
            user.groups.add(group)
            profile = form_p.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(response, "Successfully Registered!")
        else:
            messages.error(
                response, "Invalid: Please check the information you entered!")
    else:
        form = RegisterForm()
    return render(response, 'login_and_register/register.html', {
        "form": form,
    })


def profile(response):
    u = response.user
    up = Userprofile.objects.filter(user=u)
    if response.method == "POST":
        form = RegisterForm(response.POST, instance=response.user)
        form_p = UserprofileForm(
            response.POST, response.FILES, instance=response.user.userprofile)
        if form.is_valid() and form_p.is_valid():
            user = form.save(commit=False)
            user.save()
            profile = form_p.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(response, "Profile successfully edited!")
            return redirect('profile')
    else:
        form = RegisterForm(instance=response.user)
        form_p = UserprofileForm(instance=response.user.userprofile)
    return render(response, 'login_and_register/profile.html', {
        "form": form,
        "form_p": form_p,
        'u': u,
        'up': up,
    })


@login_required
def landing_page(response):
    total_product = Manage_product.objects.filter(availability=True).count()
    total_crew = User.objects.exclude(username="admin").count()
    total_customer = Customer.objects.all().count()
    t_money = Add_to_cart.objects.filter(status="Received")
    total_money = 0
    for money in t_money:
        total = total_money + money.order.price * money.quantity
        total_money = total
    print(total_money)

    money = total_money
    return render(response, "home/home.html", {
        'money': money,
        'total_product': total_product,
        'total_crew': total_crew,
        'total_customer': total_customer,
    })


def customer_info(response):

    if response.method == 'POST':
        form = CustomerForm(response.POST)
        if form.is_valid():
            save = form.save(commit=False)
            slug = slugify(unicode('%s %s %s' % (
                save.name.lower(), str(save.id), save.table_number)))
            save.slug = slug
            save.save()
            save.slug = slugify(unicode('%s %s %s' % (
                save.name.lower(), str(save.id), save.table_number)))
            save.save()
            return redirect("customer_home", save.slug)
        else:
            return HttpResponse("Invalid")
    else:
        form = CustomerForm()
    return render(response, 'customer/customer.html', {
        'form': form,
    })


def customer_home(response, slug):
    customer = Customer.objects.filter(slug=slug)
    product = Manage_product.objects.exclude(availability=False).all()
    return render(response, 'customer/customer_home.html', {
        'product': product,
        'customer': customer,
    })


def customer_nav(response, slug):
    customer = Customer.objects.filter(slug=slug).first()
    orders = Add_to_cart.objects.filter(customer=customer)
    return render(response, 'customer/customer_nav.html', {
        'customer': customer,
        'orders': orders,
    })
