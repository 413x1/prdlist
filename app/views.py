from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import GetOnlineProductForm, ProductForm
from .models import Product
from django.contrib import messages
from django.shortcuts import get_object_or_404

# Create your views here.
def index(request):
    data = {
        'rform': GetOnlineProductForm,
        'pform': ProductForm,
        'products': Product.objects.exclude(status__name='tidak bisa dijual').order_by('-id'),
    }
    return render(request,'index.html', context=data)

def get_online_products(request):
    if request.method == "POST":
        form_ = GetOnlineProductForm(request.POST)

        if form_.is_valid():
            num_created = form_.save()
            if not num_created:
                messages.warning(request, 'No data created!')
            else:
                messages.success(request, f'{num_created} data created!')
        else:
            error = form_.errors.get('username')[0]
            messages.error(request, f'{error}')
            
    return redirect(reverse('homepage'))


def add_new_product(request):
    if request.method == "POST":
        form_ = ProductForm(request.POST)

        if form_.is_valid():
            product = form_.save()
            messages.success(request, f'Product {product.name} created!')

        else:
            messages.error(request, form_.errors.as_text())
            messages.warning(request, 'Failed to add new product')
            
    return redirect(reverse('homepage'))


def update_product(request, id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=id)
        form_ = ProductForm(request.POST, instance=product)

        if form_.is_valid():
            form_.save()
            messages.success(request, f'Product {product.name} updated!')

        else:
            messages.error(request, form_.errors.as_text())
            messages.warning(request, 'Failed to edit product')
            
    return redirect(reverse('homepage'))


def delete_product(request, id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=id)
        name = product.name
        if product.delete():
            messages.success(request, f'Product {name} deleted!')

        else:
            messages.warning(request, 'Failed to delete product')
            
    return redirect(reverse('homepage'))
