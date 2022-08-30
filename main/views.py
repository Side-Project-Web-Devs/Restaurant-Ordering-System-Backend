from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
from django.contrib.auth.models import Group
from django.utils.text import slugify
from appdirs import unicode
from .forms import RegisterForm, CustomerForm
from manage_product.models import Manage_product
from .models import Customer
from manage_product.models import Add_to_cart


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


def customer_info(response):

    if response.method == 'POST':
        form = CustomerForm(response.POST)
        if form.is_valid():
            save = form.save(commit=False)
            slug = slugify(unicode('%s %s %s' % (save.name.lower(), str(save.id), save.table_number)))
            save.slug = slug
            save.save()
            save.slug = slugify(unicode('%s %s %s' % (save.name.lower(), str(save.id), save.table_number)))
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