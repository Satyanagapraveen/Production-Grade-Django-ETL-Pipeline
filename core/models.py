from django.db import models

# Create your models here.
class LegacyOrder(models.Model):
    external_id=models.CharField(max_length=100,unique=True)
    raw_data=models.JSONField()
    migrated=models.BooleanField(default=False)

    def __str__(self):
        return self.external_id
    
class Order(models.Model):
    external_id = models.CharField(max_length=100, unique=True)
    customer_email = models.EmailField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.external_id
    
class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='lines')
    sku = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.sku} (x{self.quantity})"



