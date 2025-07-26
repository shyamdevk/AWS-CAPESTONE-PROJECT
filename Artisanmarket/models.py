from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=50,unique=True)
    phone=models.BigIntegerField(unique=True)
    password=models.CharField(max_length=255)
    email=models.CharField(max_length=100)
    role=models.CharField(max_length=50)

class Product(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    productname=models.CharField(max_length=50)
    productdetails=models.CharField(max_length=100)
    actual_price=models.BigIntegerField(null=True)
    offer_price=models.BigIntegerField(null=True)
    category=models.CharField(max_length=5)
    types=models.CharField(max_length=50)
    quantity=models.IntegerField(null=True)
    image1=models.CharField(max_length=100)
    image2=models.CharField(max_length=100)
    image3=models.CharField(max_length=100)
    
class order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    fullname=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    phone=models.BigIntegerField(null=True)
    message=models.CharField(max_length=50)
    price=models.IntegerField(null=True)
    quantity=models.IntegerField(null=True)


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class OTPVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
