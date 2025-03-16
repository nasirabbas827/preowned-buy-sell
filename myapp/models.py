from django.db import models
from django.contrib.auth.models import User
from django.core import validators

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    USER_TYPE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, default="")
    email = models.EmailField(default="")
    date_of_birth = models.DateField(default=None, blank=True, null=True)
    age = models.IntegerField(default=None, blank=True, null=True, validators=[validators.MinValueValidator(0)])
    phone_number = models.CharField(
        max_length=20,
        default="",
        blank=True,
        null=True,
        validators=[validators.RegexValidator(regex='^[0-9]*$', message='Enter a valid phone number.', code='invalid_number')]
    )
    address = models.TextField(default="", blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    usertype = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='buyer')

    def __str__(self):
        return self.user.username



class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    CONDITION_CHOICES = [
        ('New', 'New'),
        ('Used', 'Used'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
    ]
    
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Sold', 'Sold'),
        ('Pending', 'Pending'),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Available')
    image = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    PAYMENT_METHODS = [
        ('Card', 'Card'),
        ('PayPal', 'PayPal'),
        ('COD', 'Cash on Delivery'),
    ]

    ORDER_STATUSES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    ]

    PAYMENT_STATUSES = [
        ('Unpaid', 'Unpaid'),
        ('Paid', 'Paid'),
    ]

    order_id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_orders')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='ordered_product')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_orders')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='COD')
    delivery_address = models.TextField(default='ABC')  # New field for address
    order_status = models.CharField(max_length=10, choices=ORDER_STATUSES, default='Pending')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUSES, default='Unpaid')  # New field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_id} - {self.product.title} ({self.order_status}) - {self.payment_status}"



class Transaction(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="transaction")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_charge_id = models.CharField(max_length=255)  # Store Stripe Payment ID
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.id} - Order {self.order.order_id} - ${self.amount}"
    

from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")
    reported_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    reported_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="reported_users")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report {self.report_id} by {self.reported_by.username}"
