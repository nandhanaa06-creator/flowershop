from django.urls import path, include
from. import views 
urlpatterns = [
     path('cart/increase/<str:id>/', views.increase_qty, name='increase_qty'),
     path('cart/decrease/<str:id>/', views.decrease_qty, name='decrease_qty'),
     

     path("checkout/", views.checkout_page, name="checkout"),
     path('order-success/<int:order_id>/', views.order_success, name='order_success'),
     path('my-orders/', views.my_orders, name='my_orders'),
     path('order/<int:order_id>/', views.order_detail, name='order_detail'),
          
     path('cart/', views.cart_page, name='cart'),
     path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
     path("remove-from-cart/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
     path('order/<int:order_id>/', views.view_single_order, name='view_single_order'),

]
