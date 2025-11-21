from django.shortcuts import render,redirect, get_object_or_404
from app.models import *
from .models import Order ,OrderItem

# Create your views here.


def cart_page(request):
    cart = request.session.get("cart", {})
    total = sum(item["price"] * item["qty"] for item in cart.values())
    return render(request, "cart.html", {"cart": cart, "total": total})

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

def checkout_page(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')

    total = sum(item['price'] * item['qty'] for item in cart.values())

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=request.POST['full_name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            pincode=request.POST['pincode'],
            total_price=total,
            payment_method=request.POST.get('payment_method', 'COD'),
        )
        for item in cart.values():
            OrderItem.objects.create(
                order=order,
                product_name=item['name'],
                product_price=item['price'],
                quantity=item['qty']
            )
        request.session['cart'] = {}  # Clear cart
        request.session.modified = True
        return redirect('order_success', order_id=order.id)

    return render(request, 'checkout.html', {'cart': cart, 'total': total})


def order_success(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order_success.html', {'order': order})


from django.contrib.auth.decorators import login_required

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})

def order_success(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order_success.html', {'order': order})



@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()  # Related name in your model
    return render(request, 'order_details.html', {
        'order': order,
        'items': items
    })

@login_required
def view_single_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'view_single_order.html', {'order': order})
