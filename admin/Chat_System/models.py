from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            # Define your maximum image size here
            max_width = 400
            max_height = 200

            if img.width > max_width or img.height > max_height:
                output_size = (max_width, max_height)
                img.thumbnail(output_size)
                img.save(self.image.path)