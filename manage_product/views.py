from ast import Add
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.utils.text import slugify
from appdirs import unicode
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
from django.contrib import messages
from django.utils.timezone import now

from .models import Manage_product, Add_to_cart, Feedback, Inventory, Date_inv
from .forms import Manage_productForm, FeedbackForm
from main.models import Customer


# Create your views here.
@login_required
@allowed_users(allowed_roles=['admin'])
def add_product(response):
    user = response.user
    if response.method == "POST":
        form = Manage_productForm(response.POST, response.FILES)
        print("1")
        if form.is_valid():
            save = form.save(commit=False)
            save.user = user
            save.save()
            save.slug = slugify(unicode('%s %s %s' % (
                save.product_name.lower(), str(save.id), save.description.lower())))
            save.save()
            messages.success(response, "Product successfully added to menu!")
        else:
            messages.error(response, "Invalid Input!")

    form = Manage_productForm()
    product = Manage_product.objects.all()
    return render(response, 'product/add_product.html', {
        'form': form,
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
            save.save()
            save.slug = slugify(unicode('%s %s %s' % (
                save.product_name.lower(), str(save.id), save.description.lower())))
            save.save()
            messages.success(response, "Product successfully edited!")
        return redirect('add_product')
    return render(response, 'product/edit_product.html', {
        'form': form,
        'pro': pro,
    })


@login_required
@allowed_users(allowed_roles=['admin'])
def delete_product(response, slug):
    product = Manage_product.objects.filter(slug=slug).first()
    product = get_object_or_404(Manage_product, slug=slug)
    product.delete()
    messages.error(response, "Product successfully deleted!")
    return redirect('add_product')


@login_required
@allowed_users(allowed_roles=['admin'])
def product_availability(response, slug):
    product = get_object_or_404(Manage_product, slug=slug)
    data = Manage_product.objects.get(product_name=product.product_name, description=product.description,
                                      price=product.price, image=product.image, slug=product.slug)
    data.user = response.user
    data.availability = False
    data.save()
    messages.success(response, "Product mark as Unavailable")
    return redirect('add_product')


@login_required
@allowed_users(allowed_roles=['admin'])
def return_availability(response, slug):
    product = get_object_or_404(Manage_product, slug=slug)
    data = Manage_product.objects.get(product_name=product.product_name, description=product.description,
                                      price=product.price, image=product.image, slug=product.slug)
    data.user = response.user
    data.availability = True
    data.save()
    messages.success(response, "Product mark as Available")
    return redirect('add_product')


@login_required
@allowed_users(allowed_roles=['admin'])
def inventory(response):
    pro = Manage_product.objects.all()
    inv = Inventory.objects.all()
    date = Date_inv.objects.all().order_by("date")
    if response.method == "POST":
        d = Date_inv()
        d.save()
        for p in pro:
            inve = Inventory(product=p.product_name, remaining=p.remaining,
                             sold=p.sold, new=p.new, total=p.total)
            inve.save()
        messages.success(response, "Successfully added")
        return redirect("inventory")

    return render(response, 'product/inventory.html', {

        'inv': inv,
        'pro': pro,
        'date': date,
    })


@login_required
@allowed_users(allowed_roles=['admin'])
def edit_inventory(response, id):
    pro = get_object_or_404(Manage_product, id=id)
    if response.method == "POST":
        sold = response.POST.get("sold")
        new = response.POST.get("new")
        remaining = response.POST.get("remaining")
        data = Manage_product.objects.get(product_name=pro.product_name, description=pro.description,
                                          price=pro.price, image=pro.image, slug=pro.slug)
        data.sold = sold
        data.new = new
        data.remaining = remaining
        data.total = int(data.remaining) + int(sold) + int(new)

        data.save()
        messages.success(response, "Successfully edited!")
        return redirect('inventory')

    form = Manage_productForm(response.POST or None, instance=pro)
    return render(response, 'product/edit_inventory.html', {
        'pro': pro,
    })


def customer_addcart(response, customer, order):
    customer = Customer.objects.get(slug=customer)
    product = Manage_product.objects.get(slug=order)
    cart = Add_to_cart.objects.filter(customer=customer, order=product)
    if response.method == 'POST':
        quantity = response.POST.get('quantity')
        status = "in_cart"
        to_di = response.POST.get('to_di')
        if to_di == "True":
            if Add_to_cart.objects.filter(customer=customer, order=product, status=status):
                messages.error(response, "This product is already in cart")
                return redirect('customer_home', customer.slug)
            else:
                slug = slugify(unicode('%s %s' % (
                    customer.name.lower(), product.product_name.lower())))
                addcart = Add_to_cart(
                    customer=customer, order=product, quantity=quantity, status=status, to_di='Take Out', slug=slug)
                addcart.save()
                messages.success(response, "Successfully added to cart")
                return redirect('customer_home', customer.slug)
        elif to_di == "False":
            if Add_to_cart.objects.filter(customer=customer, order=product, status=status):
                messages.error(response, "This product is already in cart")
                return redirect('customer_home', customer.slug)
            else:
                slug = slugify(unicode('%s %s' % (
                    customer.name.lower(), product.product_name.lower())))
                addcart = Add_to_cart(
                    customer=customer, order=product, quantity=quantity, status=status, to_di='Dine In', slug=slug)
                addcart.save()
                messages.success(response, "Successfully added to cart")
                return redirect('customer_home', customer.slug)

    return render(response, 'customer/add_cart.html', {
        'customer': customer,
        'product': product,
    })


def customer_cart(response, customer):
    cus = Customer.objects.filter(slug=customer).first()
    cart = Add_to_cart.objects.filter(customer=cus)
    if response.method == "POST":
        if response.POST.getlist("status"):
            data = response.POST.getlist("status")

            for d in data:
                get = get_object_or_404(Add_to_cart, id=d)

                ords = Add_to_cart(customer=get.customer, order=get.order,
                                   quantity=get.quantity, status="ordered", to_di=get.to_di, slug=get.slug, id=get.id)
                ords.save()
                messages.success(response, "Successfully placed order!")
            return redirect('customer_cart', cus.slug)

    return render(response, 'customer/customer_cart.html', {
        'cart': cart,
        'cus': cus,
    })


def edit_cart(response, id):
    in_cart = get_object_or_404(Add_to_cart, id=id)
    data = Add_to_cart.objects.get(
        customer=in_cart.customer, status=in_cart.status, to_di=in_cart.to_di, order=in_cart.order, id=in_cart.id)
    print(in_cart)
    if response.method == "POST":
        data.quantity = response.POST.get('quantity')
        data.to_di = response.POST.get('to_di')
        if data.to_di == "True":
            data.to_di = "Take Out"
            data.save()
        elif data.to_di == "False":
            data.to_di = "Dine In"
            data.save()
        messages.success(response, "Product successfully edited!")
        return redirect('customer_cart', data.customer.slug)

    return render(response, 'customer/edit_cart.html', {
        'in_cart': in_cart,
    })


def my_order(response, slug):
    customer = Customer.objects.filter(slug=slug).first()
    orders = Add_to_cart.objects.filter(customer=customer)

    return render(response, 'customer/orders.html', {
        'orders': orders,
        'customer': customer,
    })


def receive_order(response, id):
    receive = get_object_or_404(Add_to_cart, id=id)
    data = Add_to_cart.objects.get(customer=receive.customer, order=receive.order,
                                   quantity=receive.quantity, slug=receive.slug, id=receive.id)
    data.status = "Received"
    data.save()
    messages.success(response, "Order Received!")
    return redirect('my_order', receive.customer.slug)


def feedback(response, id):
    order = Add_to_cart.objects.get(id=id)
    if response.method == "POST":
        form = FeedbackForm(response.POST)
        print("1")
        if form.is_valid():
            save = form.save(commit=False)
            save.cus = order.customer
            save.ord = order
            save.save()
            messages.success(response, "Feedback successfully submitted!")
            return redirect('my_order', order.customer.slug)
        else:
            messages.error(response, "Invalid feedback")
            return redirect('my_order', order.customer.slug)
    form = FeedbackForm()
    return render(response, 'customer/feedback.html', {
        'form': form,
        'order': order,
    })


def feedback_cusview(response, slug):
    customer = Customer.objects.filter(slug=slug).first()
    feedback = Feedback.objects.filter(cus=customer)
    return render(response, 'customer/feedback_view.html', {
        'feedback': feedback,
        'customer': customer,
    })


@login_required
@allowed_users(allowed_roles=['admin'])
def feedback_admview(response):
    feedback = Feedback.objects.all().order_by('feedback')
    return render(response, 'crew/feedback_view.html', {
        'feedback': feedback,
    })


@login_required
@allowed_users(allowed_roles=['admin'])
def feedback_reply(response, id):
    feedback = Feedback.objects.filter(id=id)
    feed = get_object_or_404(Feedback, id=id)
    if response.method == "POST":
        form = FeedbackForm(response.POST, instance=feed)
        if form.is_valid():
            form.save()
            messages.success(response, "Feedback replied successfully!")
            return redirect('feedback_admview')
    form = FeedbackForm()
    return render(response, 'crew/feedback_reply.html', {
        'form': form,
        'feedback': feedback,
    })


@login_required
@allowed_users(allowed_roles=['admin'])
def delete_reply(response, id):
    feed = get_object_or_404(Feedback, id=id)
    feed.reply = ""
    feed.save()
    messages.error(response, "Reply deleted!")
    return redirect("feedback_admview")


@login_required
@allowed_users(allowed_roles=['admin', 'crew'])
def customer_list(response):
    customer = Customer.objects.all()

    return render(response, "crew/customer_list.html", {
        'customer': customer,
    })


@login_required
@allowed_users(allowed_roles=['admin', 'crew'])
def total_order(response):
    orders = Add_to_cart.objects.all()

    return render(response, "crew/total_order.html", {
        'orders': orders,
    })


@login_required
@allowed_users(allowed_roles=['admin', 'crew'])
def view_customer_order(response, slug):
    customer = Customer.objects.filter(slug=slug).first()
    orders = Add_to_cart.objects.filter(customer=customer).order_by('status')
    return render(response, 'crew/view_order.html', {
        'orders': orders,
        'customer': customer,
    })


@login_required
@allowed_users(allowed_roles=['admin', 'crew'])
def confirm_order(response, id):
    order = get_object_or_404(Add_to_cart, id=id)
    data = Add_to_cart.objects.get(
        customer=order.customer, order=order.order, quantity=order.quantity, slug=order.slug, id=order.id)
    data.status = "Confirmed: Preparing your order"
    data.save()
    messages.success(response, "Order confirmed!")
    return redirect('customer_order', data.customer.slug)


@login_required
@allowed_users(allowed_roles=['admin', 'crew'])
def serve_order(response, id):
    order = get_object_or_404(Add_to_cart, id=id)
    data = Add_to_cart.objects.get(
        customer=order.customer, order=order.order, quantity=order.quantity, slug=order.slug, id=order.id)
    data.status = "Ready to serve"
    data.save()
    messages.success(response, "Ready to serve!")
    return redirect('customer_order', data.customer.slug)
