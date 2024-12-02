from django.db import models

# Create your models here.
class Ranking(models.Model):
    nickname = models.CharField(max_length=255)
    time = models.DecimalField(max_digits=10, decimal_places=2)
    mailboxes = models.IntegerField()