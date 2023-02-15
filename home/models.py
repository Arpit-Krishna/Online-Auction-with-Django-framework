from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django_resized import ResizedImageField
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sdate = models.DateField(auto_now=True, auto_now_add=False)
    image=  models.ImageField(default="/media/product_image/2616533-200.png",upload_to="media/product_image")
    def __str__(self):
        return self.name



class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    desc = models.TextField()
    def __str__(self):
        return self.name 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='static/default.png', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username
    #resizing image
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 50 or img.width > 50:
            new_img = (50, 50)
            img.thumbnail(new_img)
            img.save(self.avatar.path)