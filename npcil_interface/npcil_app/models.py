from django.db import models

# Create your models here.
class Package(models.Model):
    package_id = models.CharField(max_length=50, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    version = models.CharField(max_length=50)
    node_id = models.CharField(max_length=50)

    def __str__(self):
        return(f'{self.name} {self.version}')

class Product(models .Model) :
    name = models. CharField(max_length=100)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    description = models.TextField( )
    is_available = models.BooleanField()
