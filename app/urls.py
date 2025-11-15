from django.contrib import admin
from django.urls import path    
from.import views


urlpatterns = [
    path('',views.home,name="home"),
    path('about/',views.about,name="about"),
    path('login/',views.login,name="login"),
    path('signup/',views.signup,name="signup"),
    path('contact/',views.contact_view,name="contact"),
    path('product',views.product_list,name='product'),
    path('create/',views.product_create,name='create_product'),
    path('delete/<int:pk>/',views.product_delete,name='product_delete'),
    path('update/<int:pk>/',views.product_update,name='product_update'),
    path('details/<int:pk>/',views.product_details,name='product_details'),
    
    path('cart/', views.cart_page, name='cart'),
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove-from-cart/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),

    path('logout/',views.signout,name="logout"),


    
    
    path('categories/', views.category_list, name='category_list'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/<int:pk>/update/', views.category_update, name='category_update'),
    path('category/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    

    
]
