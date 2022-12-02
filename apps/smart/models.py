
from django.db import models
from django.contrib.auth import get_user_model
from django.forms import DateTimeField
from slugify import slugify

from .utils import get_time


User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=250, primary_key=True, blank=True)
    
    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория',
        verbose_name_plural = 'Категории'


class Smart(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, primary_key=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    in_stock = models.BooleanField(default=False)
    image = models.ImageField(upload_to='smart_images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.IntegerField(default=0)
    color = models.CharField(max_length=100)
    ram = models.CharField(max_length=10)
    sim = models.CharField(max_length=20)
    parametr = models.TextField()
    description = models.TextField()
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='smarts')


    
    def save(self, *args, **kwargs):
        self.in_stock = self.quantity > 0
        if not self.slug:
            self.slug = slugify(self.title + get_time())
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class SmartImage(models.Model):
    image = models.ImageField(upload_to='smart_images/carousel')
    smart = models.ForeignKey(
        to=Smart,
        on_delete=models.CASCADE,
        related_name='smart_images'
    )


class Comment(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    smart = models.ForeignKey(
        to=Smart,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment from {self.user.username} to {self.smart.title}'


class Rating(models.Model):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    RATING_CHOICES = (
        (ONE, '1'),
        (TWO, '2'),
        (THREE, '3'),
        (FOUR, '4'),
        (FIVE, '5')
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES, 
        blank=True, 
        null=True)
    smart = models.ForeignKey(
        to=Smart,
        on_delete=models.CASCADE,
        related_name='ratings'
    )

    def __str__(self):
        return str(self.rating)


class Like(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    smart = models.ForeignKey(
        to=Smart,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    def __str__(self) -> str:
        return f'Liked by {self.user.username}'

