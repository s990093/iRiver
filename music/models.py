from django.db import models
from django.utils import timezone
# Create your models here.

class Post(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    body = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date' , )
    def __str__(self):
        return f"{self.name} ({self.pub_date})"

class music(models.Model):
    title = models.CharField(max_length=100)
    song_ID = models.CharField(max_length=100)
    song_img_url = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    artist_url = models.CharField(max_length=100, default='')
    artist_img_url = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date' , )

    def __str__(self):
        return f"{self.title}  / {self.song_ID} / ({self.pub_date})"
    