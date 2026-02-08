from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order
from .forms import ProductForm, OrderForm

def home(request):
    products = Product.objects.all()
    return render(request, 'Bstore/home.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'Bstore/product_form.html', {'form': form})

def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm(instance=product)
    return render(request, 'Bstore/product_form.html', {'form': form})

def delete_product(request, id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=id)
        product.delete()
        return redirect('home')
    return render(request, 'Bstore/delete.html')

def buy_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.total = product.price * order.quantity
            product.stock -= order.quantity
            product.save()
            order.save()
            return redirect('orders')
    else:
        form = OrderForm()
    return render(request, 'Bstore/buy.html', {'form': form, 'product': product})

def orders(request):
    orders = Order.objects.all().order_by('-date')
    return render(request, 'Bstore/orders.html', {'orders': orders})
