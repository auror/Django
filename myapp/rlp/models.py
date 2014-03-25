from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class movie(models.Model):
    name = models.CharField(max_length=20)
    year_released = models.IntegerField(default=0)
    revenue = models.FloatField()
    director = models.CharField(max_length=20)
    producer = models.CharField(max_length=20)
    actor = models.CharField(max_length=20)
    actress = models.CharField(max_length=20)
    #user = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

    class Meta:
        permissions = (
            ('view_movie', 'View Movie'),
            )
        verbose_name_plural = 'movies'
