from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('server', 'Server'),
        ('barista', 'Barista'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='server')

    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='customuser_groups',  
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='customuser_permissions', 
        blank=True
    )

    def __str__(self):
        return self.username


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price}€"


class Order(models.Model):
    STATUS_CHOICES = [
        ('received', 'Received'),
        ('ready', 'Ready'),
    ]
    server = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    table_number = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default = True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')
    is_accepted_by_server = models.BooleanField(default=False)

    def __str__(self):
        return f"Table #{self.table_number} - {self.get_status_display()}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name= 'items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity}"