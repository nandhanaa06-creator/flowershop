from django.db import models
from django.contrib.auth.models import User





# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    description= models.TextField(blank=True,null=True)

    class Meta:
        verbose_name_plural="categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=150)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    description=models.TextField()
    image=models.ImageField(upload_to='products/')
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")

    def __str__(self):
        return self.name

class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    subject=models.CharField(max_length=100)
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', default='default.png')

    def __str__(self):
        return self.user.username
