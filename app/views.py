from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout
from .models import Product,Category
from .forms import ProductForm, CategoryForm
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import HttpResponseForbidden
from .models import Contact
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile


# Create your views here.

def is_admin(user):
    return user.is_staff or user.is_superuser

def admin_required(views_func):
    def wrapper(request,*args,**kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request,'access denied')
            return redirect('product')
        return views_func(request,*args,**kwargs)
    return wrapper

def home(request):
    return render(request,"home.html")

def about(request):
    return render(request,"about.html")

def login(request):
    if request.method== 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user=authenticate(username=username, password=password)

        if user is not None:
            auth_login(request,user)
            messages.success(request, "you're logged in!")
            return redirect('home')
        else:
            messages.error(request,"invalid username or passwoed.")
            return redirect('login')
    return render(request,"login.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "User already exists")
            return render(request, "signup.html")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, "signup.html")


def contact_view(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')


        #save to database
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        messages.success(request,'your message has been sent successfully')
        return redirect('contact')
    return render(request,'contact.html')

@login_required
def product_list(request):
    products = Product.objects.all()   # ✅ use a plural variable name
    return render(request, 'product_list.html', {'products': products})

@admin_required
def product_create(request):
    form=ProductForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('product')
    return render(request,'product_form.html',{'form' : form})

@admin_required
def product_delete(request,pk):
    product= get_object_or_404(Product,pk=pk)
    if request.method== "POST":
        product.delete()
        return redirect('product')
    return render(request, 'product_confirm_delete.html',{'product':product})
@admin_required
def product_update(request,pk):
    product=get_object_or_404(Product,pk=pk)
    form=ProductForm(request.POST or None,request.FILES or None,instance=product )
    if form.is_valid():
        form.save()
        return redirect('product')
    return render(request,'product_form.html',{'form':form})

def product_details(request,pk):
    product=get_object_or_404(Product,pk=pk)
    

    return render(request,"product_details.html",{'prod':product})

def signout(request):
    username=request.user.username
    logout(request)
    return redirect('login')



# Category List View
@login_required
def category_list(request):
    categories = Category.objects.all().order_by('name')
    context = {
        'categories': categories
    }
    return render(request, 'category_list.html', context)

# Category Create View
@login_required
@admin_required
def category_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        if name:
            Category.objects.create(
                name=name,
                description=description
            )
            messages.success(request, f'✅ Category "{name}" created successfully!')
            return redirect('category_list')
        else:
            messages.error(request, '❌ Category name is required!')
    
    return render(request, 'category_form.html')

# Category Update View
@login_required
@admin_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method=='POST':
        category.name = request.POST.get('name')
        category.description = request.POST.get('description')
        category.save()
        return redirect('category_lis')
        
    return render(request, 'category_update.html',{"category":category} )

# Category Delete View
@login_required
@admin_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'✅ Category "{category_name}" deleted successfully!')
        return redirect('category_list')
    
    context = {'category': category}
    return render(request, 'category_confirm_delete.html', context)



def category_products(request, category_id):
    category = Category.objects.get(id=category_id)

    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'category': category,
        'categories': categories,
        'is_admin': request.user.is_staff or request.user.is_superuser
    }
    return render(request, 'category_products.html', context)

from django.shortcuts import redirect, get_object_or_404
from .models import Product


def cart_page(request):
    cart = request.session.get("cart", {})
    return render(request, "cart.html", {"cart": cart})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        cart[str(product_id)]["qty"] += 1
    else:
        cart[str(product_id)] = {
            "name": product.name,
            "price": float(product.price),
            "qty": 1
        }

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("product")  # redirect back to product list


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def increase_qty(request, id):
    cart = request.session.get('cart', {})

    if id in cart:
        cart[id]['qty'] += 1

    request.session['cart'] = cart
    return redirect('cart')


def decrease_qty(request, id):
    cart = request.session.get('cart', {})

    if id in cart:
        cart[id]['qty'] -= 1
        if cart[id]['qty'] <= 0:
            cart.pop(id)

    request.session['cart'] = cart
    return redirect('cart')

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'account.html', {"profile": profile})


@login_required
def edit_profile(request):

    # If profile doesn't exist, create it (no signals required)
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'edit_profile.html', context)


