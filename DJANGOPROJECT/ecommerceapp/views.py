from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout

# import product from model.py 
from .models import Product 
from .forms import ProductForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

def user_login(request):
    return render(request, 'login.html')

# fetch all dats using ORM
# def product_list(request):
def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products' : products})
    # sending data to templates
    

@staff_member_required
def crud_updates(request):

    # Add Product
    if request.method == 'POST' and 'add_product' in request.POST:
        add_form = ProductForm(request.POST, request.FILES)

        if add_form.is_valid():
            add_form.save()
            messages.success(request, "Product added successfully!")
            return redirect('crud_updates')
        else:
            messages.error(request, "Error adding product. Check inputs. ")
    else:
        add_form = ProductForm()

        # list projects
    products = Product.objects.all()

    # edit  product
    edit_product = None
    edit_form = None

    edit_id = request.GET.get('edit_id')
    if edit_id:
        edit_product = get_object_or_404(Product, id= edit_id )
        
        if request.method == 'POST' and 'edit_product' in request.POST:
            edit_form = ProductForm(request.POST, request.FILES, instance = edit_product)

            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, "Product updated successfully!")
            else:
                messages.error(request, "Error updating product.")

    else:
        edit_form = ProductForm(instance = edit_product)


    # delete product
    delete_id = request.GET.get('delete_id')

    if delete_id:
        try:
            product = Product.objects.get(id = delete_id)
            product.delete()
            messages.success(request, "Product deleted successfully!")
            return redirect('crud_updates')
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")


    return render(request, 'crud_updates.html', {
        'products' : products,
        'add_form' : add_form,
        'edit_form' :edit_form,
        'edit_product' : edit_product,
    })

    #  add to cart
def add_to_cart(request, id):

    # get cart from session
    cart = request.session.get('cart', [])

    # add to product
    cart.append(id)

    # save back to session
    request.session['cart'] = cart 

    messages.success(request, "Product added to cart!")

    return redirect('cart') 

# view cart
def cart(request):

    # get cart from session
    cart = request.session.get('cart', [])

    # fetch products
    products = Product.objects.filter(id__in = cart)

    return render(request, 'cart.html', {'products' : products})




# def cart(request):
#     return render(request, 'cart.html')

# Login
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Login Successful")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials")

    return render(request, 'login.html')

# LOGOUT
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login')