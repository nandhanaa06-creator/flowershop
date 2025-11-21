from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending','Pending'),
        ('Processing','Processing'),
        ('Shipped','Shipped'),
        ('Delivered','Deliered')
    ]

    user=models.ForeignKey(User,on_delete=models.SET_NULL, null=True,blank=True)
    full_name=models.CharField(max_length=200)
    email=models.EmailField()
    phone=models.CharField(max_length=20)
    address=models.TextField()
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=200)
    pincode=models.CharField(max_length=10)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, default='COD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Order {self.id} by {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
