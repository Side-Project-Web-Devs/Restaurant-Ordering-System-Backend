from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.utils.text import slugify
from appdirs import unicode
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users

from .models import Manage_product, Add_to_cart
from .forms import Manage_productForm
from main.models import Customer


# Create your views here.
@login_required
@allowed_users(allowed_roles=['admin'])
def add_product(response):
    user = response.user
    if response.method == 'POST':
        form = Manage_productForm(response.POST, response.FILES)
        print("1")
        if form.is_valid():
            save = form.save(commit=False)
            save.user = user
            slug = slugify(unicode('%s %s' % (save.product_name.lower(), save.description.lower())))
            save.slug = slug
            save.save()
            print("working")
        else:
            return HttpResponse("Invalid")

    form = Manage_productForm()
    img = form.instance
    product = Manage_product.objects.all()
    return render(response, 'product/add_product.html', {
        'form': form,
        'img': img,
        'product': product,

    })

@login_required
@allowed_users(allowed_roles=['admin'])
def edit_product(response, slug):
    pro = get_object_or_404(Manage_product, slug=slug)
    form = Manage_productForm(response.POST or None, instance=pro)
    user = response.user

    if response.method == "POST":
        form = Manage_productForm(response.POST or None, instance=pro)
        if form.is_valid():
            save = form.save(commit=False)
            save.user = user
            slug = slugify(unicode('%s %s' % (save.product_name.lower(), save.description.lower())))
            save.slug = slug
            save.save()
        return redirect('add_product')
    return render(response, 'product/edit_product.html', {
        'form': form,
        'pro': pro,
    })

def delete_product(response, slug):
    product = Manage_product.objects.filter(slug=slug).first()
    product = get_object_or_404(Manage_product, slug=slug)
    product.delete()
    return redirect('add_product')

def customer_addcart(response, customer, order):
    customer = Customer.objects.get(slug=customer)
    product = Manage_product.objects.get(slug=order)
    if response.method == 'POST':
        quantity = response.POST.get('quantity')
        status = "in_cart"
        slug = slugify(unicode('%s %s' % (customer.name.lower(), product.product_name.lower())))
        addcart = Add_to_cart(customer=customer, order=product, quantity=quantity, status=status, slug=slug)
        addcart.save()
        return redirect('customer_home', customer.slug)

    return render(response, 'cart/add_cart.html', {
        'customer': customer,
        'product': product,
    })

def customer_cart(response, customer):
    cus = Customer.objects.filter(slug=customer).first()
    order = Add_to_cart.objects.filter(customer=cus)
    if not order:
        return HttpResponse('Empty')

    return render(response, 'cart/customer_cart.html', {
        'order': order,
    })

def place_order(response, slug):
    in_cart = get_object_or_404(Add_to_cart, slug=slug)
    data = Add_to_cart.objects.get(customer=in_cart.customer, order=in_cart.order, slug=in_cart.slug)
    if response.method == "POST":
        data.status = "ordered"
        data.quantity = response.POST.get('quantity')
        data.save()
        return redirect('customer_home', data.customer.slug)

    return render(response, 'cart/place_order.html', {
        'in_cart': in_cart,
    })

def view_customer_order(response):
    orders = Add_to_cart.objects.all()
    return render(response, 'crew/view_order.html', {
        'orders': orders,
    })



