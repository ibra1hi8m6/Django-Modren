from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.CharField(max_length=100)
    mainImage = models.FileField()

class Subcategory(models.Model):
    title = models.CharField(max_length=75)
    image = models.FileField()
    mainImage = models.FileField()
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)

class Product(models.Model):
    title = models.CharField(max_length=255)
    mainImage = models.FileField(default="default.png")
    specs = models.FileField()
    price = models.IntegerField()
    description = models.TextField()
    isBestSeller = models.BooleanField(default=False)
    product_info_main_image = models.FileField()
    product_info_main_paragraph = models.TextField()
    subcategory = models.ForeignKey(to=Subcategory, on_delete=models.CASCADE)

    def rating(self):
        reviews = Review.objects.filter(product=self)
        sum = 0

        for review in reviews:
            sum += review.rating

        rating = 0

        if len(reviews) != 0:
            rating = sum / len(reviews)

        return {
            "reviews" : reviews,
            "count" : len(reviews),
            "rating" : rating
        }

class ProductImage(models.Model):
    image = models.FileField()
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)

class ProductInfoSection(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField()
    image = models.FileField()
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)

class Review(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    rating = models.FloatField()
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)

class Coupon(models.Model):
    code = models.CharField(max_length=50)
    discount_percentage = models.PositiveIntegerField()

class Cart(models.Model):
    items = models.ManyToManyField(Product, through='CartItem')
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    coupon = models.ForeignKey(Coupon, on_delete=models.PROTECT, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def total_price(self):
        subtotal = sum(item.subtotal for item in CartItem.objects.get(id=self.id))
        if self.coupon:
            discount = subtotal * (self.coupon.discount_percentage / 100.0)
            subtotal = round(subtotal - discount, 2)
        total = subtotal + self.shipping
        return round(total, 2)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    # subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.product.price * self.quantity


class Checkout(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street_address = models.CharField(max_length=100)
    coffee_name = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    message = models.TextField(blank=True)

    def __str__(self):
        return f"Checkout of {self.coffee_name}"