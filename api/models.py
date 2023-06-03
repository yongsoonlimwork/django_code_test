from django.db import models


# Create your models here.

class CustomerRequest(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField()
    pack1 = models.TextField()
    pack2 = models.TextField()
