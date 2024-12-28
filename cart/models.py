from django.db import models

class Configuration(models.Model):
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=5.00)

    def save(self, *args, **kwargs):
        # Ensure only one configuration instance exists
        if not self.pk and Configuration.objects.exists():
            raise ValueError("Only one configuration instance is allowed.")
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Configuration (Delivery Fee: {self.delivery_fee})"

    class Meta:
        verbose_name = "Configuration"
        verbose_name_plural = "Configurations"
