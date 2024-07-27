from django.db import models

class Gaminglaptop(models.Model):
    Name = models.CharField()
    Price = models.IntegerField()
    Description = models.TextField()

    def __str__(self):
        return self.Name

class LaptopPriceAlert(models.Model):
    laptop_name = models.CharField()
    desired_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.laptop_name} - ₹{self.desired_price}"