from django.db import models

# Create your models here.
class StoreList(models.Model):
    store_name = models.CharField(max_length=50, blank = True, null = True)
    gst_No = models.CharField(max_length=16)
    trade_licence = models.CharField(max_length=10)
    food_licence = models.CharField(max_length=10)
    store_location = models.CharField(max_length=10)

class Store(models.Model):
    Store_name=models.CharField(max_length=50, blank = True, null = True)
    store_file = models.ImageField(null=True, default=None, blank=True)
    legal_name = models.CharField(max_length=50, blank = True, null = True)
    select_region = models.CharField(max_length=50, blank = True, null = True)
    gst_No = models.CharField(max_length=50, blank = True, null = True)
    gst_attach = models.ImageField(null=True, default=None, blank=True)
    pan_card = models.CharField(max_length=50, blank = True, null = True)
    pan_attach = models.ImageField(null=True, default=None, blank=True)
    food_licence = models.CharField(max_length=50, blank = True, null = True)
    food_attach = models.ImageField(null=True, default=None, blank=True)
    trade_licence = models.CharField(max_length=50, blank = True, null = True)
    trade_attach = models.ImageField(null=True, default=None, blank=True)
    store_location = models.CharField(max_length=50, blank = True, null = True)
    address = models.CharField(max_length=50, blank = True, null = True)
    pincode = models.ImageField(max_length=10)
    state = models.CharField(max_length=50, blank = True, null = True)
    contact_person = models.CharField(max_length=50, blank = True, null = True)
    mobile = models.ImageField(max_length=10)
    remarks = models.CharField(max_length=50, blank = True, null = True)
